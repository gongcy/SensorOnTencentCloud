#!/bin/bash

/opt/SensorOnTencentCloud/getdata.py &
sleep 3
/opt/SensorOnTencentCloud/flusholed.py
