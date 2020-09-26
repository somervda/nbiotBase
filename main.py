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
    time.sleep(1)
    print('.', end='')
print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
print("attached!")

lte.connect()
print("connecting [##", end='')
while not lte.isconnected():
    time.sleep(1)
    print('#', end='')
    # print(lte.send_at_cmd('AT!="showphy"'))
    print(lte.send_at_cmd('AT!="fsm"'))
print("] connected!")

print(socket.getaddrinfo('ourLora.com', 80))
lte.deinit()
print("Disconnected")
# now we can safely machine.deepsleep()
