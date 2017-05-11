#!/usr/bin/env python
#coding:utf8

#author : xiaokong
import sys
import os
'''
path = os.path.realpath(os.path.abspath('data'))
if path not in sys.path:
    sys.path.append(path)
'''
import urlparse
import argparse
from argparse import RawTextHelpFormatter
from multiprocessing.dummy import Pool
from module.log import logger

class pocScan(object):
    """
    poc scan test
    """
    def __init__(self, plugins, v):
        
        self.func = list()
        for plugin in plugins:
        
            pluginPath = 'plugin.{plugin}'.format(plugin=plugin)
            
            try:
                __import__(pluginPath)
                func = sys.modules[pluginPath].poc(v)
                func.__name__ = plugin
                self.func.append(func)
            except ImportError as e:
                print(str(e))
        
    def start(self, target, threadNum=20):
        """
        exploit for vul 
        :param target: url
        :param threadNum: thread number
        :return: 
        """
        for func in self.func:
            pool = Pool(threadNum)
            pool.map(func.exploit, target)
            pool.close()
            pool.join()
        
def queryFile():
    
    filename = dict()
    pluginMax = 0
    descMax = 0
    
    path = os.path.realpath(os.path.abspath('plugin'))
    if path not in sys.path:
        sys.path.append(path)
    #query file
    for i in os.listdir(path):
        if i.endswith('.py'):
            pluginName = i[:-3]
            if pluginName == '__init__':
                continue
            if len(pluginName) > pluginMax:
                pluginMax = len(pluginName)
            try:    
                pluginPath = 'plugin.%s' % pluginName
                __import__(pluginPath)
                description  = sys.modules[pluginPath].description
            except Exception as e:
                parser.error('Plugin .py class is error: %s ' % str(e))
                continue
            
            if len(description) > descMax:
                descMax = len(description)
                
            filename[pluginName] = description    
            
    return filename, pluginMax, descMax
    
#list plugin
class ListPlugins(argparse.Action):
    
    def __call__(self, parser, namespace, values, option_string=None):
        
        try:
            filename, pluginMax, descMax = queryFile()        
            print('The number of plugins : %d' % len(filename))
            #list
            print('+--+'+'-'*(pluginMax+1)+'+'+'-'*(descMax+1)+'+')  
            print('|id|'+' plugin'+' '*(pluginMax-6)+'|'+' description'+' '*(descMax-11)+'|')
            print('+--+'+'-'*(pluginMax+1)+'+'+'-'*(descMax+1)+'+')
            for i,plugin in enumerate(filename.keys()):
                temp = '|'+' '*(2-len(str(i)))+'%d|'+' %s'+' '*(pluginMax-len(plugin))+'|'+' %s'+' '*(descMax-len(filename[plugin]))+'|'
                print(temp % (i, plugin, filename[plugin]))
            print('+--+'+'-'*(pluginMax+1)+'+'+'-'*(descMax+1)+'+')    

                
        except Exception as e:
            parser.error('List Plugins is error: %s ' % str(e))
            
        setattr(namespace, self.dest, True)

#transfer number to pluginName        
class NumToExploit(argparse.Action):
        
    def __call__(self, parser, namespace, values, option_string=None):
    
        try:
            exploit = list()
            filename, pluginMax, descMax = queryFile()
            tmp = filename.keys()          
            for i in values:
                exploit.append(tmp[i])
        except Exception as e:
            parser.error('Select Plugin is error: %s ' % str(e))
                
        setattr(namespace, self.dest, exploit)
    
if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(prog='testscan',
                                description ='scan of vul by xiaokong',
                                usage ='testscan.py [options]',
                                formatter_class=RawTextHelpFormatter
                                )
    #use script
    parser.add_argument('-l', dest='list',metavar='num/name', nargs='?', action=ListPlugins, help='List Plugins')
    parser.add_argument('-u', dest='target', help='Target URL')
    parser.add_argument('-f', dest='file', type=argparse.FileType('rt'), help='Targets URL From File')
    parser.add_argument('-p', dest='plugin', metavar='name', nargs='+', help='Exploit Plugin By Name')
    parser.add_argument('-n', dest='plugin', metavar='num', type=int, nargs='+',action=NumToExploit, help='Exploit Plugin By Number')
    parser.add_argument('-v', dest='verbose', default=1, choices=[1,2,3,4], help='verbose level')
    parser.add_argument('--exploit', dest='exploit', action='store_true', help='exploit')

    p = parser.parse_args()
    
    if p.list:
        sys.exit(0)
    elif p.target:
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            pocScan = pocScan(p.plugin, p.verbose)
            pocScan.start([p.target])
    elif p.file:
        targets = list()
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            pocScan = pocScan(p.plugin, p.verbose)
            for target in p.file.readlines():
                targets.append(target.strip('\r\n'))
            pocScan.start(targets)
    else:
        parser.print_help() 
    





