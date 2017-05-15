#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin

class poc(Plugin):
    
    type = 'OTHER'
    querytype = 'site'
    description = 'test for file ,not a poc'

    def __init__(self, v):
    
        self.payload = "/Tools/SwfUpload/SwfUploadService.asmx"
        self.userAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'
    
    def exploit(self, target):
        
        self.log.vuln('123')

    

   



