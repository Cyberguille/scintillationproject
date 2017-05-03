__author__ = 'root'

from nme_gp import NMEAGP
import re
import datetime


def converToDecimalDegree(degree, minutes, direction):
    mindegree = minutes/60.0
    sgn = -1 if direction=='S' or direction=='W' else 1
    return sgn*(degree+mindegree)



class GGA(NMEAGP):

    def __init__(self,msg):
        super(GGA, self).__init__(msg)

    def parse(self):
        try:
            self._parse = re.search('\$(?P<id>[A-Z]{2})(GGA),(?P<timeutc>((?P<hour>\d{2})(?P<minute>\d{2})(?P<seconds>\d{2})\.(?P<microseconds>\d{3})))?,(?P<latitude>(?P<latdegree>\d{2})(?P<latminutes>\d{2}.\d{4}))?,(?P<ns>[NS])?,(?P<longitude>(?P<longdegree>\d{3})(?P<longminutes>\d{2}.\d{4}))?,(?P<ew>[EW])?,(?P<gpsqi>[012])?,(?P<nsat>\d{2})?,(?P<hdp>\d.\d)?,(?P<aAltitude>-?\d*.\d)?,M?,(?P<GeoSep>-?\d*.\d)?,M?,(?P<AgeDifGPSData>\d.\d)?,(?P<DiffRefSID>(0\d{3}|(10(((0|1)\d)|2[0123])))\*\w{2})?',self._msg)
            self.TimeUTC = datetime.time(int(self._parse.group('hour')),int(self._parse.group('minute')),int(self._parse.group('seconds')),int(self._parse.group('microseconds')))
            self.Latitude = converToDecimalDegree(float(self._parse.group('latdegree')),float(self._parse.group('latminutes')),self._parse.group('ns'))
            self.NS_Indicator = self._parse.group('ns')
            self.Longitude = converToDecimalDegree(float(self._parse.group('longdegree')),float(self._parse.group('longminutes')),self._parse.group('ew'))
            self.EW_Indicator = self._parse.group('ew')
            self.GPS_QualityIndicator = self._parse.group('gpsqi')
            self.SatInView = self._parse.group('nsat')
            self.Hdop = self._parse.group('hdp')
            self.AntAlt = self._parse.group('aAltitude')
            self.GeoidSep = self._parse.group('GeoSep')
            self.DiffRefSID = self._parse.group('DiffRefSID')
            self.AgeDifGPSData = self._parse.group('AgeDifGPSData')
        except Exception,e:
               raise Exception('GGA: ' + e.message)


# gga = GGA('$GPGGA,145730.000,2304.1582,N,08227.6622,W,1,09,0.9,25.9,M,-21.3,M,,0000*5D')
# print(gga.TimeUTC)