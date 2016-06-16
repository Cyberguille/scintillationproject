__author__ = 'cyberguille'

# saved as save-server.py
import Pyro4
# Server Connection to MySQL:
import MySQLdb


class Server(object):
    def save(self, data):
        if data[0] == 'Temperature':
            conn = MySQLdb.connect(host="localhost",
                                   user="root",
                                   passwd="root",
                                   db="scintillationdb")
            x = conn.cursor()
            print(data)
            try:
                x.execute("INSERT INTO data (type, date_time,value) values (%s,%s,%s)", (1, data[1], data[2]))
                conn.commit()
            except Exception, e:
                print str(e)
                conn.rollback()
            conn.close()


daemon = Pyro4.Daemon()  # make a Pyro daemon
ns = Pyro4.locateNS()  # find the name server
server = Server()
uri = daemon.register(server)  # register the save maker as a Pyro object
ns.register("scintillation.save", uri)  # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls