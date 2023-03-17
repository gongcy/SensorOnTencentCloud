# -*- coding:utf-8 _*-
import time

import serial

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(1)

while True:
    ser.write(b"\xFF\x01\x78\x40\x00\x00\x00\x00\x47")
    # ser.write(bytes.fromhex('ff 01 78 00 00 00 00 00 87'))
    time.sleep(1)
    response = ser.read(9)
    print(f"response: {response}")
    if response[0] == 0xFF and response[1] == 0x17:
        high_byte = response[4]
        low_byte = response[5]
        concentration = ((high_byte << 8) + low_byte) / 1000.0
        # ch2o_ppm = (high_byte << 8) | low_byte
        print("Formaldehyde concentration: %.3f ppm" % concentration)
    else:
        print("error")

    time.sleep(1)
