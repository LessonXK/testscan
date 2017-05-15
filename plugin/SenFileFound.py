#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import time
import requests
import urlparse

from module.log import logger

class poc(object):

    type = 'WEB'
    querytype = 'site'
    description = 'Sensitive Directory/File Scan By dict AUTO'

    def __init__(self, v):
    
        self.error404 = None
        self.logger = logger(v)
    
    def __fileDic(self, target):
        
        dic = list()
        try:    
            f =  open('data/dict.txt', 'r')
            dic = f.readlines()
            netloc = urlparse.urlparse(target).netloc
            dic.append('/'+netloc+'.rar')
            dic.append('/'+netloc+'.7z')
            dic.append('/'+netloc+'.zip')
            for name in netloc.split('.'):
                if '/' in name or 'www'==name or 'com'==name:
                    continue
                dic.append('/'+name+'.rar')
                dic.append('/'+name+'.zip')
                dic.append('/'+name+'.7z')
        except IOError as e:
            self.logger.error(str(e))
            return None
        except Exception as e:
            self.logger.error(str(e))
            return None

        return dic
        
    def exploit(self, target):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'}
        try:
            for path in self.__fileDic(target):
                path = path.strip('\r\n')
                r = requests.head(target+path, headers=headers, timeout=10, allow_redirects=False)
                if r.ok and r.status_code == 200:
                    if dict(r.headers).has_key('content-type'):
                        if 'text/html' in r.headers['Content-Type']:
                            continue
                        else:
                            self.logger.log(41,str([target+path]))
                    else:
                        self.logger.warn(str([target]))
        except Exception as e:
            self.logger.error(str(e))
            

            
        
        
        
        
    
