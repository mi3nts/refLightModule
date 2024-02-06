
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

debug           = False 

devicesPresent  = False
deviceOpen      = False

spectrumPlotter = True

macAddress          = mD.macAddress

electricDarkCorrelationUsage = False
nonLinearityCorrectionUsage  = False
integrationTimeMicroSec      = 1000000 
integrationTimeSec           = integrationTimeMicroSec/1000000
scansToAverage               = 5
boxCarWidth                  = 5 
fiberDiametorMicroMeter      = 200

darkSpectrumFile         = \
    "darkSpectrums/Dark_Spectra_for_SN:SR200544-_EDCU:False-_NLCU:False-_IT:1_0_s-_StA:5-_BCW:5-_DT:2024-02-05_22:56:38_619126+00:00.pkl"

calibrationFile          = \
    "calibrationFiles/SR200544_cc_20230323_OOIIrrad.CAL"


areaInSquareCM           = mO.squareMicroMetersToSquareCentimeters(\
                                mO.calculateCirceArea(\
                                    fiberDiametorMicroMeter/2))

unitTransformDenomenator = (areaInSquareCM*integrationTimeSec)


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
        
        mO.getAllSpectrumDetails(device)  

        try:
            while True:

                dateTime           = datetime.now(timezone.utc)
                
                illuminatedSpectrum  = device.get_formatted_spectrum()

                mO.publishSR200544RC(dateTime,\
                                        waveLengths,\
                                            illuminatedSpectrum,\
                                                integrationTimeMicroSec,\
                                                    scansToAverage,\
                                                        boxCarWidth)
                


                energyInMicroJoulesPerAreaPerSecPerNanoMeter = \
                                    mO.getAbsouluteIrradiance(device,
                                        illuminatedSpectrum,\
                                            darkSpectra,\
                                                calibrationData,\
                                                    unitTransformDenomenator,
                                                        waveLengthSpread\
                                                            )

                mO.publishSR200544AI(dateTime,\
                                        waveLengths,\
                                            energyInMicroJoulesPerAreaPerSecPerNanoMeter,\
                                                integrationTimeMicroSec,\
                                                    scansToAverage,\
                                                        boxCarWidth,\
                                                            calibrationDate,\
                                                                darkSpectraTime)
                
                if spectrumPlotter:
                    
                    plotTitle = "Illuminated Spectrum Counts for " + str(dateTime) 
                    mO.plotter(waveLengths,\
                                illuminatedSpectrum,\
                                    "Wave Lengths (nm)",\
                                        "Illuminated Spectrum (counts) ",\
                                            "Illuminated Spectrum Collected from " + illuminatedSpectrum ,\
                                                "/home/teamlary/mintsData/spectrumDiagrams/" + \
                                                    plotTitle.replace(" ","_").replace(",","-").replace(".","_"))
                    
                    plotTitle = "Absolute Irradiance for " + str(dateTime) 
                    mO.plotter(waveLengths,\
                                energyInMicroJoulesPerAreaPerSecPerNanoMeter,\
                                    "Wave Lengths (nm)",\
                                        "Absolute Irradiance(uJ/(cm2*nm*sec)) ",\
                                            "Dark Spectra Collected from " + \
                                                energyInMicroJoulesPerAreaPerSecPerNanoMeter ,\
                                                "/home/teamlary/mintsData/spectrumDiagrams/" + \
                                                    plotTitle.replace(" ","_").replace(",","-").replace(".","_"))
                    

                time.sleep(10)

        except KeyboardInterrupt:
            # Handle a keyboard interrupt (Ctrl+C)
            print("Keyboard interrupt detected. Exiting gracefully.")

            # Perform any necessary cleanup or device closing operations
            mO.closeDevice(deviceID)


    
    else:
        print("No Ocean Optics Spectrometors found")
        

        