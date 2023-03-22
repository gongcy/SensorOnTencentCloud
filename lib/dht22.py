# -*- coding:utf-8 _*-
import Adafruit_DHT


def get_dht_data():
    pin = 4
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    return -1, -1
