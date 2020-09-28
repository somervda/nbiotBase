#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import machine
import math
import network
import os
import time
import utime
import gc
import pycom
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack
import struct


def blink(seconds, rgb):
    # print("blink", rgb)
    pycom.rgbled(rgb)
    time.sleep(seconds/2)
    pycom.rgbled(0x000000)  # off
    time.sleep(seconds/2)


def most_common_coord(coord_dict):
    if len(coord_dict) == 0:
        return (None, None)
    else:
        max_coord_count = 0
        max_coord = (None, None)
        for coord_item in coord_dict.items():
            if coord_item[1] > max_coord_count:
                print("new max_coord:", coord_item[0])
                max_coord = coord_item[0]
                max_coord_count = coord_item[1]
        print("max_coord:", max_coord)
        return max_coord


def getGPS(py, max_samples):
    """ Get GPS lng/lat by performing multiple GPS collections and then
    returning the most often seen results , after power on this can take a while
    but once coordinates stabilize the results will be returned """
    early_end_count = 10

    # Create a dictionary of coords and count
    coord_dict = {}
    gc.enable()

    # setup rtc
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(750)
    # print('\nRTC Set from NTP to UTC:', rtc.now())
    utime.timezone(7200)
    # print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

    l76 = L76GNSS(py, timeout=30)
    valid_coord_count = 0

    print("getGPS: ", end="")

    for sample_number in range(max_samples):
        # time.sleep(1)

        coord = l76.coordinates()
        if coord[0] is None or coord[1] is None:
            blink(1, 0xff0000)  # red
            print(".", end='')
        else:
            blink(1, 0x00ff00)  # green
            print("^", end='')
            valid_coord_count += 1
            if coord in coord_dict:
                coord_dict[coord] += 1
            else:
                coord_dict[coord] = 1
        # print("coord_dict", coord_dict)
        # print("{} - {}".format(coord, sample_number))
        # End early if we have enough coord samples
        if valid_coord_count > early_end_count:
            print(" ")
            return most_common_coord(coord_dict)
    print(" ")
    return most_common_coord(coord_dict)


class GPS_Payload:
    """ Class for managing the GPS payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    longitude = 0.0
    latitude = 0.0
    pack_format = "ff"

    def __init__(self, longitude, latitude):
        if longitude is not None and latitude is not None:
            self.longitude = longitude  # Float
            self.latitude = latitude  # Float

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    # Noter: use single precision float f for GPS Lng/Lat to get locations down to a meter
    def pack(self):
        return struct.pack(self.pack_format, self.longitude, self.latitude)

    def calcsize(self):
        return struct.calcsize(self.pack_format)
