#!/usr/bin/env python
#- * - coding:utf-8 - * -

import logging
import sys
from logging.handlers import RotatingFileHandler

'''
class colorLoggingHandler(ColorizingStreamHandler):
    
    level_map = {
      logging.DEBUG: (None, 'cyan', False),
      logging.INFO: (None, 'white', False),
      logging.WARNING: (None, 'yellow', True),
      logging.ERROR: (None, 'red', True),
      logging.CRITICAL: ('red', 'white', True),
    }
'''   

class logger(object):

    def __init__(self, verbose, module=None):
        self.module = module
        logging.addLevelName(51, 'VUL')
        self.logger = logging.getLogger('testscan')
        try:
            from logutils.colorize import ColorizingStreamHandler
            handler = ColorizingStreamHandler(sys.stdout)
            handler.level_map[logging.getLevelName('VUL')] = (None, 'red', True)
            handler.level_map[logging.INFO] = (None, 'white', False)
        except ImportError:
            handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter("[%(funcName)s] %(message)s", "%Y-%m-%d %H:%M:%S") 
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(verbose*10)

    def debug(self, message):
        self.logger.debug('['+self.module+'] '+message)

    def info(self, message):
        self.logger.info('['+self.module+'] '+message)

    def error(self, message):
        self.logger.error('['+self.module+'] '+message)

    def vuln(self, message):
        self.logger.log(51, '['+self.module+'] '+message)

        


    