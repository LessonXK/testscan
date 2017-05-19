#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import urlparse
from module.plugin import Plugin


class poc(Plugin):

    type = 'WEB'
    querytype = 'route'
    description = 'Sensitive Directory/File Scan By dict AUTO'

    def __init__(self):
    
        self.error404 = None
    
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
            self.log.error(str(e))
            return None
        except Exception as e:
            self.log.error(str(e))
            return None

        return dic
        
    def exploit(self, target):

        try:
            for path in self.__fileDic(target):
                path = path.strip('\r\n')
                response = self.query(method='HEAD', url=target+path, allow_redirects=False)
                if response is not None:
                    if response.ok and response.status_code == 200:
                        if dict(response.headers).has_key('content-type'):
                            if 'text/html' in response.headers['Content-Type']:
                                continue
                            else:
                                self.log.vuln(str([target+path]))
                        else:
                            self.log.debug(str([target]))
        except Exception as e:
            self.log.error(str(e))
            

            
        
        
        
        
    
