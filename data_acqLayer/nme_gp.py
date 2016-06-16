__author__ = 'guille'
from abc import ABCMeta, abstractmethod

class NMEAGP(object):
    __metaclass__ = ABCMeta

    def __init__(self, msg):
        self._parse = None
        self._msg=msg
        self.parse()


    @abstractmethod
    def parse(self):
        pass