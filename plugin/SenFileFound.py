#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import requests

from module.log import logger

description = 'Sensitive Directory/File Scan By dict AUTO'
type = 'route'

class poc(object):
    
    def __init__(self, v):
    
        self.error404 = None
        self.logger = logger(v)
    
    def __fileDic(self, target):
        
        dic = list()
        f =  open('data/dict.txt', 'r')
        dic = f.readlines().strip()
        
        return dic
        
    def exploit(self, target):
        
        #status404,statusWaf,customPage = checkWebStatus(target)
        pass
        
            

            
        
        
        
        
    
