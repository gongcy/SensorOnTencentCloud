#!/usr/bin/python
# -*- coding:utf-8 _*-
import json
import sqlite3
import time

import serial

from lib import dht22
from lib import util


def updatedata(udata, tdata, hdata):
    # get time
    utime = int(time.time())
    stime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utime))

    # get data.dict
    ddata = {
        "utime": utime,
        "stime": stime,
        "udata": round(udata, 3),
        "tdata": round(tdata, 1),
        "hdata": round(hdata, 1),
    }

    # format data
    cache = json.dumps(ddata)  # "{utime}	{stime}	{udata}".format(**ddata)
    dbsql = "insert into sensordata (utime, udata, tdata, hdata) " \
            "values ('{utime}','{udata}','{tdata}','{hdata}')".format(**ddata)

    # get config
    cfile = util.get_cachepath()
    dbfile = util.get_dbpath()

    # flush cache
    f = open(cfile, "w")
    f.write(cache)
    f.close()

    # insert db
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute(dbsql)
    conn.commit()
    conn.close()

    return True


# 切换到主动上传模式
ENABLE_AUTO_SUBMIT = b"\xFF\x01\x78\x40\x00\x00\x00\x00\x47"
# 关闭主动上传模式
DISABLE_AUTO_SUBMIT = b"\xFF\x01\x78\x41\x00\x00\x00\x00\x46"
# 问答模式，读浓度
QUERY_CONCENTRATION = b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79"

ser = serial.Serial("/dev/serial0", 9600)
ser.write(ENABLE_AUTO_SUBMIT)
while True:
    start_time = time.time()
    tdata, hdata = dht22.get_dht_data()
    response = ser.read(9)
    # checksum = util.calculate_checksum(response)
    # print("response: %s, checksum: %d, checkbit: %d" % (response, checksum, response[8]))
    if response[0] == 0xFF and response[1] == 0x17:
        high_byte = response[4]
        low_byte = response[5]
        concentration = ((high_byte << 8) + low_byte) / 1000.0
        # ch2o_ppm = (high_byte << 8) | low_byte
        # print("Formaldehyde concentration: %.3f ppm" % concentration)
        updatedata(concentration, tdata, hdata)
    else:
        print(f"error start, response={response}")
        continue
    end_time = time.time()
    cost = end_time - start_time
    time.sleep(1 - cost)
