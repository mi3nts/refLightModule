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
from matplotlib import pyplot as plt
from datetime import datetime, timezone
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

debug          = False 

devicesPresent = False
deviceOpen     = False

metaPlotter = False

macAddress          = mD.macAddress


electricDarkCorrelationUsage = mD.electricDarkCorrelationUsage
nonLinearityCorrectionUsage  = mD.nonLinearityCorrectionUsage
integrationTimeMicroSec      = mD.integrationTimeMicroSec

scansToAverage               = mD.scansToAverage
boxCarWidth                  = mD.boxCarWidth
integrationTimesInMicroSec   = list(range(500000, 6000001, 500000)) 


if __name__ == "__main__":
    
    print()
    print("============ MINTS Reference Light Module ============")
    print()

    devicesPresent, deviceIDs = mO.checkingDevicePresence()

    if devicesPresent:
        
        print("Ocean Optics Spectrometors found")
        # Only choosing the 1st Device
        deviceID,device             =  mO.openDevice(deviceIDs,0)


        serialNumber, waveLengths   =  mO.getAllSpectrumDetails(device)   
        
        dateTime     = datetime.now(timezone.utc)
        for integrationTimeMicroSec in integrationTimesInMicroSec:
            time.sleep(1)
            mO.storeDarkSpecta(
                device,\
                    dateTime,\
                        electricDarkCorrelationUsage,\
                            nonLinearityCorrectionUsage,\
                                integrationTimeMicroSec,\
                                    scansToAverage,\
                                        boxCarWidth,\
                                )
            
              

        mO.closeDevice(deviceID)
    
    else:
        print("No Ocean Optics Spectrometors found")
        

        













