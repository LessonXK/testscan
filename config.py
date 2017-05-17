#!/usr/bin/env python
#coding:utf8

config ={
    'proxy': None,
    'verbose': None,
    'timeout': 30,
    'pause': None
}

def get_config(key):
    global config
    return config[key]

def set_config(key, value):
    global config
    config[key] = value