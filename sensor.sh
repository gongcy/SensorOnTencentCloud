#!/bin/bash

/home/pi/SensorOnTencentCloud/getdata.py &
sleep 3
/home/pi/SensorOnTencentCloud/flusholed.py
