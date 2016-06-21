import os
import sys
from  multiprocessing.dummy import Pool

class component_scan(object):

    def __init__(self, script):
       self.script = script 

    def __verify(self, dest):
       
        __import__(self.script)
        result = sys.module[self.script].verify(dest)

        return result

    def __exploit(self):
        
        __import__(self.script)
        result = sys.module[self.script].exploit(dest)

        return result

    def scan(self, num, dest, mode):
        
        pool = Pool(num)
        if mode == 'verify':
            result = pool.map(dest, __verify)
        elif mode == 'exploit':
            result = pool.map(dest, __exploit)

        pool.close()
        pool.join()

        return result
        
