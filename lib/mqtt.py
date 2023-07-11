# -*- coding:utf-8 _*-
"""
@summary: mqtt
@author: regangong@tencent.com
@date: 2023/7/10
"""
import paho.mqtt.client as mqtt

from lib import util

# MQTT broker details
mqtt_broker = util.get_config()['mqtt']['broker']
mqtt_port = util.get_config()['mqtt']['port']
mqtt_topic = "device/dht-ze08/sensor"


class Mqtt:
    def __int__(self):
        self.client = mqtt.Client()
        self.client.connect(mqtt_broker, mqtt_port)

    def send_topic(self, msg_body: str):
        self.client.publish(mqtt_topic, msg_body)

    def disconnect(self):
        # Disconnect MQTT client
        self.client.disconnect()
