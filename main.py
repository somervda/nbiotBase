import pycom
import lteHelper
import machine
import pytrackHelper
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
import time
import gc

# ***********************************************************
# Project used to test out LTE communication (LTE-M & NB-IOT)
# ***********************************************************
pycom.heartbeat(False)
py = Pytrack()
acc = LIS2HH12()

print("")
DEEP_SLEEP_SECONDS = 600


# Set deep sleep parameters
py.setup_int_wake_up(True, False)
# Turn off accelerometer
acc.set_odr(0)

#  Get GPS data from pytrack board
gc.collect()
gps = pytrackHelper.getGPS(py, 300)
if (gps[0] is not None and gps[1] is not None):
    # Create a list of key value pairs to be
    # sent by LTE to hologram
    dataList = []
    dataList.append(("lat", gps[0]))
    dataList.append(("lng", gps[1]))
    dataList.append(("value", 1))
    gc.collect()
    # Connect to LTE and send the list of data items and hologram device key
    lteHelper.sendData(dataList, "lQ6Gjc$n")

# Go into low power sleep
print("Deep sleep for %d seconds..." % (DEEP_SLEEP_SECONDS))
time.sleep(1)
py.setup_sleep(DEEP_SLEEP_SECONDS)
py.go_to_sleep(gps=False)
