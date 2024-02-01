from __future__ import annotations
import serial
from datetime import datetime, timezone
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
from matplotlib import pyplot as plt
import pickle

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
    # serialNumber = device.get_serial_number()
    # print("Device Serial Number: %s" % serialNumber)
    return deviceID,device;
    

def getSpectrumDetails(device):
    device.details()
    waveLengths = device.get_wavelengths()
    # print("Wave Lengths")
    # print(waveLengths)
    # print("Number of Wavelengths returned")
    # print(len(waveLengths))
    return waveLengths

def getAllSpectrumDetails(device):

    print("===========================")
    print("Ocean Optics Spectrum Info:")
    # device.details()
    # time.sleep(1)
    deviceType         = device.get_device_type()
    print("Device Type                 :",deviceType)
    time.sleep(1)

    deviceModel        = device.get_model()
    print("Device Model                :",deviceModel)
    time.sleep(1)

    serialNumber       = device.get_serial_number()
    print("Serial Number               :",serialNumber)    
    time.sleep(1)

    maxIntensity       = device.get_max_intensity ()
    print("Max Intensity               :",maxIntensity)
    time.sleep(1)

    minIntegrationTime = device.get_minimum_integration_time()    
    print("Minimum Integration Time    :",minIntegrationTime)    
    time.sleep(1)

    maxIntegrationTime = device.get_maximum_integration_time()
    print("Maximum Integration Time    :",maxIntegrationTime)   
    time.sleep(1)

    integrationTime    = device.get_integration_time()
    print("Integration Time            :",integrationTime)    
    time.sleep(1)
    
    numberOfDarkPixeks = device.get_number_electric_dark_pixels()
    print("# of Dark Pixels            :",numberOfDarkPixeks)    
    time.sleep(1)    
    
    acquisitionDelay               = device.get_acquisition_delay()
    print("Acquisition Delay           :",acquisitionDelay)
    time.sleep(1)
    
    acquisitionDelayIncrement      = device.get_acquisition_delay_increment()
    print("Acquisition Delay Incriment :",acquisitionDelayIncrement)
    time.sleep(1)
    
    acquisitionDelayIncrementMin   = device.get_acquisition_delay_minimum()
    print("Minimum Acquisition Delay   :",acquisitionDelayIncrementMin)
    time.sleep(1)
    
    acquisitionDelayIncrementMax   = device.get_acquisition_delay_maximum()
    print("Maximum Acquisition Delay   :",acquisitionDelayIncrementMax)
    time.sleep(1)
    
    nonLinearityCorrectionUsage    = device.get_nonlinearity_correction_usage()
    print("Non Linearaty Correction    :",nonLinearityCorrectionUsage)

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

def obtainDarkSpectrums(device,\
                       integrationTimeMicroSec):
    
    dateTime     = datetime.now(timezone.utc)
    
    print("Collecting a Dark Spectrum")
    

    time.sleep(1)
    waveLengths                = device.get_wavelengths()
    time.sleep(1)
    serialNumber               = device.get_serial_number()
    time.sleep(1)   


    # 11 --------------
    electricDarkCorrelationUsage =  True 
    nonLinearityCorrectionUsage  =  True 
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)
    preTitle = "Formatted Spectrum 11"
    formattedSpectrum                   = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)
    
    pickleListFloatSave(formattedSpectrum,"darkSpectrums/" + labelNoSpaces)

    # 10 --------------
    electricDarkCorrelationUsage =  True 
    nonLinearityCorrectionUsage  =  False 
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)
    preTitle = "Formatted Spectrum 10"
    formattedSpectrum                   = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)
    
    pickleListFloatSave(formattedSpectrum,"darkSpectrums/" + labelNoSpaces)


    # 01 --------------
    electricDarkCorrelationUsage =  False 
    nonLinearityCorrectionUsage  =  True 
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    

    time.sleep(1)
    preTitle = "Formatted Spectrum 01"
    formattedSpectrum                   = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)
    
    pickleListFloatSave(formattedSpectrum,"darkSpectrums/" + labelNoSpaces)
   
   # 00 --------------
    electricDarkCorrelationUsage =  False 
    nonLinearityCorrectionUsage  =  False 
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)
    preTitle = "Formatted Spectrum 00"
    formattedSpectrum                   = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)
    
    pickleListFloatSave(formattedSpectrum, "darkSpectrums/" + labelNoSpaces)


def getStringTitle(serialNumber, preTitle,\
                electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                            dateTime):
    
    titleStr = preTitle + " for SN: " + str(serialNumber) \
                  + " ,EDCU: " + str(electricDarkCorrelationUsage)\
                  + " ,NLCU: " + str(nonLinearityCorrectionUsage)\
                  + " ,IT: " + str(integrationTimeMicroSec/1000000) +" s"\
                  + " ,Date Time: " + str(dateTime) 

    return titleStr,titleStr.replace(" ","_").replace(",","_").replace(".","_");


def pickleListFloatSave(floatList,fileName):
    try:
        with open( fileName + '.pkl', 'wb') as file:
            pickle.dump(floatList, file)
    except Exception as e:
        print(f"An error occurred: {e}")


def pickleListFloatLoad(fileName):
    try:
        with open(fileName, 'rb') as file:
            loaded_float_list = pickle.load(file)
            # print("Loaded float list:", loaded_float_list)
    except Exception as e:
        print(f"An error occurred: {e}")
    return loaded_float_list; 

def plotter(waveLengths,spectrum,\
            titleName, fileName):
    plt.figure()
    plt.plot(waveLengths,spectrum)
    plt.xlabel('Wave Lengths (nm)')
    plt.ylabel('Energy')

    # titleStr = preTitle + " for SN: " + str(serialNumber) \
    #               + " ,EDCU: " + str(electricDarkCorrelationUsage)\
    #               + " ,NLCU: " + str(nonLinearityCorrectionUsage)\
    #               + " ,IT: " + str(integrationTimeMicroSec/1000000) +" s"\
    #               + " ,Date Time: " + str(dateTime) 

    font = {'weight' : 'bold',
                'size'   : 5}

    plt.rc('font', **font)
    plt.title(titleName)
    plt.savefig(fileName+".png")
    plt.close()


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


def getCorrectedSpectrums(device,integrationTimeMicroSec,serialNumber,waveLengths,darkSpectrumFile):

    print("Loading dark spectrum file")
    darkSpectrum = pickleListFloatLoad(darkSpectrumFile)

    dateTime     = datetime.now(timezone.utc)
    print("Collecting an Ambient Spectrum")
    
    # Dark Spectrum --------------
    preTitle = "Dark Spectrum at 00"
    
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,darkSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    # 00 --------------
    preTitle = "DC 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.get_dark_corrected_spectrum1(darkSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    # 00 --------------
    preTitle = "DC + NL 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.nonlinearity_correct_spectrum1(darkSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces) 



    # # 01 --------------
    # preTitle = "DC 01"
    # electricDarkCorrelationUsage =  False
    # nonLinearityCorrectionUsage  =  True
    # setUpDevice(device,\
    #                     electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                     integrationTimeMicroSec,\
    #                     )
    # time.sleep(1)

    # formattedSpectrum                   = device.get_dark_corrected_spectrum1(darkSpectrum)
    # labelSpaced, labelNoSpaces = \
    #             getStringTitle(serialNumber, preTitle,\
    #                 electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                         integrationTimeMicroSec,\
    #                             dateTime)
    
    # plotter(waveLengths,formattedSpectrum,\
    #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    # 10 --------------
    # preTitle = "DC 10"    
    # electricDarkCorrelationUsage =  True
    # nonLinearityCorrectionUsage  =  False
    # setUpDevice(device,\
    #                     electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                     integrationTimeMicroSec,\
    #                     )
    # time.sleep(1)

    # formattedSpectrum                   = device.get_dark_corrected_spectrum1(darkSpectrum)
    # labelSpaced, labelNoSpaces = \
    #             getStringTitle(serialNumber, preTitle,\
    #                 electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                         integrationTimeMicroSec,\
    #                             dateTime)
    
    # plotter(waveLengths,formattedSpectrum,\
    #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    # # 11 --------------
    # preTitle = "DC 11"    
    # electricDarkCorrelationUsage =  True
    # nonLinearityCorrectionUsage  =  True
    # setUpDevice(device,\
    #                     electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                     integrationTimeMicroSec,\
    #                     )
    # time.sleep(1)

    # formattedSpectrum                   = device.get_dark_corrected_spectrum1(darkSpectrum)
    # labelSpaced, labelNoSpaces = \
    #             getStringTitle(serialNumber, preTitle,\
    #                 electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                         integrationTimeMicroSec,\
    #                             dateTime)
    
    # plotter(waveLengths,formattedSpectrum,\
    #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

 










    # preTitle = "Ambient Spectrum 00"
    # formattedSpectrum                   = device.get_nonlinearity_corrected_spectrum1(darkSpectrum)
    # labelSpaced, labelNoSpaces = \
    #             getStringTitle(serialNumber, preTitle,\
    #                 electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                         integrationTimeMicroSec,\
    #                             dateTime)
    
    # plotter(waveLengths,formattedSpectrum,\
    #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)    

