
# from turtle import st
from getmac import get_mac_address
import serial.tools.list_ports
import yaml

def findPorts(strIn1,strIn2):
    ports = list(serial.tools.list_ports.comports())
    allPorts = []
    for p in ports:
        currentPortStr1 = str(p[1])
        currentPortStr2 = str(p[2])
        if(currentPortStr1.find(strIn1)>=0 and currentPortStr2.find(strIn2)>=0 ):
            allPorts.append(str(p[0]).split(" ")[0])
    return allPorts

def findPortsGPS(strIn1):
    ports = list(serial.tools.list_ports.comports())
    allPorts = []
    for p in ports:
        currentPortStr1 = str(p[1])
        if(currentPortStr1.find(strIn1)>=0):
            allPorts.append(str(p[0]).split(" ")[0])
    return allPorts
  
  
  
def findMacAddress():
    macAddress= get_mac_address(interface="eth0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="docker0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp1s0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp31s0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="wlan0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    return "xxxxxxxx"


latestDisplayOn       = False
latestOn              = False

macAddress               = findMacAddress()

mintsDefinitions         = yaml.load(open('mintsXU4/credentials/mintsDefinitions.yaml'),Loader=yaml.FullLoader)
credentials              = yaml.load(open('mintsXU4/credentials/credentials.yaml'),Loader=yaml.FullLoader)
loRaCredentials          = yaml.load(open('mintsXU4/credentials/loRacredentials.yaml'),Loader=yaml.FullLoader)
fPortIDs                 = yaml.load(open('mintsXU4/credentials/portIDs.yaml'),Loader=yaml.FullLoader)['portIDs']
nodeIDs                  = yaml.load(open('mintsXU4/credentials/nodeIDs.yaml'),Loader=yaml.FullLoader)

mqttCredentialsFile      = 'mintsXU4/credentials/credentials.yaml'
mqttBroker               = "mqtt.circ.utdallas.edu"
mqttPort                 =  8883  # Secure port

keys                     = yaml.load(open('mintsXU4/credentials/keys.yaml'),Loader=yaml.FullLoader)

dataFolder                = mintsDefinitions['dataFolder']
dataFolderTmp             = mintsDefinitions['dataFolderTmp']
dataFolderJson            = mintsDefinitions['dataFolderJson']


dataFolderReference       = "/home/teamlary/mintsData/reference"
dataFolderMQTTReference   = "/home/teamlary/mintsData/referenceMQTT"
dataFolderMQTT            = "/home/teamlary/mintsData/rawMQTT"

mqttPortLoRa              = loRaCredentials['port']
mqttBrokerLoRa            = loRaCredentials['broker']

mqttOn                    = True

nodeIDs                  = nodeIDs['nodeIDs']

keys                     = yaml.load(open('mintsXU4/credentials/keys.yaml'),Loader=yaml.FullLoader)

appKey                   = keys['appKey']


# mqttBroker                = mintsDefinitions['broker']
tlsCert                   = mintsDefinitions['tlsCert']

loRaE5MiniPorts          = findPorts("CP2102N USB to UART Bridge Controller","PID=10C4:EA60")
canareePorts             = findPorts("Canaree PM","PID=10C4:EA60")
gpsPorts                 = findPortsGPS("u-blox")

    
rainPorts                = ['/dev/ttyS1'] # Direct connected to the gpio port - May not be available on all polo nodes


 
# For Ref Light Module 


darkSpectrumFile         = \
    "darkSpectrums/Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:1_0_s-_StA:5-_BCW:5-_DT:2024-02-07_17:54:22_097455+00:00.pkl"

calibrationFile          = \
    "calibrationFiles/SR200544_cc_20230323_OOIIrrad.CAL"

electricDarkCorrelationUsage = False
nonLinearityCorrectionUsage  = False
integrationTimeMicroSec      = 1000000 
integrationTimeSec           = integrationTimeMicroSec/1000000
scansToAverage               = 5
boxCarWidth                  = 5 
fiberDiametorMicroMeter      = 200
     