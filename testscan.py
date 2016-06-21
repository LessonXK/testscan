import requests
import sys
import os
import urlparse
import argparse


def parse_args():

    
    parse = argparse.ArgumentParser(prog='vulscan',
                                description ='scan of vul by xiaokong',
                                usage ='vulscan.py [options]',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                )

    parse.add_argument('-v', action='version', version='%(prog)s 1.0')
    parse.add_argument('-u', help='input singal url', default='')
    parse.add_argument('-n', type=int, help='input number of thread', default=20)
    parse.add_argument('-f', help='input file')

    args = parse.parse_args()






def main():
    pass

if __name__ == '__main__':
    main()
