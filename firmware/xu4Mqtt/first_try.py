from __future__ import annotations
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
import pandas as pd
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


debug           = False 

devicesPresent  = False
deviceOpen      = False

spectrumPlotter = True

macAddress          = mD.macAddress

#set to false any corrections
electricDarkCorrelationUsage = mD.electricDarkCorrelationUsage
nonLinearityCorrectionUsage  = mD.nonLinearityCorrectionUsage

#set definitions

scansToAverage               = mD.scansToAverage
boxCarWidth                  = mD.boxCarWidth
fiberDiametorMicroMeter      = mD.fiberDiametorMicroMeter

#Define initial dark spectra and calibration file
#darkSpectrumFile         = mD.darkSpectrumFile
calibrationFile          = mD.calibrationFile



areaInSquareCM           = mO.squareMicroMetersToSquareCentimeters(\
                                mO.calculateCirceArea(\
                                    fiberDiametorMicroMeter/2))


totalWaitingTime       = 10

#  At this point this is hardcoded 
darkSpectrumFilePre         = "/home/teamlary/gitHubRepos/refLightModule/firmware/xu4Mqtt/darkSpectrums/Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:"

# Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:2_5_s-_StA:5-_BCW:5-_DT:2024-03-14_18:19:13_385533+00:00.pkl
darkSpectrumFilePost        = "-_StA:5-_BCW:5-_DT:2024-03-14_18:47:29_801698+00:00.pkl"

# 2024-03-14_18:47:29_801698+00:00.pkl

if __name__ == "__main__":
    
    print()
    print("============ MINTS Reference Light Module ============")
    print()

    #Set up device

    devicesPresent, deviceIDs = mO.checkingDevicePresence()
                # Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:0_5_s-_StA:5-_BCW:5-_DT:2024-02-11_02:07:22_203964+00:00.pkl
  # darkSpectrums/Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:2_0_s-_StA:5-_BCW:5-_DT:2024-02-11_01:44:13_906446+00:00.pkl
    if devicesPresent:
        
        print("Ocean Optics Spectrometors found")
        # Only choosing the 1st Device
        deviceID,device             = mO.openDevice(deviceIDs,0)
        serialNumber, waveLengths   = mO.getAllSpectrumDetails(device)   
        waveLengthSpread            = mO.calculateBinSize(waveLengths)
        calibrationData             = mO.loadCalibrationData(calibrationFile)
        #darkSpectra                 = mO.loadDarkSpectra(darkSpectrumFile)
        calibrationDate             = mO.getCalibrationMeta(calibrationFile)
        

        #Choose and set first integration time
        integrationTimeMicroSec     = mO.max_count_collector(device,electricDarkCorrelationUsage,nonLinearityCorrectionUsage,scansToAverage,boxCarWidth)
        integrationTimeSec          = integrationTimeMicroSec/1000000
        print("Integration Time : " + str(integrationTimeSec) + " secs")

        # darkSpectrumFile            = "Dark_Spectra/dark_spectrum_" + str(integrationTimeMicroSec) + ".pkl"
        # darkSpectra                 = mO.loadDarkSpectra(darkSpectrumFile)
        # darkSpectraTime             = mO.getDarkSpectaMeta(darkSpectrumFile)
        
        # print(darkSpectra)
        # print()
        max_list = []
        
        unitTransformDenomenator = (areaInSquareCM*integrationTimeSec)

        mO.setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        scansToAverage,\
                        boxCarWidth,\
                        )

        try:
            while True:
                startTime        = time.time()
                startTimeITCheck = time.time()
                print()
                print("========================")
                dateTimeRaw                   = datetime.now(timezone.utc)
                integrationTimeMicroSecString = str(integrationTimeMicroSec/1000000) + " s"
                darkSpectrumFile              = darkSpectrumFilePre + integrationTimeMicroSecString.replace(" ","_").replace(",","-").replace(".","_") +darkSpectrumFilePost 
                print("Dark Spectrum File")
                print(darkSpectrumFile)
                
                darkSpectra                   = mO.loadDarkSpectra(darkSpectrumFile)
                print("Dark Specta:")
                print(darkSpectrumFile)
                

                darkSpectraTime               = mO.getDarkSpectaMeta(darkSpectrumFile)
                print("Dark Spectrum Collection Time")
                print(darkSpectrumFile)


                #Initialize list to store max values to be used for adaptive integration time function


                #Collect spectrum
                illuminatedSpectrum   = device.get_formatted_spectrum()
                print("Collecttion Time:" + str(dateTimeRaw))
                maximum = max(illuminatedSpectrum)
                max_list.append(maximum)
                energyInMicroJoulesPerAreaPerSecPerNanoMeter, zeroCorrectedSpectrum = \
                                    mO.getAbsouluteIrradiance(device,
                                        illuminatedSpectrum,\
                                            darkSpectra,\
                                                calibrationData,\
                                                    unitTransformDenomenator,
                                                        waveLengthSpread\
                                                            )

                
                mO.publishSR200544RC(dateTimeRaw,\
                                        waveLengths,\
                                            illuminatedSpectrum,\
                                                integrationTimeMicroSec,\
                                                    scansToAverage,\
                                                        boxCarWidth)
                
                # Publishing Absolute Irradiance
                time.sleep(.1)
                mO.publishSR200544(dateTimeRaw,\
                                        waveLengths,\
                                            energyInMicroJoulesPerAreaPerSecPerNanoMeter,\
                                                integrationTimeMicroSec,\
                                                    scansToAverage,\
                                                        boxCarWidth,\
                                                            calibrationDate,\
                                                                darkSpectraTime,
                                                                    "SR200544AI")
                if spectrumPlotter:
                    time.sleep(.1)
                    plotTitle = "Illuminated Spectrum Counts for " + str(dateTimeRaw) 
                    mO.plotter(waveLengths,\
                                illuminatedSpectrum,\
                                    "Wave Lengths (nm)",\
                                        "Illuminated Spectrum (counts) ",\
                                            "Illuminated Spectrum collected on " + str(dateTimeRaw) ,\
                                                "/home/teamlary/mintsData/spectrumDiagrams/" + \
                                                    plotTitle.replace(" ","_").replace(",","-").replace(".","_"))


                    time.sleep(.1)
                    plotTitle = "Absolute Irradiance for " + str(dateTimeRaw) 
                    mO.plotter(waveLengths,\
                                energyInMicroJoulesPerAreaPerSecPerNanoMeter,\
                                    "Wave Lengths (nm)",\
                                        "Absolute Irradiance(uJ/(cm2*nm*sec)) ",\
                                            "Absolute Irradiance collected on " + str(dateTimeRaw) ,\
                                                "/home/teamlary/mintsData/spectrumDiagrams/" + \
                                                    plotTitle.replace(" ","_").replace(",","-").replace(".","_"))
                    
                    spectrumPlotter = False

                #Check if integration time is still appropriate, if not, set to new.    
                if (time.time() - startTimeITCheck > 3600):
                    integrationTimeMicroSec = mO.adaptive_integration_time(max_list,device,integrationTimeMicroSec)
                    max_list = [];

                elapsedTime = time.time() - startTime
                remainingWaitingTime = totalWaitingTime - elapsedTime - 0.001053

                # If remaining waiting time is positive, wait for it; otherwise, no additional waiting
                if remainingWaitingTime > 0:
                    time.sleep(remainingWaitingTime)




        except KeyboardInterrupt:
            # Handle a keyboard interrupt (Ctrl+C)
            print("Keyboard interrupt detected. Exiting gracefully.")

            # Perform any necessary cleanup or device closing operations
            mO.closeDevice(deviceID)


    
    else:
        print("No Ocean Optics Spectrometors found")
        