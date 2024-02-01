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

def getAllSpectrumDetails(device):
    print("Ocean Optics Spectrum Details Complete:")
    device.details()
    time.sleep(1)
    deviceType         = device.get_type()
    time.sleep(1)
    deviceModel        = device.get_model()
    time.sleep(1)
    serialNumber       = device.get_serial_number()
    time.sleep(1)
    maxIntensity       = device.get_max_intensity ()
    time.sleep(1)
    minIntegrationTime = device.get_minimum_integration_time()    
    time.sleep(1)
    maxIntegrationTime = device.get_maximum_integration_time()
    time.sleep(1)
    integrationTime    = device.get_integration_time()
    time.sleep(1)
    numberOfDarkPixeks = device.get_number_electric_dark_pixels()
    time.sleep(1)    
    # device.details() 
    # time.sleep(1)
    acquisitionDelay               = device.get_acquisition_delay()
    time.sleep(1)
    acquisitionDelayIncrement      = device.get_acquisition_delay_increment()
    time.sleep(1)
    acquisitionDelayIncrementMin   = device.get_acquisition_delay_minimum()
    time.sleep(1)
    acquisitionDelayIncrementMax   = device.get_acquisition_delay_maximum()
    time.sleep(1)
    nonLinearityCorrectionUsage    = device.get_nonlinearity_correction_usage()


    print("Device Type", deviceType)
    print("Device Model", deviceModel)
    print("Serial Number", serialNumber)
    print("Max Intensity", maxIntensity)
    print("Minimum Integration Time", minIntegrationTime)
    print("Maximum Integration Time", maxIntegrationTime)
    print("Integration Time", integrationTime)
    print("# of Dark Pixels", numberOfDarkPixeks)
    print("Acquisition Delay", acquisitionDelay)
    print("Minimum Acquisition Delay",acquisitionDelayIncrementMin)
    print("Maximum Acquisition Delay",acquisitionDelayIncrementMax)
    print("Non Linearaty Correction",acquisitionDelayIncrementMax)
    
    return;



def setUpDevice(device,\
                electricDarkCorrelationUsage,\
                nonLinearityCorrectionUsage,\
                integrationTimeMicroSec,\
                ):
    print("Setting Dark Correction usage to: " +str(electricDarkCorrelationUsage))
    device.set_electric_dark_correction_usage(electricDarkCorrelationUsage)
    print("Setting Nonlinearity Correction usage to: " +str(electricDarkCorrelationUsage))
    device.set_nonlinearity_correction_usage(nonLinearityCorrectionUsage)
    print("Settin Integration Time to: " +str(integrationTimeMicroSec)+ " micro seconds")
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

