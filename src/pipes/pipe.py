from abc import ABCMeta, abstractmethod
import sys
import time
from ..colors import bcolors

"""
Abstract class that must be inherited by all pipes. Provides common functionality across pipes.
"""
class Pipe():

    __metaclass__ = ABCMeta
    __name__ = "Pipe"
    __kwargs__ = {}

    def __init__(self,**kwargs):
        for name,options in self.__kwargs__.items():
            if name not in kwargs.keys():
                if options['required']:
                    raise Exception(f"[ERROR] Pipe {self.__name__} requires argument {name}")
                else:       
                    setattr(self,name,options['default'])
            else:
                setattr(self,name,kwargs[name])

    @abstractmethod
    def process(self):
        pass

    def start(self):
        sys.stdout.write(f"[INFO] Running pipe {self.__name__}... {bcolors.OKGREEN}running{bcolors.ENDC}\r")
        self.start = time.time()

    def done(self):
        end = time.time() - self.start
        sys.stdout.write(f"[INFO] Running pipe {self.__name__}... {bcolors.OKGREEN}done ✓ ({round(end,2)}s) {bcolors.ENDC}\n")

    def error(self,e):
        sys.stdout.write(f"[ERROR] Running pipe {self.__name__}... {bcolors.ERROR}error ❌ ({str(e)}) {bcolors.ENDC}\n")

    def __str__(self):
        return self.__name__