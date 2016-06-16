__author__ = 'root'

import re
import os

import Pyro4


def nmea_chksum(sentence):
    sentence = sentence.rstrip('\n')
    cksum = sentence[len(sentence) - 3:]
    chksumdata = re.sub("(\n|\r\n)", "", sentence[sentence.find("$") + 1:sentence.find("*")])
    csum = 0
    for c in chksumdata:
        csum ^= ord(c)
    try:
        if hex(csum) == hex(int(cksum, 16)):
            return True
    except Exception:
        pass
    return False


def nmea_chkmerged(sentence):
    if sentence.find('$GP', 3) <= 0:
        return True
    return False


def send_packet():
    if lastRMC == "":
        return
    # for line in nmea_packet:
    #	print(line)
    # outFile.write(line)
    nmea_packet.append(lastRMC)
    # AQUI ENVIAR EL OBJETO NMEAPACKET
    # print("before pyro")
    acq = Pyro4.Proxy("PYRONAME:scintillation.acq")  # use name server object lookup uri shortcut
    # print nmea_packet
    acq.getData(nmea_packet)
    del nmea_packet[:]


# outFile.write(lastRMC)


def packet_assembly(sentence):
    if sentence.startswith('$GPRMC'):
        global lastRMC
        lastRMC = sentence
        return
    if len(nmea_packet) == 0:
        if not sentence.startswith('$GPGGA'):
            return
    if len(nmea_packet) == 1:
        if not sentence.startswith('$GPGSA'):
            del nmea_packet[:]
            return
    if len(nmea_packet) == 2:
        if not sentence.startswith('$GPGSV'):
            del nmea_packet[:]
            return
        try:
            if not sentence.split(',')[2] == '1':
                del nmea_packet[:]
                return
        except Exception:
            print "Exception"
            del nmea_packet[:]
            return
    if len(nmea_packet) >= 3:
        if not sentence.startswith('$GPGSV'):
            del nmea_packet[:]
            return
        else:
            try:
                numOfGSV = int(nmea_packet[-1].split(',')[1])
                currentGSV = int(sentence.split(',')[2])
                prevGSV = int(nmea_packet[-1].split(',')[2])
                # print(numOfGSV,currentGSV,prevGSV)
                if not currentGSV - prevGSV == 1:
                    del nmea_packet[:]
                    return
                if currentGSV == numOfGSV:
                    nmea_packet.append(sentence)
                    # print("send_packet")
                    send_packet()
                    return
            except Exception,e :
                print "Exception"
                print(e)
                del nmea_packet[:]
                return
    nmea_packet.append(sentence)


lineNum = 0
lastRMC = ""
nmea_packet = []
# Config Segment BEGIN
workFolder = "/media/guille/Storage/Project/GPS/GPS_Log_00/"
fileId = 0
# Config Segment END
infilepath = workFolder + str(fileId) + ".nmea"
outfilepath = workFolder + str(fileId) + "_ok.nmea"

while os.path.isfile(infilepath):
    outFile = open(outfilepath, "w")
    with open(infilepath, "r") as inFile:
        for line in inFile:
            lineNum += 1
            if not nmea_chkmerged(line):
                print("BAD LINE: %s" % lineNum)
                del nmea_packet[:]
            else:
                if not nmea_chksum(line):
                    print("BAD LINE: %s" % lineNum)
                    del nmea_packet[:]
                else:
                    # print "ok line: %s" %lineNum
                    packet_assembly(line)
    outFile.close()
    fileId += 1
    infilepath = workFolder + str(fileId) + ".nmea"
    outfilepath = workFolder + str(fileId) + "_ok.nmea"
    # break
print "End"