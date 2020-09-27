import pycom
import lteHelper


pycom.heartbeat(False)
print("LTE Modem Software Version: ", lteHelper.getVersion())
lteHelper.sendData('{"device_id":"1234"}')
