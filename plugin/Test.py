#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import requests
from module.log import logger

description = 'test for file ,not a poc'
type = 'site'

class poc(object):
    
    def __init__(self, v):
    
        self.payload = "/Tools/SwfUpload/SwfUploadService.asmx"
        self.userAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'
        self.logger = logger(v)
    
    def exploit(self, target):
        
        headers = {'User-Agent': self.userAgent}
        try:
            
            res = requests.get(target+self.payload, headers=headers, timeout=30)
            if not res.ok:
                return True
            data = res.content
            if '"SwfUploadService.asmx?WSDL"' in data:
                self.logger.log(41,str([target]))
        except Exception as e:
            self.logger.debug(str(e))
    

   



