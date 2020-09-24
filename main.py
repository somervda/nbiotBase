from network import LTE
import time
import socket

lte = LTE()
lte.init()
# some carriers have special requirements, check print(lte.send_at_cmd("AT+SQNCTM=?")) to see if your carrier is listed.
# when using verizon, use
# lte.init(carrier=verizon)
# when usint AT&T use,
# lte.init(carrier=at&t)

# some carriers do not require an APN
# also, check the band settings with your carrier
lte.attach(band=20, apn="your apn")
print("attaching..", end='')
while not lte.isattached()
time.delay(0.25)

print('.', end='')
print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
print("attached!")

lte.connect()
print("connecting [##", end='')
while not lte.isconnected():
    time.sleep(0.25)
    print('#', end='')
    # print(lte.send_at_cmd('AT!="showphy"'))
    print(lte.send_at_cmd('AT!="fsm"'))
print("] connected!")

print(socket.getaddrinfo('pycom.io', 80))
lte.deinit()
# now we can safely machine.deepsleep()
