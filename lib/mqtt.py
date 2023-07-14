# -*- coding:utf-8 _*-
"""
@summary: mqtt
@author: regangong@tencent.com
@date: 2023/7/10
"""
import json

import paho.mqtt.client as mqtt

from lib import log
from lib import util

# MQTT broker details
mqtt_broker = util.get_config()['mqtt']['broker']
mqtt_port = util.get_config()['mqtt']['port']
mqtt_username = util.get_config()['mqtt']['username']
mqtt_password = util.get_config()['mqtt']['password']
mqtt_topic = "device/dht-ze08/sensor"


def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    log.info(msg.topic + " " + str(msg.payload))


class Mqtt(object):
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.connect(mqtt_broker, mqtt_port)

    def send_message(self, stime, udata, temp_data, hdata):
        msg_body = self.package_param(stime, udata, temp_data, hdata)
        res = self.client.publish(mqtt_topic, msg_body)
        return res

    def package_param(self, stime: str, udata: str, tdata: str, hdata: str):
        return json.dumps({
            'time_str': stime,
            'ch2o': udata,
            'temperature': tdata,
            'humidity': hdata,
        })

    def disconnect(self):
        # Disconnect MQTT client
        self.client.disconnect()
