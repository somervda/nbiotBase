import pycom
import lteHelper
from network import WLAN


pycom.heartbeat(False)
print("LTE Modem Software Version: ", lteHelper.getVersion())


# Don't use wifi so turn it off to save power
wlan = WLAN()
wlan.deinit()

lteHelper.sendData('{"device_id":"94320"}')
