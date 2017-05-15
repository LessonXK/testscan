#!/usr/bin/env python
#coding:utf8

#__author__ = xiaokong

import requests
import config
from module.log import logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Plugin(object):

    type = 'CMS/OTHER/FRAME/WEB'
    cmsname = 'Please add the CMS name if CMS type'
    querytype = 'site/route/page'
    description = 'Please complete the description'

    def __new__(cls, *args, **kwargs):
        self = super(Plugin, cls).__new__(cls, *args, **kwargs)
        self.log = logger(config.get_config('verbose'), self.__module__)
        return self
    
    def query(self, method, url, data=None, cookie=None,headers={}, params=None, allow_redirects=True):
        """
        query url
        """
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'
        proxies = config.get_config('proxy') if config.get_config('proxy') else None
        if cookie:
            headers['Cookie'] = cookie
        try: 
            self.log.debug(url)
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=method, 
                                url=url, 
                                headers=headers, 
                                proxies=proxies,
                                data=data, 
                                params=params,
                                timeout=30,
                                verify=False,
                                allow_redirects=allow_redirects)
        except Exception as e:
            self.log.error('error: '+str(e))
            return None

        return response
            