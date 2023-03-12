# -*- coding:utf-8 _*-
import Adafruit_DHT


def get_dht_data():
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)
    if humidity is not None and temperature is not None:
        return str(format(temperature, ".1f")) + '°C', str(format(humidity, ".1f")) + '%'
    return -1, -1
