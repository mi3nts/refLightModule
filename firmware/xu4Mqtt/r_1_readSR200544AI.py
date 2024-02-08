
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

# Collect New Dark Spectra 
# Automate the collection of both 



debug           = False 

devicesPresent  = False
deviceOpen      = False

spectrumPlotter = True

macAddress          = mD.macAddress

electricDarkCorrelationUsage = mD.electricDarkCorrelationUsage
nonLinearityCorrectionUsage  = mD.nonLinearityCorrectionUsage
integrationTimeMicroSec      = mD.integrationTimeMicroSec

scansToAverage               = mD.scansToAverage
boxCarWidth                  = mD.boxCarWidth
fiberDiametorMicroMeter      = mD.fiberDiametorMicroMeter

darkSpectrumFile         = mD.darkSpectrumFile
calibrationFile          = mD.calibrationFile

integrationTimeSec           = integrationTimeMicroSec/1000000


areaInSquareCM           = mO.squareMicroMetersToSquareCentimeters(\
                                mO.calculateCirceArea(\
                                    fiberDiametorMicroMeter/2))

unitTransformDenomenator = (areaInSquareCM*integrationTimeSec)

totalWaitingTime       = 10

if __name__ == "__main__":
    
    print()
    print("============ MINTS Reference Light Module ============")
    print()

    devicesPresent, deviceIDs = mO.checkingDevicePresence()

    if devicesPresent:
        
        print("Ocean Optics Spectrometors found")
        # Only choosing the 1st Device
        deviceID,device             = mO.openDevice(deviceIDs,0)
        serialNumber, waveLengths   = mO.getAllSpectrumDetails(device)   
        waveLengthSpread            = mO.calculateBinSize(waveLengths)
        calibrationData             = mO.loadCalibrationData(calibrationFile)
        darkSpectra                 = mO.loadDarkSpectra(darkSpectrumFile)
        calibrationDate             = mO.getCalibrationMeta(calibrationFile)
        darkSpectraTime             = mO.getDarkSpectaMeta(darkSpectrumFile)

        mO.setUpDevice(device,\
                        electricDarkCorrelationUsage,\
                        nonLinearityCorrectionUsage,\
                        integrationTimeMicroSec,\
                        scansToAverage,\
                        boxCarWidth,\
                        )

        try:
            while True:
                startTime = time.time()
                print()
                print("========================")
                dateTimeRaw           = datetime.now(timezone.utc)
                
                illuminatedSpectrum   = device.get_formatted_spectrum()
                print("Collecttion Time:" + str(dateTimeRaw))
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
                    

                    
         
                elapsedTime = time.time() - startTime
                remainingWaitingTime = totalWaitingTime - elapsedTime

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
        

        