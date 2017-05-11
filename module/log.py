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

def logger(v):
    logger = None    
    logging.addLevelName(41, 'VUL')
    logger = logging.getLogger('cmsMap')
    
    try:
        from logutils.colorize import ColorizingStreamHandler
        handler = ColorizingStreamHandler(sys.stdout)
        handler.level_map[logging.getLevelName('VUL')] = (None, 'red', True)
        handler.level_map[logging.INFO] = (None, 'white', False)
    except ImportError:
        handler = logging.StreamHandler(sys.stdout)
    
    formatter = logging.Formatter("[%(funcName)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S") 
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(v*10)
    return logger

    