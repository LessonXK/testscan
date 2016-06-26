import sys
import os

path = os.path.realpath(os.path.abspath('data'))
if path not in sys.path:
    sys.path.append(path)

import urlparse
import argparse
from argparse import RawTextHelpFormatter
from data import AttribDict




def parser_args():

    
    parser = argparse.ArgumentParser(prog='vulscan',
                                description ='scan of vul by xiaokong',
                                usage ='vulscan.py [options]',
                                formatter_class=RawTextHelpFormatter
                                )
    subparser = parser.add_subparsers(help='Which function do you want to use?\n\n', dest='mode')
    script_args = subparser.add_parser('script', help='verify or exploit by script')
    config_args = subparser.add_parser('config', help='verify or exploit by config')

    #use script
    script_args.add_argument('-f', metavar='FILE', help='open file of targets', required=False)
    script_args.add_argument('-u', metavar='URL', help='input a singal target', required=False)
    script_args.add_argument('-s', metavar='SCRIPT', help='input scripts to run', required=False)
    script_args.add_argument('-l', action='store_true', help='list scripts', required=False)
    script_args.add_argument('-t', metavar='TYPE', help='verify or exploit', choices=['verify', 'exploit'], default='verify')
    script_args.add_argument('-n', metavar='NUMBER', default=20, help='number of threads', required=False)

    #use config
    config_args.add_argument('-f', metavar='FILE', help='open file of targets', required=False)
    config_args.add_argument('-u', metavar='URL', help='input a singal target', required=False)
    config_args.add_argument('-c', metavar='config', help='input config to run', required=False)
    config_args.add_argument('-l', metavar='LIST SCRIPT', help='list config', required=False)
    config_args.add_argument('-t', metavar='TYPE', help='verify or exploit', choices=['verify', 'exploit'], default='verify')
    config_args.add_argument('-n', metavar='NUMBER', default=20, help='number of threads', required=False)


    args = parser.parse_args()


    if args.mode == 'script':

        result = AttribDict()
        result.num = args.n
        #result.scirpt = args.s
        result.type = args.t

        data = None
        if args.l:
            path = os.path.realpath(os.path.abspath('plugin'))
            raise Exception(os.listdir(path))
        if not args.f and not args.u:
            raise Exception('error')
        if args.f:
            if not os.path.exists(args.f):
                raise Exception('open file error')
            else:
                f = open(args.f, 'r')
                data = f.readlines()
        result.data = data
        result.url = args.u if not data else None
        return result

    elif args.mode == 'config':
        pass









def main():



    try:
        parser_args()
    except Exception as e:
        print str(e)

if __name__ == '__main__':
    main()
