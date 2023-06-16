from __future__ import annotations
import serial
import datetime
import os
import csv
#import deepdish as dd
# from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
# from mintsXU4 import mintsSensorReader as mSR
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import math
import base64
import json
import struct
import numpy as np
from datetime import timedelta


from oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError
from oceandirect.od_logger import od_logger
from threading import Thread


macAddress     = mD.macAddress
dataFolder     = mD.dataFolder
fPortIDs        = mD.fPortIDs

mqttOn         = mD.mqttOn
decoder        = json.JSONDecoder(object_pairs_hook=OrderedDict)
od = OceanDirectAPI()

# Gives the first device it detects 
def checkingDevicePresence():
    od.find_usb_devices()

    deviceIDs   = od.get_device_ids()
    deviceCount = len(deviceIDs)
    if deviceCount:
        print("Ocean Optics devices found")
        return True,deviceIDs ;
    else:
        print("Ocean Optics devices not found")
        return False, [];

def openDevice(deviceOpen,devicesPresent,deviceIDs):

    if devicesPresent:
        print("Ocean Optics Devices found:")
        if not(deviceOpen):
            print("Opening Device")
            device       = od.open_device(id)
        else:
            print("Device Already Opened")

        # Provide the first ID it finds
        for deviceID in deviceIDs:
            deviceSerialNumber = device.get_serial_number()
            print("Device Serial Number: %s" % deviceSerialNumber)
            return device,True,deviceID,deviceSerialNumber

    print("No devices found")
    return [],deviceOpen,[],[];

def closeDevice(devicesOpen,devicesPresent,deviceID):
    if devicesOpen and devicesPresent:
        od.close_device(deviceID);



def setUpDevice(devicesPresent, deviceOpen,device,\
                electricDarkCorrelationUsage,\
                nonLinearityCorrectionUsage,\
                integrationTimeMicroSec,\
                ):
    if devicesPresent:
        print("Devices Present")
        if deviceOpen:
            print("Device Open")
            print("Setting Up Device")
            device.set_electric_dark_correction_usage(electricDarkCorrelationUsage)
            device.set_nonlinearity_correction_usage(nonLinearityCorrectionUsage)
            device.set_integration_time(integrationTimeMicroSec)
        else:
            print("Device not open")    
    else:
        print("No Devices found to setup")    

def getSingleSpectrum(devicesPresent, deviceOpen,device):
    if devicesPresent:
        print("Devices Present")
        if deviceOpen:
            print("Device Open")
            print("Setting Up Device")
            try: 
                spectra_m = device.get_formatted_spectrum()
                print(spectra_m)
                return spectra_m;
            except OceanDirectError as e:
                print("Error Reading Data")
                print(e.get_error_details())
                return [];
        else:
            print("Device not open")    
    else:
        print("No Devices found to setup")   


        

def getSpectraSingle(devicesPresent, deviceOpen,\
                     device,numbSpectra,logger):
    if devicesPresent:
        print("Devices Present")
        if deviceOpen:
            print("Device Open")
            print("Setting Up Device")    
            try: 
                device.set_scans_to_average(1)
                numb_pixel = len(device.get_formatted_spectrum()) 
                spectra_m = [[0 for x in range(numb_pixel)] for y in range(numbSpectra)]
                for i in range(numbSpectra):
                    spectra_m[i] = device.get_formatted_spectrum()
                return spectra_m;

            except OceanDirectError as e:
                logger.error(e.get_error_details())
                return;

        else:
            print("Device not open")    
    else:
        print("No Devices found to setup")   

def closeDevice(deviceOpen,devicesPresent,deviceID):
    if deviceOpen and devicesPresent:
        od.close_device(deviceID);
