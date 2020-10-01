from network import LTE
import time
import socket
import ssl
import pycom
import binascii


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


def sendData(dataList):
    blink(2, 0xffffff)
    print("sendData:", dataList, buildData(dataList))
    # Use Hologram setup settings
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
    blink(2, 0x00ff00)  # Green

    # ******************** Hologram endpoint

    HOST = "cloudsocket.hologram.io"
    PORT = 9999
    # generated on hologram's portal for each SIM card.
    DEVICE_KEY = "lQ6Gjc$n"
    TOPIC = "SENSOR_DATA"

    # idx = 0

    # lteSocket = socket.socket()
    # lteSocket.setblocking(True)
    bodyData = buildData(dataList)
    lteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lteSocket.connect(socket.getaddrinfo(HOST,  PORT)[0][-1])
    data = '{"k": "%s", "d": "{%s}", "t": "%s"}' % (
        DEVICE_KEY, bodyData, TOPIC)
    print("Send Data:", data, bytes(data, 'ascii'))
    # lteSocket.send(bytes(data, 'ascii'))
    lteSocket.send(data)
    lteSocket.close()

    # print(lteSocket)
    # dns_records = socket.getaddrinfo(HOST, PORT)
    # print("got dns_records:")
    # print(dns_records)

    # dns_record = dns_records[0][-1]
    # print("DNS Record: {}".format(dns_record))
    # lteSocket.connect(dns_record)
    # print("==== LTE Socket connected")

    # while (idx < 1):

    #     print("@@@@@@@@@@@@@@@@@@@@ Transmission #: {}".format(idx))
    #     # print("Local Time: {}".format(utime.localtime())

    #     message = "Hi"

    #     # for record in dns_records:
    #     try:
    #         data = '{"k": "%s", "d": "%s", "t": "%s"}' % (
    #             DEVICE_KEY, message, TOPIC)
    #         print("Send Data:", data)
    #         lteSocket.send(bytes(data, 'ascii'))
    #         time.sleep(1)

    #         print("==== LTE Socket data sent")
    #         # result = lteSocket.recv(8).decode()
    #         # print("LTE Socket result received: "+result)
    #     except Exception as err1:
    #         try:
    #             print("LTE Socket exception: {}".format(err1))
    #             print("LTE Socket closing...")
    #             lteSocket.close()
    #         except:
    #             pass
    #         print("   "+err1)

    #     idx += 1

    #     time.sleep(5)

    # lteSocket.close()
    # print("LTE Socket closed.")

    # print(socket.getaddrinfo('ourLora.com', 80))

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print('socket connected')
    # s = ssl.wrap_socket(s)
    # print('ssl. wrap connected')
    # s.connect(socket.getaddrinfo('ourLora.com',  443)[0][-1])
    # print(' connect to iot socket')

    # # htp = hypertext transfer protocol - the content of the TCP message being sent
    # # Note: even small IP data requires ~8KB to send data over SSL
    # htp = "POST /mailbox HTTP/1.1\r\n"
    # headers = []
    # headers.append(("content-length", str(len(bodyData))))
    # headers.append(("content-type", "application/json"))
    # headers.append(("user-agent", "LTE"))
    # headers.append(("host", "ourLora.com"))
    # headers.append(("authorization", "Basic b3VyTG9yYTpwYXNzd29yZA=="))

    # for header in headers:
    #     htp += header[0] + ":" + header[1] + "\r\n"

    # htp += "\r\n" + bodyData
    # print("message", htp)

    # print("Send:", s.send(htp))
    # # Don't wait for reply , we don't use it
    # s.close()
    # print("Socket closed")

    lte.deinit()
    print("Disconnected")
    blink(2, 0xff0000)  # red
