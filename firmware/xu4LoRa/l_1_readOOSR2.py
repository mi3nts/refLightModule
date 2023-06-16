
from __future__ import annotations
# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
import itertools
import base64
from cgitb import strong
# import imp
# from this import d
import paho.mqtt.client as mqtt
import datetime 
from datetime import timedelta
import yaml
import collections
import json
import time 
import serial.tools.list_ports
from collections import OrderedDict
from glob import glob
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsPoLo as mPL
from collections import OrderedDict
import struct
import numpy as np
import pynmea2
import shutil


from oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError
from oceandirect.od_logger import od_logger
from threading import Thread
logger = od_logger()
od = OceanDirectAPI()

from mintsXU4 import mintsOptics as mO

import math
import sys
import time
import os

debug  = False 

devicesPresent = False
deviceOpen = False

macAddress          = mD.macAddress

electricDarkCorrelationUsage = False
nonLinearityCorrectionUsage  = True
integrationTimeMicroSec      = 1000 


if __name__ == "__main__":
    
    print()
    print("============ MINTS Reference Light Module ============")
    print()

    devicesPresent, deviceIDs = mO.checkingDevicePresence()
    device, deviceOpen, deviceID, deviceSerialNumber = \
        mO.openDevice(deviceOpen,devicesPresent,deviceIDs)
    
    mO.setUpDevice(devicesPresent, deviceOpen, device,\
                    electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                    integrationTimeMicroSec,\
                    )
    

    mO.getSingleSpectrum(devicesPresent,deviceOpen,device)


    mO.getSingleSpectrum(devicesPresent,deviceOpen,device)
    

    mO.closeDevice(deviceOpen,devicesPresent,deviceID)

    

   
    # while True:
    #     try:    



        # except Exception as e:
        #     time.sleep(.5)
        #     print ("Error and type: %s - %s." % (e,type(e)))
        #     time.sleep(.5)
        #     print("Data Packet Not Sent")
        #     time.sleep(.5)

                  
        
        
        

        
        
        
        
        