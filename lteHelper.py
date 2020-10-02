from network import LTE
import time
import socket
import ssl
import pycom
# import binascii


def blink(seconds, rgb):
    # print("blink", rgb)
    pycom.rgbled(rgb)
    time.sleep(seconds/2)
    pycom.rgbled(0x000000)  # off
    time.sleep(seconds/2)


def buildData(dataList):
    # Convert a lists of key value pairs into a string
    dataString = ""
    for data in dataList:
        if (dataString != ""):
            dataString += ","
        dataString += '\\"%s\\":%f' % (data[0], data[1])
    return dataString

# See https://docs.pycom.io/firmwareapi/pycom/network/lte/#lteconnectcid1 and
#  https://docs.pycom.io/tutorials/networks/lte/ for more details


def sendData(dataList, deviceKey):
    # ******************** Hologram endpoint Definition
    HOST = "cloudsocket.hologram.io"
    PORT = 9999
    TOPIC = "SENSOR_DATA"

    blink(1, 0xffffff)  # blink white
    # Set up LTE connection
    lte = LTE()
    lte.init()
    print("Resetting LTE modem ... ", end="")
    lte.send_at_cmd('AT^RESET')
    print("Reset OK")
    time.sleep(1)
    # While the configuration of the CGDCONT register survives resets,
    # the other configurations don't. So just set them all up every time.
    print("Configuring LTE ", end='')
    # Changed this from origninal
    lte.send_at_cmd('AT+CGDCONT=1,"IP","hologram"')
    print(".", end='')
    # changed band from 28 to 4. I dont know what earfcn=9410 is;
    lte.send_at_cmd('AT!="RRC::addscanfreq band=4 dl-earfcn=9410"')
    print(".", end='')
    # lte.send_at_cmd

    # Do the attach (Enable radio functionality and attach to the LTE network authorized by the inserted SIM card)
    lte.attach()
    print("attaching..", end='')
    while not lte.isattached():
        blink(1, 0x0000ff)  # blue
        print('.', end='')
    # print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
    print("attached!")

    # Do the connect (Start a data session and obtain and IP address)
    lte.connect()
    print("connecting [##", end='')
    while not lte.isconnected():
        time.sleep(1)
        print('#', end='')
    print("] connected!")
    blink(1, 0x00ff00)  # Green

    # **** Send data to hologram
    bodyData = buildData(dataList)
    lteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lteSocket.connect(socket.getaddrinfo(HOST,  PORT)[0][-1])
    data = '{"k": "%s", "d": "{%s}", "t": "%s"}' % (
        deviceKey, bodyData, TOPIC)
    print("Send Data:", data)
    lteSocket.send(data)

    # Clean up and close connection
    lteSocket.close()
    lte.deinit()
    print("Disconnected")
    blink(1, 0xff0000)  # red
