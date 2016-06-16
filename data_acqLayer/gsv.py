__author__ = 'root'

from nme_gp import NMEAGP
import re

class Sat(object):

    def __init__(self,id,elevation,azimuth,snr):
        self.id = id
        self.elevation = elevation
        self.azimuth = azimuth
        self.snr = snr

class GSV(NMEAGP):

    def __init__(self,msg):
        super(GSV, self).__init__(msg)

    def parse(self):
        self._parse = re.search('\$(?P<id>GP)(GSV),(?P<nmsg>[123])?,(?P<msgn>[123])?,(?P<sats>\d{2})?(,(?P<sat_id>\d{2})?,(?P<elevation>([0-8]\d|90))?,(?P<azimuth>([0-3]\d{2}))?,(?P<snr>\d{2})?)*\*\w{2}?',self._msg)
        # print self._parse
        self.TotalNMsg = self._parse.group('nmsg')
        self.MsgN = self._parse.group('msgn')
        self.Sats = self._parse.group('sats')
        p = re.compile(ur'(?P<id>\d{2}),(?P<ele>([0-8]\d|90)),(?P<azi>([0-3]\d{2})),(?P<snr>\d{2})')
        self.SatList =[]
        for m in p.finditer(self._msg):
            self.SatList.append(Sat(m.group('id'),m.group('ele'),m.group('azi'),m.group('snr')))

# gsv = GSV('$GPGSV,3,1,12,15,87,060,26,29,62,240,34,20,51,003,20,13,46,044,20*7A')
# print(gsv.Sats)
# print gsv.SatList