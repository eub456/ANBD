from variable import Variable
import sys

var = Variable(sys.argv[1])
toolList = var.getToolList()
pluginList = var.getPluginList()

if "jenkins" not in toolList:
    print("Not exist jenkins tool in your yaml!")
    exit()

print(var, toolList, pluginList)
print("haha",var.getJenkinsData()['url'])