
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

debug  = False 

devicesPresent = False
deviceOpen = False

macAddress          = mD.macAddress

electricDarkCorrelationUsage = False
nonLinearityCorrectionUsage  = True
integrationTimeMicroSec      = 1000000 
integrationTimeSec           = integrationTimeMicroSec/1000000
fiberDiametorMicroMeter      = 200

if __name__ == "__main__":
    
    print()
    print("============ MINTS Reference Light Module ============")
    print()

    devicesPresent, deviceIDs = mO.checkingDevicePresence()
    if devicesPresent:
        
        print("Ocean Optics Spectrometors found")
        # Only choosing the 1st Device
        deviceID,device =  mO.openDevice(deviceIDs,0)
        
        time.sleep(1)
        waveLengths                = device.get_wavelengths()
        time.sleep(1)
        serialNumber               = device.get_serial_number()
        time.sleep(1)   

        mO.getAllSpectrumDetails(device)   

        # mO.obtainDarkSpectrums(device,\
        #                             integrationTimeMicroSec)

        # Loading the dark spectrum 
        # darkSpectrumFile = \
        #     "darkSpectrums/Formatted_Spectrum_00_for_SN:_SR200544__EDCU:_False__NLCU:_False__IT:_1_0_s__Date_Time:_2024-02-02_21:05:53_771689+00:00.pkl"
        # calibrationFile = \
        #     "calibrationFiles/SR200544_cc_20230323_OOIIrrad.CAL"

        # waveLengthSpread = mO.calculateBinSize(waveLengths)
        # electricDarkCorrelationUsage =  False
        # nonLinearityCorrectionUsage  =  False

        # dateTime     = datetime.now(timezone.utc)
        # preTitle = "Wavelength Spread"
        # time.sleep(1)

        # labelSpaced, labelNoSpaces = \
        #             mO.getStringTitle(serialNumber, preTitle,\
        #                 electricDarkCorrelationUsage,\
        #                     nonLinearityCorrectionUsage,\
        #                         integrationTimeMicroSec,\
        #                             dateTime)

        # mO.plotter(waveLengths,waveLengthSpread,\
        #             labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   






        dateTime     = datetime.now(timezone.utc)
        formattedSpectrum = \
            mO.getCorrectedSpectrums(device,\
                                     integrationTimeMicroSec,\
                                        serialNumber,\
                                            waveLengths,\
                                                darkSpectrumFile)
        # Later add something that gets the dark spectrum at the start of the code 
        print(len(formattedSpectrum))
        # Apply the calibration

        ## Collecting the calibration file 

        calibrationData = \
                    mO.collectCalibrationData(integrationTimeMicroSec,\
                                                serialNumber,\
                                                    waveLengths,\
                                                        calibrationFile)
            


        # Fiber Diametor --> 200 µm
        # 
        energyInMicroJoules = mO.multiplyLists(formattedSpectrum,calibrationData)

        preTitle = "Energy In Micro Joules"
        time.sleep(1)

        labelSpaced, labelNoSpaces = \
                    mO.getStringTitle(serialNumber, preTitle,\
                        electricDarkCorrelationUsage,\
                            nonLinearityCorrectionUsage,\
                                integrationTimeMicroSec,\
                                    dateTime)

        mO.plotter(waveLengths,energyInMicroJoules,\
                    labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   


        areaInSquareCM = mO.squareMicroMetersToSquareCentimeters(\
                            mO.calculateCirceArea(\
                                fiberDiametorMicroMeter/2))


        unitTransformDenomenator = (areaInSquareCM*integrationTimeSec)

        energyInMicroJoulesPerAreaPerSec\
                       = [x / (unitTransformDenomenator) for x in energyInMicroJoules]
        

        preTitle = "Energy In Micro Joules Per Area Per Time"
        time.sleep(1)

        labelSpaced, labelNoSpaces = \
                    mO.getStringTitle(serialNumber, preTitle,\
                        electricDarkCorrelationUsage,\
                            nonLinearityCorrectionUsage,\
                                integrationTimeMicroSec,\
                                    dateTime)

        mO.plotter(waveLengths,energyInMicroJoulesPerAreaPerSec,\
                    labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   

        energyInMicroJoulesPerAreaPerSecPerNanoMeter\
                       = mO.divideLists(energyInMicroJoulesPerAreaPerSec,waveLengthSpread)
        

        preTitle = "Energy In Micro Joules Per Area Per Time Per Nano Meter"
        time.sleep(1)

        labelSpaced, labelNoSpaces = \
                    mO.getStringTitle(serialNumber, preTitle,\
                        electricDarkCorrelationUsage,\
                            nonLinearityCorrectionUsage,\
                                integrationTimeMicroSec,\
                                    dateTime)

        mO.plotter(waveLengths,energyInMicroJoulesPerAreaPerSec,\
                    labelSpaced,"/home/teamlary/mintsData/spectrumDiagrams/" + labelNoSpaces)   



        # mO.getAllSpectrumDetails(device)   

        # mO.obtainDarkSpectrums(device,\
        #                     integrationTimeMicroSec)




        # waveLengths  = mO.getSpectrumDetails(device)

        # dateTime     = datetime.datetime.now()
        # spectrum     = mO.getSingleSpectrum(device)

        # plt.plot(waveLengths,spectrum)
        # plt.xlabel('Wave Lengths (nm)')
        # plt.ylabel('Energy')
        
        # titleStr = "Serial Number: " + str(serialNumer) \
        #           + " ,Electric Dark Correlation Usage:" + str(electricDarkCorrelationUsage)\
        #           + " ,Non Linearity Correction Usage:" + str(nonLinearityCorrectionUsage)\
        #           + " ,Integration Time:" + str(integrationTimeMicroSec/1000000) +" s"\
        #           + " ,Spectrum read at:" + str(dateTime) 


        # font = {'family' : 'normal',
        #         'weight' : 'bold',
        #         'size'   : 5}

        # plt.rc('font', **font)
        # plt.title(titleStr)
        # plt.savefig("/home/teamlary/mintsData/spectrumDiagrams/"+titleStr.replace(" ","")+".png")
        mO.closeDevice(deviceID)
    
    else:
        print("No Ocean Optics Spectrometors found")
        

