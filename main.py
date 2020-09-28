import pycom
import lteHelper
import machine
from machine import I2C
import pytrackHelper
from pytrackHelper import GPS_Payload
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
import gc


pycom.heartbeat(False)
#  lteHelper.getVersion()


# Don't use wifi so turn it off to save power
# Turn off accelerometer
py = Pytrack()
acc = LIS2HH12()

# Set deep sleep parameters
py.setup_int_wake_up(True, False)
acc.set_odr(0)
gc.collect()
gps = pytrackHelper.getGPS(py, 300)

bodyData = '{"device_id":"94320", "payload_fields" : {"lat": ' + \
    str(gps[0]) + ',"lng":' + str(gps[1]) + ' }}'

gc.collect()
lteHelper.sendData(bodyData)

py.setup_sleep(600)
print("Sleep..")
py.go_to_sleep(gps=False)
