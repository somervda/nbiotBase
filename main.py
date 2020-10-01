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
# gps = pytrackHelper.getGPS(py, 300)
gps = (1, 2)
# bodyData = '{"device_id":"94320", "payload_fields" : {"lat": ' + \
#     str(gps[0]) + ',"lng":' + str(gps[1]) + ' }}'
# bodyData = "'lat': " + str(gps[0]) + ",'lng':" + str(gps[1])
# qt = '\\"'
# bodyData = qt + 'lat' + qt + ':' + \
#     str(gps[0]) + ',' + qt + 'lng' + qt + ':' + \
#     str(gps[1]) + ',' + qt + 'value' + qt + ':' + '47'
dataList = []
dataList.append(("lat", 4))
dataList.append(("lng", 7))
dataList.append(("value", 9))
gc.collect()
lteHelper.sendData(dataList)

# Go into low power sleep
# py.setup_sleep(600)
# print("Sleep..")
# py.go_to_sleep(gps=False)
