__author__ = 'cyberguille'

# saved as save-server.py
import Pyro4
# Server Connection to MySQL:
import MySQLdb

from gga import GGA
from gsa import GSA
from gsv import GSV
from rmc import RMC

import datetime
import time

class Acq(object):
    def __init__(self):
        self.utc = datetime.time()
        self.date = datetime.datetime(day=1,month=1,year=2016)
        self.station=0

    def getData(self, data):
        gga = GGA(data[0])
        if self.utc > gga.TimeUTC:
            self.date += datetime.timedelta(days=1)
        utc = gga.TimeUTC
        gsa = GSA(data[1])
        gsv = [GSV(data[2])]
        for i in range(3,5):
            gsv.append(GSV(data[i]))
        rmc = RMC(data[len(data)-1])
        if rmc != None:
            self.date = rmc.Date
        # self.date.time = self.utc
        self.save(gga,gsa,gsv,self.date,1)


    def save(self,gga,gsa,gsv,date,station):
        conn = MySQLdb.connect(host="localhost",
                                   user="root",
                                   passwd="root",
                                   db="scintillationdb")
        x = conn.cursor()
        try:
            datem = date.strftime('%Y-%m-%d %H:%M:%S')
            # print (datem,float(gsa.Hdop),float(gsa.Vdop),float(gsa.Pdop),float(gga.Latitude),float(gga.Longitude),float(gga.AntAlt),int(gga.GPS_QualityIndicator),int(gga.SatInView),station)

            x.execute("INSERT INTO primary_data (datetime,station_id,hdop,vdop,pdop,fix,nsat,latitude,longitude,height) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(datem,int(station),float(gsa.Hdop),float(gsa.Vdop),float(gsa.Pdop),int(gga.GPS_QualityIndicator),int(gga.SatInView),float(gga.Latitude),float(gga.Longitude),float(gga.AntAlt)))
            id = x.lastrowid

            for item in gsv:
                for sat in item.SatList:
                    # print (int(sat.id),id,int(sat.azimuth),int(sat.elevation),int(sat.snr),sat.id==gsa.SatList[0])
                    # print("sat.id: " + sat.id )
                    # print("gsa.SatList[0]: " + gsa.SatList[0])

                    x.execute("INSERT INTO sat_epoch (prn_code,obs_id,azm,elv,cno,used_fix) values (%s,%s,%s,%s,%s,%s)",
                      (int(sat.id),id,int(sat.azimuth),int(sat.elevation),int(sat.snr),int(sat.id==gsa.SatList[0])))

            conn.commit()
        except Exception, e:
            print str(e)
            conn.rollback()
        conn.close()



daemon = Pyro4.Daemon()  # make a Pyro daemon
ns = Pyro4.locateNS()  # find the name server
acq = Acq()
uri = daemon.register(acq)  # register the save maker as a Pyro object
ns.register("scintillation.acq", uri)  # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls