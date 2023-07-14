#!/usr/bin/python3
# -*- coding:utf-8 _*-
import json
import os
import time
import traceback

from lib import log
from lib import util
from lib.mqtt import Mqtt
from lib.oled import oled

# import commands

# get cachedata
cachefile = util.get_cachepath()
# get wlan ip
# rflag, wlanip_tmp = commands.getstatusoutput("ifconfig wlan0 | grep 'inet ' | awk '{print $2}'")

# wlanip = 'NULL' if 0 != rflag else wlanip_tmp
# oled obj
# oledobj = oled('i2c-128*64')
oledobj = oled('i2c-128*32')
checktime = 0
showdata = []
mqtt_client = Mqtt()

i = 0
while True:
    start_time = time.time()
    showdata = []
    # check modify
    mtime = os.stat(cachefile).st_mtime
    if mtime == checktime:
        # print '%s no change'%cachefile
        continue

    # create oleddata
    with open(cachefile, 'r') as f:
        try:
            tdata = json.load(f)
        except Exception as e:
            error_message = traceback.format_exc()
            log.error(str(e) + '||' + error_message)
            time.sleep(0.1)
            tdata = json.load(f)
        f.close()
    checktime = mtime
    stime = tdata['stime']
    udata = "%.3f" % tdata['udata']
    temp_data = tdata['tdata']
    hdata = tdata['hdata']
    showdata.append(stime)
    showdata.append("CH2O: %s ppm" % udata)
    showdata.append("T: %s°C H: %s%%" % (temp_data, hdata))
    # showdata.append("ip: %s" % wlanip)
    showdata.append('')
    if i % 30 == 0:
        try:
            mqtt_client.send_message(stime, udata, temp_data, hdata)
        except Exception as e:
            error_message = traceback.format_exc()
            log.error(str(e) + '||' + error_message)
    i += 1
    # flush data
    if not oledobj.flush(showdata):
        log.error('Failed to flusholed: %s' % oledobj.get_errorinfi())
    end_time = time.time()
    cost = end_time - start_time
    if cost < 1:
        time.sleep(1 - cost)
