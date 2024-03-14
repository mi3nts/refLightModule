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
import pandas as pd
import re
import sys
from oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError
from oceandirect.od_logger import od_logger
from threading import Thread
from mintsXU4 import mintsSensorReader as mSR
# Set these and collect a new Dark spectra 
# Individual commands to collect dark spectra 
# Individual command to collect ambient specta 
# Add it to the MQTT pipeline 
# Check on the calibration file 
# Add Box Car Width = 5 
# Scans to Average  = 10 


macAddress     = mD.macAddress
dataFolder     = mD.dataFolder
fPortIDs        = mD.fPortIDs

mqttOn         = mD.mqttOn
decoder        = json.JSONDecoder(object_pairs_hook=OrderedDict)
od = OceanDirectAPI()

max_cap         = mD.max_cap 

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

    scansToAverage     =  device.get_scans_to_average ()
    print("Scans To Average            :",scansToAverage)
    time.sleep(1)

    boxCarWidth        = device.get_boxcar_width()    
    print("Box Car Width               :",boxCarWidth)    
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

    time.sleep(1)
    waveLengths                    = device.get_wavelengths()
    
    return serialNumber, waveLengths;

def setUpDevice(device,\
                electricDarkCorrelationUsage,\
                nonLinearityCorrectionUsage,\
                integrationTimeMicroSec,\
                scansToAverage, \
                boxCarWidth\
                ):
    
    print("===========================")
    print("Setting up Device:")
    time.sleep(.5)    
    print("Setting Dark Correction usage to: " +str(electricDarkCorrelationUsage))
    device.set_electric_dark_correction_usage(electricDarkCorrelationUsage)
    time.sleep(.5)    
    
    print("Setting Nonlinearity Correction usage to: " +str(electricDarkCorrelationUsage))
    device.set_nonlinearity_correction_usage(nonLinearityCorrectionUsage)
    time.sleep(.5)

    print("Setting Integration Time to: " +str(integrationTimeMicroSec)+ " micro seconds")
    device.set_integration_time(integrationTimeMicroSec)
    time.sleep(.5)

    print("Setting Scans to Average to: " +str(scansToAverage)+ " scans")
    device.set_scans_to_average(scansToAverage)
    time.sleep(.5)

    print("Setting Boxcar Width to: " + str(boxCarWidth)+ " wave lengths")
    device.set_boxcar_width(boxCarWidth)
    time.sleep(.5)

def obtainDarkSpecta(
        device,\
            dateTime,\
                electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                            scansToAverage,\
                                boxCarWidth,\
                        ):
    print("===========================")
    print("Obtaining Dark Spectrum for integration time :" + str(integrationTimeMicroSec))
    time.sleep(1)
    waveLengths                = device.get_wavelengths()
    time.sleep(1)
    serialNumber               = device.get_serial_number()
    time.sleep(1)   

    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        scansToAverage,\
                        boxCarWidth 
                        )
    time.sleep(1)
    preTitle = "Dark Spectra"
    formattedSpectrum                   = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                scansToAverage,\
                                    boxCarWidth,\
                                        dateTime)
    
    plotter(waveLengths,\
                formattedSpectrum,\
                    "Wave Lengths (nm)",\
                        "Counts",\
                            labelSpaced,"darkSpectrums/" + labelNoSpaces)
    
    pickleListFloatSave(formattedSpectrum, "darkSpectrums/" + labelNoSpaces)


def getStringTitle(serialNumber, preTitle,\
                electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                            scansToAverage,\
                                boxCarWidth,\
                                    dateTime):
    
    titleStr = preTitle + " for SN:" + str(serialNumber) \
                  + ", EDCU:" + str(electricDarkCorrelationUsage)\
                  + ", NLCU:" + str(nonLinearityCorrectionUsage)\
                  + ", IT:" + str(integrationTimeMicroSec/1000000) + " s"\
                  + ", StA:" + str(scansToAverage) \
                  + ", BCW:" + str(boxCarWidth)  \
                  + ", DT:" + str(dateTime) \

    return titleStr,titleStr.replace(" ","_").replace(",","-").replace(".","_");

def plotter(waveLengths,spectrum,xLabel,yLabel,\
            titleName, fileName):
    print("===========================")
    print("Plotting:" + titleName)
    plt.figure(figsize=(16, 12))
    plt.plot(waveLengths,spectrum)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid(True)
    
    font = {'weight' : 'bold',
                'size'   : 10}
    plt.rc('font', **font)
    plt.title(titleName)
    plt.savefig(fileName+".png" ,dpi=300)
    plt.close()

def loadCalibrationData(calibrationFile):
    print("===========================")
    print("Loading calibration data file")
    calibrationData = []
    with open(calibrationFile, 'r') as file:
        # Skip the first 9 lines (header information)
        for _ in range(9):
            next(file)
        # Read the remaining lines and convert them to floats
        for line in file:
            float_value = float(line.strip())
            calibrationData.append(float_value)

    return calibrationData;

def loadDarkSpectra(darkSpectrumFile):
    print("===========================")
    print("Loading dark spectrum file")
    darkSpectrum = pickleListFloatLoad(darkSpectrumFile)
    return darkSpectrum;

def getDarkSpectaMeta(fileIn):
    print("===========================")
    print("Dark Spectra Meta Data")    
    # "Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:1_0_s-_StA:5-_BCW:5-_DT:2024-02-05_22:56:38_619126+00:00.pkl"
    # Define a regular expression pattern to capture the required components
    pattern = re.compile(r'SN:(\w+)-_EDCU:(\w+)-_NLCU:(\w+)-_IT:(\d+_\d+)_s-_StA:(\d+)-_BCW:(\d+)-_DT:(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}_\d{6})[+-]\d{2}:\d{2}.pkl')

    # Use the pattern to search for matches in the formatted string
    match = pattern.search(fileIn.replace("darkSpectrums/", ""))

    if match:
        serial_number = match.group(1)
        edcu_value = 0 if match.group(2) == "False" else 1 if match.group(2) == "True" else int(match.group(2))
        nlcu_value = 0 if match.group(3) == "False" else 1 if match.group(3) == "True" else int(match.group(3))
        
        it_value   = float(f"{match.group(4)}.{match.group(5)}") if match.group(5) else float(match.group(4))
        sta_value  = match.group(5)
        bcw_value  = match.group(6)
        dt_value   = match.group(7)

        # Extracting individual components of the datetime
        dt_components = dt_value.split('_')
        year, month, date = map(int, dt_components[0].split('-'))
        hour, minute, second = map(int, dt_components[1].split(':'))
        micro_seconds = int(dt_components[2])

        print("Serial Number:", serial_number)
        print("EDCU Value:", edcu_value)
        print("NLCU Value:", nlcu_value)
        print("IT Value:", it_value)
        print("StA Value:", sta_value)
        print("BCW Value:", bcw_value)
        print("Year:", year)
        print("Month:", month)
        print("Date:", date)
        print("Hour:", hour)
        print("Minute:", minute)
        print("Second:", second)
        print("Microseconds:", micro_seconds)
        darkSpectraTime =  "DST"+ "_" + str(year)+ "_" + str(month)+ "_" + str(date)+ "_" + str(minute)+ "_" + str(second)+ "_" + str(micro_seconds)

        return darkSpectraTime;
    else:
        time.sleep(5)
        print("No match found.")
        sys.exit()  
        return;

def getCalibrationMeta(fileIn):
    print("===========================")
    print("Calibration Meta Data")   

    pattern = re.compile(r'SR(\d+)_cc_(\d{4})(\d{2})(\d{2})_OOIIrrad\.CAL')

    # Use the pattern to search for matches in the formatted string
    match = pattern.search(fileIn)

    if match:
        serial_number = match.group(1)
        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))

        print("Serial Number:", serial_number)
        print("Year:", year)
        print("Month:", month)
        print("Day:", day)
        calibrationDate =  "CD"+ "_" + str(year)+ "_" + str(month)+ "_" + str(day)
        return calibrationDate;

    else:
        time.sleep(5)
        print("No match found.")
        sys.exit()  
        return;


def getAbsouluteIrradiance(device,
                            illuminatedSpectrum,\
                                darkSpectra,\
                                    calibrationData,\
                                        unitTransformDenomenator,
                                            waveLengthSpread):
    

    zeroCorrectedSpectrum   = zeroCorrection(\
                                device.nonlinearity_correct_spectrum2(\
                                    darkSpectra,\
                                        illuminatedSpectrum\
                                            ))
        
    energyInMicroJoules     = multiplyLists(\
                                zeroCorrectedSpectrum,\
                                    calibrationData\
                                        )

    energyInMicroJoulesPerAreaPerSec\
                            = [x / (unitTransformDenomenator) for x in energyInMicroJoules]
        
    energyInMicroJoulesPerAreaPerSecPerNanoMeter\
                            = divideLists(\
                                energyInMicroJoulesPerAreaPerSec,\
                                    waveLengthSpread)

    return energyInMicroJoulesPerAreaPerSecPerNanoMeter,zeroCorrectedSpectrum;
        


def getAbsouluteIrradianceIC(device,
                            illuminatedSpectrum,\
                                    calibrationData,\
                                        unitTransformDenomenator,
                                            waveLengthSpread):
    
    zeroCorrectedSpectrumIC   = zeroCorrection(illuminatedSpectrum)
        
    energyInMicroJoules     = multiplyLists(\
                                zeroCorrectedSpectrumIC,\
                                    calibrationData\
                                        )

    energyInMicroJoulesPerAreaPerSec\
                            = [x / (unitTransformDenomenator) for x in energyInMicroJoules]
        
    energyInMicroJoulesPerAreaPerSecPerNanoMeterIC\
                            = divideLists(\
                                energyInMicroJoulesPerAreaPerSec,\
                                    waveLengthSpread)

    return energyInMicroJoulesPerAreaPerSecPerNanoMeterIC,zeroCorrectedSpectrumIC;



def publishSR200544RC(dateTime,\
                        waveLengths,\
                            counts,\
                                integrationTimeMicroSec,\
                                    scansToAverage,\
                                        boxCarWidth):
    print("===========================")
    print("Publish SR200544RC - Raw Counts")   

    if(len(waveLengths) == len(counts)):
        sensorDictionary = OrderedDict([
            ("dateTime"                  ,str(dateTime)),
           	("integrationTimeMicroSec"   ,integrationTimeMicroSec),
           	("scansToAverage"            ,scansToAverage),
           	("boxCarWidth"               ,boxCarWidth),
        ])
        for key, value in zip(waveLengths, counts):
            sensorDictionary[str(key)] = value        

        # print(sensorDictionary)
        mSR.sensorFinisher(dateTime,"SR200544RC",sensorDictionary)        
        return;
                
 
                
def publishSR200544(dateTime,\
                        waveLengths,\
                            energy,\
                                integrationTimeMicroSec,\
                                    scansToAverage,\
                                        boxCarWidth,\
                                            calibrationDate,\
                                                darkSpectraTime,\
                                                    sensorID):
    
    print("===========================")
    print("Publish SR200544AI - Absolute Irradiance")   

    if(len(waveLengths) == len(energy)):
        sensorDictionary = OrderedDict([
            ("dateTime"                  ,str(dateTime)),
           	("integrationTimeMicroSec"   ,integrationTimeMicroSec),
           	("scansToAverage"            ,scansToAverage),
           	("boxCarWidth"               ,boxCarWidth),               
           	("calibrationDate"           ,calibrationDate),
            ("darkSpectraTime"           ,darkSpectraTime),
        ])

        for key, value in zip(waveLengths, energy):
            sensorDictionary[str(key)] = value        
        # print(sensorDictionary)
        mSR.sensorFinisher(dateTime,sensorID,sensorDictionary)
        return;



def obtainDarkSpectrums(device,\
                            dateTime,
                                integrationTimeMicroSec):
    # dateTime     = datetime.now(timezone.utc)
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


# def getStringTitle(serialNumber, preTitle,\
#                 electricDarkCorrelationUsage,\
#                     nonLinearityCorrectionUsage,\
#                         integrationTimeMicroSec,\
#                             dateTime):
    
#     titleStr = preTitle + " for SN: " + str(serialNumber) \
#                   + " ,EDCU: " + str(electricDarkCorrelationUsage)\
#                   + " ,NLCU: " + str(nonLinearityCorrectionUsage)\
#                   + " ,IT: " + str(integrationTimeMicroSec/1000000) +" s"\
#                   + " ,Date Time: " + str(dateTime) 

#     return titleStr,titleStr.replace(" ","_").replace(",","_").replace(".","_");


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


    # Acquire Spectrum at 00 --------------
    preTitle = "AS 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    illuminatedSpectrum                  = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,illuminatedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)  



   # 00 --------------
    preTitle = "AS DC 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.dark_correct_spectrum2(darkSpectrum,illuminatedSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   


   # 00 --------------
    preTitle = "AS DC NLC 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.nonlinearity_correct_spectrum2(darkSpectrum,illuminatedSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    return zeroCorrection(formattedSpectrum);



def getCorrectedSpectra(device,\
                        integrationTimeMicroSec,\
                            serialNumber,\
                                waveLengths,\
                                    darkSpectrumFile):

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


    # Acquire Spectrum at 00 --------------
    preTitle = "AS 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    illuminatedSpectrum                  = device.get_formatted_spectrum()
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,illuminatedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)  



   # 00 --------------
    preTitle = "AS DC 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.dark_correct_spectrum2(darkSpectrum,illuminatedSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   


   # 00 --------------
    preTitle = "AS DC NLC 00"
    electricDarkCorrelationUsage =  False
    nonLinearityCorrectionUsage  =  False
    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        )
    time.sleep(1)

    formattedSpectrum                   = device.nonlinearity_correct_spectrum2(darkSpectrum,illuminatedSpectrum)
    labelSpaced, labelNoSpaces = \
                getStringTitle(serialNumber, preTitle,\
                    electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                            integrationTimeMicroSec,\
                                dateTime)
    
    plotter(waveLengths,formattedSpectrum,\
                labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

    return zeroCorrection(formattedSpectrum);







# def collectCalibrationData(integrationTimeMicroSec,serialNumber,waveLengths,calibrationFile):
    
#     dateTime     = datetime.now(timezone.utc)
#     print("Collecting an Ambient Spectrum")
    
#     calibrationData = []
#     with open(calibrationFile, 'r') as file:
#         # Skip the first 7 lines (header information)
#         for _ in range(9):
#             next(file)

#         # Read the remaining lines and convert them to floats
#         for line in file:
#             # print(line.strip())
#             float_value = float(line.strip())
#             calibrationData.append(float_value)
    
    

#     print(len(calibrationData))
    
#     preTitle = "Callibration Data"
#     electricDarkCorrelationUsage =  False
#     nonLinearityCorrectionUsage  =  False

#     time.sleep(1)

#     labelSpaced, labelNoSpaces = \
#                 getStringTitle(serialNumber, preTitle,\
#                     electricDarkCorrelationUsage,\
#                         nonLinearityCorrectionUsage,\
#                             integrationTimeMicroSec,\
#                                 dateTime)

#     plotter(waveLengths,calibrationData,\
#                 labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   
#     return calibrationData;


def zeroCorrection(inputList):
    return [max(0.0, value) for value in inputList]


def multiplyLists(list1, list2):
    return [a * b for a, b in zip(list1, list2)]

def divideLists(list1, list2):
    return [a / b for a, b in zip(list1, list2)]

def calculateCirceArea(radius):
     return  math.pi * (radius**2)
        
def squareMicroMetersToSquareCentimeters(valueIn):
    return valueIn / 1e8



def calculateBinSize(floatList):
    n = len(floatList)
    bin_sizes = [floatList[1] - floatList[0]]  # Assuming bin size for the first element is 0

    for P in range(1, n - 1):
        dL = (floatList[P + 1] - floatList[P - 1]) / 2
        bin_sizes.append(dL)

    bin_sizes.append(floatList[-1] - floatList[-2])  # Assuming bin size for the last element is 0

    return bin_sizes


def max_count_collector(device,electricDarkCorrelationUsage,nonLinearityCorrectionUsage,scansToAverage,boxCarWidth):
    result_df = pd.DataFrame(columns=['Integration Time', 'Maximum'])
    # for integrationTimeMicroSec in range(500000, 6000001, 500000):
    for integrationTimeMicroSec in range(500000, 2500001, 500000):
        setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        scansToAverage,\
                        boxCarWidth,\
                        )
        illuminated_spectrum = device.get_formatted_spectrum()
        maximum = max(illuminated_spectrum)
 
        #result_df = pd.concatresult_df.append({'Integration Time': boxCarWidth, 'Maximum': maximum}, ignore_index=True)
        result_df = pd.concat([result_df, pd.DataFrame([[integrationTimeMicroSec, maximum]],\
                   columns=['Integration Time', 'Maximum'])], sort=False)
        print(result_df)
    # Find the maximum value closest to 75% of max cap
    closest_to_75_percent = result_df.iloc[(result_df['Maximum'] - 0.75 * max_cap).abs().argsort()[0]]
    print("Collecting Integration Time:")
    print(str(closest_to_75_percent['Integration Time'].iloc[0].values))
    # print(closest_to_75_percent['Integration Time'])
    # print(closest_to_75_percent['Integration Time'][0])
    # print(closest_to_75_percent['Integration Time'][1])
    return closest_to_75_percent['Integration Time'].iloc[0].values
 


def adaptive_integration_time(max_list,device,integrationTimeMicroSec):

    # Convert the list to numpy array
    max_array = np.array(max_list)
    
    # Calculate the 25th and 75th quantiles
    quantile_25 = np.quantile(max_array, 0.25)
    quantile_75 = np.quantile(max_array, 0.75)
    
    # Extract values within the 25th and 75th quantiles
    extracted_values = max_array[(max_array >= quantile_25) & (max_array <= quantile_75)]
    
    # Calculate the average of the extracted values
    average = np.mean(extracted_values)
    
    # Compare the average value to the max cap
    if 0.6 * max_cap <= average <= 0.9 * max_cap:
        device.set_integration_time(integrationTimeMicroSec)# Keep integration_time the same
    else:
        device.set_integration_time(max_count_collector(device))



def saveToPickle(floatList, integrationTimeMicroSec, directory):
    try:
        # Create a directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Construct the filename based on integration time
        fileName = os.path.join(directory, f'dark_spectrum_{integrationTimeMicroSec}.pkl')
        
        with open(fileName, 'wb') as file:
            pickle.dump(floatList, file)
    except Exception as e:
        print(f"An error occurred: {e}")



def storeDarkSpecta(
        device,\
            dateTime,\
                electricDarkCorrelationUsage,\
                    nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                            scansToAverage,\
                                boxCarWidth,\
                        ):
    print("===========================")
    print("Obtaining Dark Spectrum for integration time :" + str(integrationTimeMicroSec))
    time.sleep(1)
    waveLengths                = device.get_wavelengths()
    time.sleep(1)
    serialNumber               = device.get_serial_number()
    time.sleep(1)   

    setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        scansToAverage,\
                        boxCarWidth 
                        )
    time.sleep(1)
    
    formattedSpectrum                   = device.get_formatted_spectrum()
    
    
    saveToPickle(formattedSpectrum,integrationTimeMicroSec,'Dark_Spectra')        


    # # 00 --------------
    # preTitle = "DC 00"
    # electricDarkCorrelationUsage =  False
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

    # # 00 --------------
    # preTitle = "DC + NL 00"
    # electricDarkCorrelationUsage =  False
    # nonLinearityCorrectionUsage  =  False
    # setUpDevice(device,\
    #                     electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                     integrationTimeMicroSec,\
    #                     )
    # time.sleep(1)

    # formattedSpectrum                   = device.get_nonlinearity_corrected_spectrum1(darkSpectrum)
    # labelSpaced, labelNoSpaces = \
    #             getStringTitle(serialNumber, preTitle,\
    #                 electricDarkCorrelationUsage,\
    #                     nonLinearityCorrectionUsage,\
    #                         integrationTimeMicroSec,\
    #                             dateTime)
    
    # plotter(waveLengths,formattedSpectrum,\
    #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces) 



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

