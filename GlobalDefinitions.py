"""
Module containing variables used throughout the system

Python declares all variables static so it may be necessary to declare internal variables within classes
which will not be affected by other variables of the same class modifying them

Data is passed from the getter threads (UDP and serial) to the Processing thread through a queue defined here
and from the processing thread to the send to APRS thread on another queue defined here

CAUTION CAUTION CAUTION
entries in APRS.ini override definitions in this file




"""

#import Mapper
import Map
import AVCGAmmsi
import datetime
from queue import Queue
import sys


class Global:
    # static MyTcpServer server

    #  and an AIS_Data object for later use


    # Time To Live (TTL) for mappings of MMSI to ShipName
    # Entries flushed from the Mapping Dictionary by the do_stats function
    # stored here as seconds - in AIS2APRS.ini entered as minutes
    MappingTTL = 360 * 60

    #  and another dictionary which holds mappings from MMSI to Callsign,Name,Destination,Type
    #  thgis is used by the APRS stream generators to replace MMSI by callsign and to put Name in the comments field
    # again create a dummy to show content

    MyMap = Map.Map()
    Themap = MyMap.Themap
    #  Dictionary holding list of AVCGA vessels and their MMSI
    # again a dummy to show content keyed om MMSI
    # only facilities with MMSI are held
    AVCGADict = {}
    """
    the list of strings is defined as
        _facility = record[0]
        _location = record[1]
        _callsign = record[2]
        _stationType = record[3]
        _licenceNo = record[4]
        _siteID = record[5]
        _CGDom = record[6]
        _CGNewDom = record[7]
        _epirb = record[8]
        _hexNo = record[9]
        _expiry = record[10]
        _mmsi = record[11]
        _dsc = record[12]
        _ant_checked = record[13]
        _comment = record[14]

    """
    dummyAVCGA = AVCGAmmsi.AVCGAMMSI("list of strings")

    #  Dictionary used to hold APRS text stream prior to sending to server
    ServerQueue = {}
    #
    # and another dictionary of valid Serial port speeds
    SpeedDict = {
        300: True,
        600: True,
        1200: True,
        2400: True,
        4800: True,
        9600: True,
        19200: True,
        38400: True,
        57600: True,
        115200: True,
        128000: True,
    }

    #  We need to keep count of Safety Bulletin IDs (type 14 Messages)
    Bulletin = int(0)  # incremented mod 10 before use

    #  and now we need a holding location for the last time APRS data was sent
    LastTransmit = datetime.datetime.now()

    # queue to collect data from "getters"
    # both have a size limit of 1024 items
    # and  thje queue put and gets should check for space or empty queue
    #  and gets should not block
    queuesize = 1024
    inputqueue = Queue(queuesize)
    # queue to send data on to the send to APRS thread
    outputqueue = Queue(queuesize)
    # queue to collect stats in a thread safe manner
    Statsqueue = Queue(64)  # shouldnt need to be overlarge should be cleared regulary
    # format is tuple (StatName, StatValue)

    # and a bool which is checked by threads to see if trhey should cease
    _keepgoing = True
    ServerPeriod = 30
    Use_Serial = False
    Use_UDP = True
    Use_AISfile = False

    WorkingDir = ""
    AISFileName = "AISDatastream.txt"
    APRSFileName = ""
    AVCGAList = ""
    Station = "CG722-1"
    StderrFileName = "StdErrFile"
    WebPort = 8448

    UseRemote = True  # use remote server rather than local UIView
    remoteEnd = "vf12.dyndns.org"
    CloseDown = False

    inport = 4158
    APRSPort = 1448
    ServerAddress = ""
    ComPort = ""
    ComSpeed = 38400

    diagnostic = False
    diagnostic2 = False
    diagnostic3 = False
    diagnostic_Level = 0
    LogIncoming = False
    LogAPRS = False
    LogServer = False
    # Simple Network Management Protocol settings
    SNMP = True
    SNMPServer = "192.168.80.3"

    # group of Statistics
    starttime = datetime.datetime.now()  # this will be overwritten on start up

    Statistics = {
        "Nr_UDP_Frames_RX": 0,
        "Nr_UDP_Frames_Dropped": 0,
        "Nr_UDP_Frames_permin": 0,
        "Nr_Serial_Frames_RX": 0,
        "Nr_Serial_Frames_Dropped": 0,
        "Nr_Serial_Frames_permin": 0,
        "Nr_APRS_TX": 0,
        "Nr_APRS_permin": 0,
    }

    UDP_Received_IP_Addresses = (
        {}
    )  # Dictionary of IP Addresses from which data is received

    # really heavy stuff - redirecting std.out, std.err
    stdout = sys.stdout
    stdin = sys.stdin
    stderr = sys.stderr

    #  Need a bool to indicate we have connection problems
    NoConnect = False

    APRS_Socket_Status = False  # flag indicating if APRS Stream has been
    # instantiated

    Production = False  # used to allow recovery in production environment
    # where error message3s will be written to a file but
    # operation will continue having dumped whatever record caused grief


def main():
    pass


if __name__ == 'main':
    main()
