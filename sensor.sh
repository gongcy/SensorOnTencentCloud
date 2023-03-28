#!/bin/bash

sudo /opt/SensorOnTencentCloud/getdata.py &
sleep 3
sudo /opt/SensorOnTencentCloud/flusholed.py
