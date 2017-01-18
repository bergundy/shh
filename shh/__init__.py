import sys
from .process import Process


class Module(object):
    Process = Process

    def __init__(self, module):
        self.module = module

    def __getattr__(self, command):
        try:
            return getattr(self.module, command)
        except AttributeError:
            return self.Process(command)


sys.modules['shh'] = Module(sys.modules['shh'])
