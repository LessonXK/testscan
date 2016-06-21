import sys
import multiprocessing.dummy as thread

from lib.data import AttribDict
import logging
import sys
from logging.handlers import RotatingFileHandler

logger = None

if not PrConsole:

    logger = logging.getLogger('monitorlog')

    Rhandler = None

    Rhandler = RotatingFileHandler('monitor.log',mode = 'a',maxBytes = 10*1024*1024,backupCount = 5)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S %p")

    Rhandler.setFormatter(formatter)
    logger.addHandler(Rhandler)
    logger.setLevel(logging.INFO)

else:

    logger = logging.getLogger("monitorlog")

    handler = None

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S %p")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


'''
LOGGER = logging.getLogger('monitorlog')

LOGGER_HANDLER = None

LOGGER_HANDLER = logging.FileHandler('monitor.log',mode = 'w')

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)
'''

def scan(num,dest,script):

    vscript = script

    pool = thread.Pool(num)
    result = pool.map(dest, run)

    pool.close()
    pool.join()




def run(dest):

    global vscript
    __import__(vscript)

    result = sys.module[vscript].audit(dest)

    return result
