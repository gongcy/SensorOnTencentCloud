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
mqtt_username = util.get_config()['mqtt']['username']
mqtt_password = util.get_config()['mqtt']['password']
mqtt_topic = "device/dht-ze08/sensor"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


class Mqtt(object):
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.connect(mqtt_broker, mqtt_port)

    def send_message(self, msg_body: str):
        res = self.client.publish(mqtt_topic, msg_body)
        return res

    def disconnect(self):
        # Disconnect MQTT client
        self.client.disconnect()
