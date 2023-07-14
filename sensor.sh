#!/bin/bash

log_dir="/var/log/sensor"

if [ ! -d "$log_dir" ]; then
  sudo mkdir -p "$log_dir"
else
  sudo rm -r "$log_dir"/*
fi

sudo rm -rf /dev/shm/sensor.db
sudo rm -rf /dev/shm/sensor.info

sudo /opt/SensorOnTencentCloud/getdata.py &
sleep 5
sudo /opt/SensorOnTencentCloud/flusholed.py
