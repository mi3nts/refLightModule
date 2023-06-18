
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
    if devicesPresent:
        print("Ocean Optics Spectrometors found")
        mO.openDevice(deviceOpen,devicesPresent,deviceIDs)
    
    # Only choosing the 1st Device
    deviceID,device,serialNumer =  mO.openDevice(deviceIDs,0)
    
    mO.setUpDevice(device,\
                    electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                    integrationTimeMicroSec,\
                    )

    mO.getSingleSpectrum(device)
   

    mO.closeDevice(deviceID)

    

