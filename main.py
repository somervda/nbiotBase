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


pycom.heartbeat(False)
blink(2, 0xffffff)
lte = LTE()
lte.init()
# some carriers have special requirements, check print(lte.send_at_cmd("AT+SQNCTM=?")) to see if your carrier is listed.
# when using verizon, use
# lte.init(carrier=verizon)
# when usint AT&T use,
# lte.init(carrier=at&t)


print("Resetting LTE modem ... ", end="")
lte.send_at_cmd('AT^RESET')
print("Reset OK")
time.sleep(1)
# While the configuration of the CGDCONT register survives resets,
# the other configurations don't. So just set them all up every time.
print("Configuring LTE ", end='')
lte.send_at_cmd('AT+CGDCONT=1,"IP","hologram"')  # Changed this from origninal
print(".", end='')
# changed band from 28 to 4. I dont know what earfcn=9410 is;
lte.send_at_cmd('AT!="RRC::addscanfreq band=4 dl-earfcn=9410"')
print(".", end='')
lte.send_at_cmd


# some carriers do not require an APN
# also, check the band settings with your carrier
lte.attach()
print("attaching..", end='')
while not lte.isattached():
    blink(1, 0x0000ff)  # blue
    print('.', end='')
print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
print("attached!")


lte.connect()
print("connecting [##", end='')
while not lte.isconnected():
    time.sleep(1)
    print('#', end='')
# print(lte.send_at_cmd('AT!="showphy"'))
# print(lte.send_at_cmd('AT!="fsm"'))
print("] connected!")
blink(2, 0x00ff00)  # Green

print(socket.getaddrinfo('ourLora.com', 80))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket connected')
s = ssl.wrap_socket(s)
print('ssl. wrap connected')
s.connect(socket.getaddrinfo('ourLora.com',  443)[0][-1])
print(' connect to iot socket')

message = "POST /mailbox HTTP/1.1\r\n"
body = '{"device":"1234"}'
headers = []
headers.append(("content-length", str(len(body))))
headers.append(("content-type", "application/json"))
headers.append(("user-agent", "LTE"))
headers.append(("host", "ourLora.com"))

for header in headers:
    message += header[0] + ":" + header[1] + "\r\n"

message += "\r\n" + body
print("message", message)
# finalMessage = binascii.hexlify(finalMessage)

print("Send:", s.send(message))
# while True:
#     data = s.recv(100)
#     if data:
#         print(str(data, 'utf8'), end='')
#     else:
#         break
s.close()
print("Socket closed")

# s = socket.socket()
# s.connect(socket.getaddrinfo('ourLora.com', 80)[0][-1])
# s.send({"k": "ABCDWXYZ", "d": "Hello, World!", "t": "TOPIC1"})
# print(s.recv(4096))
# s.close()

lte.deinit()
print("Disconnected")
blink(2, 0xff0000)  # red
# now we can safely machine.deepsleep()
