#!/usr/bin/python
# -*- coding:utf-8 _*-
import json
import os
import time

import commands

from lib.oled import oled
from lib.public import get_cachepath

# get cachedata
cachefile = get_cachepath()
# get wlan ip
rflag, wlanip_tmp = commands.getstatusoutput("ifconfig wlan0 | grep 'inet ' | awk '{print $2}'")
wlanip = 'NULL' if 0 != rflag else wlanip_tmp
# oled obj
oledobj = oled('i2c-128*32')
checktime = 0
showdata = []
while True:
    time.sleep(1)
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
            print(e)
            time.sleep(0.1)
            tdata = json.load(f)
        f.close()
    checktime = mtime
    showdata.append(tdata['stime'])
    showdata.append("CH₂O: %s ppm" % (tdata['udata'] - 0.03))
    showdata.append("T&H: %s %s" % (tdata['tdata'], tdata['hdata']))
    showdata.append(wlanip)
    showdata.append('')

    # flush data
    if not oledobj.flush(showdata):
        print('Failed to flusholed: %s' % oledobj.get_errorinfo())
