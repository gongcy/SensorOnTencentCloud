#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function

import json

from client_package.rest import ApiException

import client_package


def api_request(pdata):
    # create an instance of the API class
    api_instance = client_package.SensorDataApi()
    try:
        # sensor_data
        api_response = api_instance.post_sensor_data(body=json.dumps(pdata))
        return True, api_response
    except ApiException as e:
        return False, "Exception when calling SensorDataApi->post_sensor_data: %s\n" % e


def getindex():
    pdata = {}
    pdata['type'] = 'getindex'
    return api_request(pdata)


def putdata(data):
    pdata = {}
    pdata['type'] = 'putdata'
    pdata['data'] = data

    return api_request(pdata)
