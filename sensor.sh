#!/bin/bash

sudo rm -rf /dev/shm/sensor.db
sudo rm -rf /dev/shm/sensor.info

sudo /opt/SensorOnTencentCloud/getdata.py &
sleep 5
sudo /opt/SensorOnTencentCloud/flusholed.py
