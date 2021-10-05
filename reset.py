from github import Github
from slack import Slack
from gradle import Gradle
from sonarqube import Sonarqube
from dockerhub import Dockerhub
from dependency import Dependency
from anchore import Anchore
from argocd import Argocd
import yaml
from jenkinsapi.jenkins import Jenkins
import urllib.parse
import requests
import base64
from xml.etree.ElementTree import parse
import json
import sys

def stringToBase64(s):
        return base64.b64encode(s.encode('utf-8'))

def xml_modify(filename, **kargs):
    tree = parse(filename)
    root = tree.getroot()
    for tag, value in kargs.items():
        for i in root.iter(tag):
            i.text = value
    tree.write(filename, encoding='UTF-8', xml_declaration=True)

with open(sys.argv[1]) as g:
    file = yaml.load(g, Loader=yaml.FullLoader)

toolList = []
pluginList = []
stages = []

for dict in file:
    if dict['tool']['name'] == "jenkins":
        toolList.append("jenkins")
        jenkins_data = dict['tool']['data']

    elif dict['tool']['name'] == "github":
        toolList.append("github")
        pluginList.append("github-pullrequest@0.3.0")
        github_data = dict['tool']['data']
        github_cred = dict['tool']['credential']
        github_webhook = dict['tool']['webhook']

    elif dict['tool']['name'] == 'slack':
        toolList.append("slack")
        pluginList.append("slack@2.48")
        slack_data = dict['tool']['data']
        slack_cred = dict['tool']['credential']

    elif dict['tool']['name'] == 'gradle':
        toolList.append("gradle")

    elif dict['tool']['name'] == 'sonarqube':
        toolList.append("sonarqube")
        pluginList.append("sonar@2.13.1")
        sonar_data = dict['tool']['data']
        sonar_cred = dict['tool']['credential']

    elif dict['tool']['name'] == 'dockerhub':
        toolList.append("dockerhub")
        pluginList.append("docker-plugin@1.2.3")
        pluginList.append("docker-workflow@1.26")
        dockerhub_data = dict['tool']['data']
        dockerhub_cred = dict['tool']['credential'] 

    elif dict['tool']['name'] == 'anchore':
        toolList.append("anchore")
        pluginList.append("anchore-container-scanner@1.0.23")
        anchore_data = dict['tool']['data']
        anchore_cred = dict['tool']['credential']

    elif dict['tool']['name'] == 'dependency':
        toolList.append("dependency")
        pluginList.append("dependency-check-jenkins-plugin@5.1.1")

    elif dict['tool']['name'] == 'argocd':
        toolList.append("argocd")
        pluginList.append("ssh-agent@1.23")
        argocd_data = dict['tool']['data']
        argocd_cred = dict['tool']['credential']
        
    else:
        print("Invalid tool name")


jenkins_url = "http://{}".format(jenkins_data['url'])
jenkins = Jenkins(jenkins_url, username=jenkins_data['username'], password=jenkins_data['password'], useCrumb=True)
jobList = jenkins.get_jobs_list()

if len(sys.argv) > 2:
    print("Too many arguments")
elif len(sys.argv) == 2:
    if sys.argv[1] in jobList:
        jenkins.delete_job(sys.argv[1])
        print("Deleted job: \"{}\"".format(sys.argv[1]))
    else:
        print("Not exist \"{}\" pipeline".format(sys.argv[1]))
else:
    if len(jobList) > 0:
        for job in jobList:
            jenkins.delete_job(job)
            print("Deleted job: \"{}\"".format(job))
    else:
        print("No job in your jenkins")


def deleteFileInRepository(filepath):
    github_apiurl = "https://api.github.com/repos/{0}/{1}/contents/{2}".format(github_data['username'], github_data['reponame'], filepath)
    github_body = {}
    github = Github(jenkins, token=github_data['token'], cred_id=github_cred['id'], cred_description=github_cred['description'], url=github_data['url'])
    response = github.call_api("GET", github_apiurl, github_body)

    if response.status_code == 200:
        print("{} exist in github repository".format(filepath))
        jsondata = json.loads(response.text)
        sha = jsondata['sha']

        # delete file in github repository
        url = "https://api.github.com/repos/{0}/{1}/contents/{2}".format(github_data['username'], github_data['reponame'], filepath)
        body = {
                "message": "delete file using api",
                "sha": sha
        }
        response = github.call_api("DELETE", github_apiurl, body)
        if response.status_code == 200:
            print("Complete Delete! \"{}\"".format(filepath))
        else:
            print("Failed delete \"{}\"".format(filepath))
    else:
        print("not exist {} in github repository".format(filepath))



deleteFileInRepository("jenkinsfile")
deleteFileInRepository("Dockerfile")
deleteFileInRepository("templates/deployments.yaml")
deleteFileInRepository("templates/svc.yaml")