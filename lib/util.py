#!/usr/bin/python
# -*- coding:utf-8 _*-
import json
import os
import sqlite3


def get_config():
    confile = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/data/config.json'
    with open(confile, 'r') as f:
        data = json.load(f)
        return data


def get_dbinitsql():
    sqlfile = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/data/init.sql'
    return open(sqlfile, "r").read()


def get_dbpath():
    sdb = get_config()['sqlite']['dbfile']
    if not os.path.isfile(sdb):
        conn = sqlite3.connect(sdb)
        print("Opened database successfully")
        c = conn.cursor()
        c.execute(get_dbinitsql())
        conn.commit()
        conn.close()
    return sdb


def get_cachepath():
    return get_config()['cache']


def calculate_checksum(data):
    """
    计算数据包的校验和值
    """
    checksum = sum(data[1:-1])
    return (~checksum + 1) & 0xFF
