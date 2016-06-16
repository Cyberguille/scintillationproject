__author__ = 'cyberguille'

from nme_gp import NMEAGP
import re
import datetime

class RMC(NMEAGP):
    def __init__(self,msg):
       super(RMC, self).__init__(msg)

    def parse(self):
        self._parse = re.search('\$GPRMC,(?P<timeutc>((?P<hour>\d{2})(?P<minute>\d{2})(?P<seconds>\d{2})\.(?P<microseconds>\d{3})))?,(?P<status>[AV]),(?P<latitude>\d{4}.\d{4})?,(?P<ns>[NS])?,(?P<longitude>\d{5}.\d{4})?,(?P<ew>[EW])?,(?P<speedOG>\d.\d{2})?,(?P<courseOG>\d{3}.\d{2})?,(?P<date>(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{2}))?,(?P<magneticVar>\d{3}.\d{2})?,(?P<ewMG>[EW])?,[A-Z]?(\*\w{2})?',self._msg)
        self.TimeUTC = datetime.time(int(self._parse.group('hour')),int(self._parse.group('minute')),int(self._parse.group('seconds')),int(self._parse.group('microseconds')))
        self.Status = self._parse.group('status')
        self.Latitude = self._parse.group('latitude')
        self.NS_Indicator = self._parse.group('ns')
        self.Longitude = self._parse.group('longitude')
        self.EW_Indicator = self._parse.group('ew')
        self.SpeedOG = self._parse.group('speedOG')
        self.CourseOG = self._parse.group('courseOG')
        self.Date = datetime.datetime(int('20'+self._parse.group('year')),int(self._parse.group('month')),int(self._parse.group('day')))
        self.MagneticVar = self._parse.group('magneticVar')
        self.EW_MG = self._parse.group('ewMG')

# rmc = RMC('$GPRMC,145730.000,A,2304.1582,N,08227.6622,W,0.00,245.11,140116,,,A*7C')
# print(rmc.Date)
