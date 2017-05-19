
#!/usr/bin/env python
#coding:utf8

#author : xiaokong

import sys
import os
import urlparse
import argparse
import config
import ipaddr
import time
from argparse import RawTextHelpFormatter
from multiprocessing.dummy import Pool

class PocScan(object):
    """
    poc scan test
    """
    def __init__(self, plugins):

        self.func = list()
        for plugin in plugins:

            pluginpath = 'plugin.{plugin}'.format(plugin=plugin)

            try:
                __import__(pluginpath)
                func = sys.modules[pluginpath].poc()
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
        s1 = time.time()
        try:
            pool = Pool(threadnum)
            for func in self.func:
                result = pool.map_async(func.exploit, urls)#.get(9999999999999999)
                #pool.map(func.exploit, urls)
                pool.close()
               
                while True:
                    try:
                        result.successful()
                        break
                    except AssertionError as e:
                        time.sleep(10)
                
        except KeyboardInterrupt as e:
            print 'scan interrup'
        
        print time.time()-s1
def queryfile(status):
    """
    query plugin file
    :parma:
    :return:
    """
    pluginmax = 0
    descmax = 0
    pluginnums = 0
    filename = {
            'WEB': dict(),
            'CMS': dict(),
            'FRAME': dict(),
            'OTHER': dict()
        }

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
                description = sys.modules[pluginpath].poc.description
                plugintype = sys.modules[pluginpath].poc.type
                pluginnums += 1
            except Exception as err:
                print('Plugin .py class is error: %s ' % str(err))
                continue

            if len(description) > descmax:
                descmax = len(description)
            if plugintype == 'WEB':
                filename['WEB'][pluginname] = description
            elif plugintype == 'CMS':
                filename['CMS'][pluginname] = description
            elif plugintype == 'FRAME':
                filename['FRAME'][pluginname] = description
            elif plugintype == 'OTHER':
                filename['OTHER'][pluginname] = description

        if pluginmax < 6:
            pluginmax = 6
        if descmax < 11:
            descmax = 11

    if status:
        return filename, pluginmax, descmax, pluginnums
    else:
        return filename

#list plugin
class ListPlugins(argparse.Action):
    """
    list plugin for .py
    """
    def __call__(self, parsers, namespace, values, option_string=None):
        number = 0
        try:
            filename, pluginmax, descmax, pluginnums = queryfile(True) 
            print('The number of plugins : %d' % pluginnums)
            print('+---+'+'-'*(pluginmax+1)+'+'+'-'*6+'+'+'-'*(descmax+1)+'+')  
            print('|id |'+' plugin'+' '*(pluginmax-6)+'| '+'type'+' |'+' description'+' '*(descmax-11)+'|')
            print('+---+'+'-'*(pluginmax+1)+'+'+'-'*6+'+'+'-'*(descmax+1)+'+')  
            for plugintype, plugindict in filename.items():
                for i,plugin in enumerate(sorted(plugindict.keys())):
                    temp = '|'+' '*(3-len(str(number)))+'%d|'+' %s'+' '*(pluginmax-len(plugin))+'| '+'%s'+' '*(5-len(plugintype))+'|'+' %s'+' '*(descmax-len(plugindict[plugin]))+'|'
                    print(temp % (number, plugin, plugintype, plugindict[plugin]))
                    number += 1
            print('+---+'+'-'*(pluginmax+1)+'+'+'-'*6+'+'+'-'*(descmax+1)+'+')     
        except IOError as e:
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
            tmp = list()
            filename = queryfile(False)
            for plugintype, plugindict in filename.items():
                tmp += sorted(plugindict.keys())
            for i in values:
                exploit.append(tmp[i])
        except Exception as err:
            parser.error('Select Plugin is error: %s ' % str(err))
        
        setattr(namespace, self.dest, exploit)

def main():

    parser = argparse.ArgumentParser(prog='testscan',
                                description ='scan of vul by xiaokong',
                                usage ='testscan.py [options] -u http://www.xxx.com -n 1',
                                formatter_class=RawTextHelpFormatter
                                )
    #use script
    parser.add_argument('-l', dest='list',metavar='num/name', nargs='?', action=ListPlugins, help='List Plugins')
    parser.add_argument('-u', dest='target', help='Target URL or IP Address')
    parser.add_argument('-f', dest='file', type=argparse.FileType('rt'), help='Targets URL From File')
    parser.add_argument('-p', dest='plugin', metavar='name', nargs='+', help='Exploit Plugin By Name')
    parser.add_argument('-n', dest='plugin', metavar='num', type=int, nargs='+',action=NumToExploit, help='Exploit Plugin By Number')
    parser.add_argument('-v', dest='verbose', default=2, type=int, choices=[1,2,3,4], help='verbose level')
    parser.add_argument('--proxy', dest='proxy', help='http agent')
    parser.add_argument('--pause', dest='pause', help='http Request interval')

    p = parser.parse_args()

    config.set_config('verbose', p.verbose)
    if p.proxy:
        config.set_config('proxy', {urlparse.urlparse(p.proxy).scheme:urlparse.urlparse(p.proxy).netloc})
    if p.pause:
        config.set_config('pause', p.pause)
    if p.list:
        sys.exit(0)

    elif p.target:
        try:
            ips = ipaddr.IPv4Network(p.target).iterhosts()
            ip_list = [str(x) for x in ips]
            p.target = ip_list if len(ip_list) else p.target
        except ipaddr.AddressValueError as e:
            pass
            
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            p.target = p.target if isinstance(p.target, list) else [p.target]
            pocscan = PocScan(p.plugin)
            pocscan.start(p.target)
    elif p.file:
        targets = list()
        if not p.plugin:
            parser.error('please input -n or -p')
        else:
            pocscan = PocScan(p.plugin)
            for target in p.file.readlines():
                targets.append(target.strip('\r\n'))
            pocscan.start(targets)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
