# -*- coding:utf-8 _*-
import adafruit_dht
from board import D4

# See: https://github.com/adafruit/Adafruit_CircuitPython_DHT

dht_device = adafruit_dht.DHT22(D4)


def get_dht_data():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if humidity is not None and temperature is not None:
            return temperature, humidity
        return -1, -1
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        raise error
