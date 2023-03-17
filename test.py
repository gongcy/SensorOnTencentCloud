# -*- coding:utf-8 _*-
import time

import serial

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(1)

while True:
    ser.write(b"\xFF\x01\x78\x00\x00\x00\x00\x00\x88")
    # ser.write(bytes.fromhex('ff 01 78 00 00 00 00 00 87'))
    time.sleep(1)
    response = ser.read(9)

    if response[0] == 0xFF and response[1] == 0x17:
        high_byte = response[2]
        low_byte = response[3]
        concentration = ((high_byte << 8) + low_byte) / 1000.0
        # ch2o_ppm = (high_byte << 8) | low_byte
        print("Formaldehyde concentration: %.3f ppm" % concentration)

    time.sleep(1)