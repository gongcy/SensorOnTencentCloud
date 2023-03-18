#!/usr/bin/python
# -*- coding:utf-8 _*-
import sys
import time

import serial

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
        is_valid = check_valid(response)
        print(f"response: {response}, is_valid: {is_valid}")
        if response[0] == 0xFF and response[1] == 0x17:
            high_byte = response[4]
            low_byte = response[5]
            concentration = ((high_byte << 8) + low_byte) / 1000.0
            # ch2o_ppm = (high_byte << 8) | low_byte
            print("Formaldehyde concentration: %.3f ppm" % concentration)
        else:
            print("error")


def check_valid(value) -> bool:
    # 校验和 = （取反（Byte1+Byte2+……+Byte7））+ 1
    length = len(value)
    j = 1
    sum = 0
    while j < length - 2:
        sum += value[j]
        j += 1
    check_bit = (~sum) + 1
    if check_bit == value[length - 1]:
        return True
    return False


if __name__ == '__main__':
    passive = False
    if len(sys.argv) > 1:
        passive = True

    get_concentration(passive)
