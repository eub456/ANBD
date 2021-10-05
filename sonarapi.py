from sonarqube import SonarQubeClient
from sonarqube.utils.rest_client import RestClient
from sonarqube.utils.config import (
    API_PLUGINS_AVAILABLE_ENDPOINT,
    API_PLUGINS_CANCEL_ALL_ENDPOINT,
    API_PLUGINS_INSTALL_ENDPOINT,
    API_PLUGINS_INSTALLED_ENDPOINT,
    API_PLUGINS_PENDING_ENDPOINT,
    API_PLUGINS_UNINSTALL_ENDPOINT,
    API_PLUGINS_UPDATE_ENDPOINT,
    API_PLUGINS_UPDATES_ENDPOINT,
)
from sonarqube.utils.common import GET, POST

url = 'http://3.35.233.3:9000'
username = "admin"
password = "user"
sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)

plugins = sonar.plugins.get_available_plugins()
print(plugins)

sonar.plugins.install_plugin(key="dependencycheck")
