#!/usr/bin/python3
# -*- coding:utf-8 _*-
import sys
import time

import serial

from lib import util

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(1)

# 切换到主动上传模式
ENABLE_AUTO_SUBMIT = b"\xFF\x01\x78\x40\x00\x00\x00\x00\x47"
# 关闭主动上传模式
DISABLE_AUTO_SUBMIT = b"\xFF\x01\x78\x41\x00\x00\x00\x00\x46"
# 问答模式，读浓度
QUERY_CONCENTRATION = b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79"


def get_concentration(passive=False):
    model = ENABLE_AUTO_SUBMIT
    if passive:
        model = DISABLE_AUTO_SUBMIT
    ser.write(model)
    while True:
        # ser.write(bytes.fromhex('ff 01 78 00 00 00 00 00 87'))
        time.sleep(1)
        response = ser.read(9)
        i = 0
        while i < len(response):
            print("%d: %x" % (i, response[i]))
            i += 1
        checksum = util.calculate_checksum(response)
        print("response: %s, checksum: %d, checkbit: %d" % (response, checksum, response[8]))
        if response[0] == 0xFF and response[1] == 0x17:
            high_byte = response[4]
            low_byte = response[5]
            concentration = ((high_byte << 8) + low_byte) / 1000.0
            # ch2o_ppm = (high_byte << 8) | low_byte
            print("Formaldehyde concentration: %.3f ppm" % concentration)
        else:
            print("error")


if __name__ == '__main__':
    passive = False
    if len(sys.argv) > 1:
        passive = True

    get_concentration(passive)
