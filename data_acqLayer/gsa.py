__author__ = 'root'

from nme_gp import NMEAGP
import re

class GSA(NMEAGP):

    def __init__(self,msg):
        super(GSA, self).__init__(msg)

    def parse(self):
           try:
               self._parse = re.search('\$(?P<id>[A-Z]{2})(GSA),(?P<selectMode>[MA])?,(?P<mode>[123])?,(?P<sats>((\d{2})?,){12})(?P<pdop>-?\d.\d)?,(?P<hdop>-?\d.\d)?,(?P<vdop>\d.\d)?\*\w{2}?',self._msg)
               self.SelMode = self._parse.group('selectMode')
               self.Mode = self._parse.group('mode')
               p = re.compile(ur'\d{2}')
               self.SatList =[]
               for m in p.finditer(self._msg):
                   self.SatList.append(m.group())
               self.Pdop = self._parse.group('pdop')
               self.Hdop = self._parse.group('hdop')
               self.Vdop = self._parse.group('vdop')
           except Exception,e:
               raise Exception('GSA: ' + e.message)

# gsa = GSA('$GPGSA,A,3,15,21,24,20,18,29,13,10,05,,,,1.6,0.9,1.4*3E')
# print(gsa.hdop)
# print(gsa.SatList)