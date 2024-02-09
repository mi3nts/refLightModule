# GUVA-S12SD

import datetime
from datetime import timedelta
import time
import math

from collections import OrderedDict
import datetime
from mintsXU4 import mintsSensorReader as mSR



from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

# Mints Battery level SoLo nodes
class GUVAS12SD:

    def __init__(self, i2c_dev,debugIn, busNum):
        # self.i2c = smbus.SMBus(0)
        # self.address = address
        self.i2c      = i2c_dev
        self.debug    = debugIn     
        # print("Initiating INA219 for GUVAS12SD")
        self.ina    =None
        
        try:
            self.ina   = INA219(SHUNT_OHMS, busnum=busNum)
        
        except Exception as e:
            time.sleep(.5)
            print ("Error and type: %s - %s." % (e,type(e)))
            time.sleep(.5)
            print("INA not found")
            time.sleep(.5)
    
    def initiate(self):
        print("Initializing GUVAS12SD")        
        time.sleep(1)
        try:
            if "Adafruit_GPIO.I2C" in str(self.ina._i2c):
                self.ina.configure()
                # print("Initiated INA for GUVAS12SD")
                return True;

        except Exception as e:
            time.sleep(.5)
            print ("Error and type: %s - %s." % (e,type(e)))
            time.sleep(.5)
            print("INAs not configured")
            time.sleep(.5)
            return False

    def readMqtt(self):
        dateTime  = datetime.datetime.now()
        uv        = self.ina.voltage()

        sensorDictionary =  OrderedDict([
            ("dateTime"     , str(dateTime)), # always the same
            ("uv"           ,uv),
             ])        
        # print(sensorDictionary)
        mSR.sensorFinisher(dateTime,"GUVAS12SD",sensorDictionary)
        time.sleep(1)   
        return;      

    def read(self):
        uv  = self.ina.voltage()
        return [uv];

