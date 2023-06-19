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

def openDevice(deviceIDs,deviceIndex):
    deviceID = deviceIDs[deviceIndex]
    device   = od.open_device(deviceID)
    serialNumber = device.get_serial_number()
    print("Device Serial Number: %s" % serialNumber)
    return deviceID,device,serialNumber;
    

def getSpectrumDetails(device):
    device.details()
    waveLengths = device.get_wavelengths()
    # print("Wave Lengths")
    # print(waveLengths)
    # print("Number of Wavelengths returned")
    # print(len(waveLengths))
    return waveLengths


def setUpDevice(device,\
                electricDarkCorrelationUsage,\
                nonLinearityCorrectionUsage,\
                integrationTimeMicroSec,\
                ):
    print("Setting Dark Correction usage to: " +electricDarkCorrelationUsage)
    device.set_electric_dark_correction_usage(electricDarkCorrelationUsage)
    print("Setting Nonlinearity Correction usage to: " +electricDarkCorrelationUsage)
    device.set_nonlinearity_correction_usage(nonLinearityCorrectionUsage)
    print("Settin Integration Time to: " +electricDarkCorrelationUsage + " micro seconds")
    device.set_integration_time(integrationTimeMicroSec)

def getSingleSpectrum(device):
    print("Obtaining Spectrum")
    spectra = device.get_formatted_spectrum()
    # print(spectra)
    # print(len(spectra))
    return spectra;


def closeDevice(deviceID):
    print("Closing Device")
    od.close_device(deviceID);


        

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

