import pycom
import lteHelper
import machine
from machine import I2C
import pytrackHelper
from pytrackHelper import GPS_Payload
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
import time
import gc

# ***********************************************************
# Project used to test out LTE communication (LTE-M & NB-IOT)
# ***********************************************************

print("")

pycom.heartbeat(False)
py = Pytrack()
acc = LIS2HH12()

# Set deep sleep parameters
py.setup_int_wake_up(True, False)
# Turn off accelerometer
acc.set_odr(0)

#  Get GPS data from pytrack board
gc.collect()
gps = pytrackHelper.getGPS(py, 300)
dataList = []
dataList.append(("lat", gps[0]))
dataList.append(("lng", gps[1]))
dataList.append(("value", 1))
gc.collect()
lteHelper.sendData(dataList, "lQ6Gjc$n")

# Go into low power sleep
print("Sleep..")
time.sleep(1)
py.setup_sleep(600)
py.go_to_sleep(gps=False)
