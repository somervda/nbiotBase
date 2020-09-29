import pycom
import lteHelper
import machine
from machine import I2C
import pytrackHelper
from pytrackHelper import GPS_Payload
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
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
bodyData = '{"device_id":"94320", "payload_fields" : {"lat": ' + \
    str(gps[0]) + ',"lng":' + str(gps[1]) + ' }}'

# Send data via LTE
gc.collect()
lteHelper.sendData(bodyData)

# Go into low power sleep
py.setup_sleep(600)
print("Sleep..")
py.go_to_sleep(gps=False)
