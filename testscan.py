
#!/usr/bin/env python
#coding:utf8

#author : xiaokong

import sys
import os
import urlparse
import argparse
from argparse import RawTextHelpFormatter
from multiprocessing.dummy import Pool
from module.log import logger

class PocScan(object):
    """
    poc scan test
    """
    def __init__(self, plugins, v):

        self.func = list()
        for plugin in plugins:

            pluginpath = 'plugin.{plugin}'.format(plugin=plugin)

            try:
                __import__(pluginpath)
                func = sys.modules[pluginpath].poc(v)
                func.__name__ = plugin
                self.func.append(func)
            except ImportError as err:
                print str(err)

    def start(self, urls, threadnum=20):
        """
        exploit for vul
        :param urls: url
        :param threadnum: thread number
        :return:
        """
        for func in self.func:
            pool = Pool(threadnum)
            pool.map(func.exploit, urls)
            pool.close()
            pool.join()

def queryfile():
    """
    query plugin file
    :parma:
    :return:
    """
    filename = dict()
    pluginmax = 0
    descmax = 0

    path = os.path.realpath(os.path.abspath('plugin'))
    if path not in sys.path:
        sys.path.append(path)
    #query file
    for i in os.listdir(path):
        if i.endswith('.py'):
            pluginname = i[:-3]
            if pluginname == '__init__':
                continue
            if len(pluginname) > pluginmax:
                pluginmax = len(pluginname)
            try:
                pluginpath = 'plugin.%s' % pluginname
                __import__(pluginpath)
                description = sys.modules[pluginpath].description
            except Exception as err:
                parser.error('Plugin .py class is error: %s ' % str(err))
                continue

            if len(description) > descmax:
                descmax = len(description)

            filename[pluginname] = description

    return filename, pluginmax, descmax

#list plugin
class ListPlugins(argparse.Action):
    """
    list plugin for .py
    """
    def __call__(self, parsers, namespace, values, option_string=None):

        try:
            filename, pluginmax, descmax = queryfile()   
            print('The number of plugins : %d' % len(filename))
            #list
            print('+--+'+'-'*(pluginmax+1)+'+'+'-'*(descmax+1)+'+')  
            print('|id|'+' plugin'+' '*(pluginmax-6)+'|'+' description'+' '*(descmax-11)+'|')
            print('+--+'+'-'*(pluginmax+1)+'+'+'-'*(descmax+1)+'+')
            for i,plugin in enumerate(filename.keys()):
                temp = '|'+' '*(2-len(str(i)))+'%d|'+' %s'+' '*(pluginmax-len(plugin))+'|'+' %s'+' '*(descmax-len(filename[plugin]))+'|'
                print(temp % (i, plugin, filename[plugin]))
            print('+--+'+'-'*(pluginmax+1)+'+'+'-'*(descmax+1)+'+')    
        except Exception as e:
            parsers.error('List Plugins is error: %s ' % str(e))

        setattr(namespace, self.dest, True)

#transfer number to pluginname
class NumToExploit(argparse.Action):
    """
    number of plugin tranfer to name of plugin
    """
    def __call__(self, parser, namespace, values, option_string=None):

        try:
            exploit = list()
            filename, pluginmax, descmax = queryfile()
            tmp = filename.keys()
            for i in values:
                exploit.append(tmp[i])
        except Exception as err:
            parser.error('Select Plugin is error: %s ' % str(err))

        setattr(namespace, self.dest, exploit)

def main():

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
    parser.add_argument('-v', dest='verbose', default=1, type=int, choices=[1,2,3,4], help='verbose level')
    parser.add_argument('--exploit', dest='exploit', action='store_true', help='exploit')

    p = parser.parse_args()

    if p.list:
        sys.exit(0)
    elif p.target:
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            pocscan = PocScan(p.plugin, p.verbose)
            pocscan.start([p.target])
    elif p.file:
        targets = list()
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            pocscan = PocScan(p.plugin, p.verbose)
            for target in p.file.readlines():
                targets.append(target.strip('\r\n'))
            pocscan.start(targets)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
