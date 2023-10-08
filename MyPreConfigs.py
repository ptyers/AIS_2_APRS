# colection of preconfigured parameters for use thtoughout the program
#  may be modified by either access to registry or by reading from command line and changing
#

import socket
import ipaddress
import GlobalDefinitions
import sys
from configparser import ConfigParser
from datetime import datetime
from ProcessAVCGAList import ProcessAVCGAList
import pathlib


class MyPreConfigs:

    # flag starttime
    GlobalDefinitions.starttime = datetime.now()

    def __init__(self):
        # here would be a reading of the ini file to pick up any changes
        cfg = ConfigParser()
        cfg.read("AIS2APRS.ini")
        sections = cfg.sections()

        GlobalDefinitions.Global.WorkingDir = self.stripquotes(
            cfg.get("installation", "WorkingDirectory")
        )
        if len(GlobalDefinitions.Global.WorkingDir) == 0:
            # no working directory specified in ini
            # set it to directory from which this is run
            GlobalDefinitions.Global.WorkingDir = self.stripquotes(
                pathlib.Path(__file__).parent
            )
        GlobalDefinitions.Global.AVCGAList = self.stripquotes(
            cfg.get("installation", "AVCGAList")
        )
        GlobalDefinitions.Global.Station = self.stripquotes(
            cfg.get("installation", "Station")
        )
        GlobalDefinitions.Global.Production = cfg.getboolean(
            "installation", "Production"
        )
        GlobalDefinitions.Global.queuesize = int(cfg.get("installation", "QueueSize"))
        GlobalDefinitions.Global.Use_Serial = cfg.getboolean("operation", "UseSerial")
        GlobalDefinitions.Global.Use_UDP = cfg.getboolean("operation", "UseUDP")
        GlobalDefinitions.Global.Use_AISfile = cfg.getboolean(
            "operation", "UseDataFile"
        )
        GlobalDefinitions.Global.ComPort = self.stripquotes(
            cfg.get("operation", "COMPort")
        )
        GlobalDefinitions.Global.ComSpeed = int(cfg.get("operation", "COMSpeed"))
        GlobalDefinitions.Global.ServerAddress = self.stripquotes(
            cfg.get("operation", "LocalServer")
        )  # options FQDN or IPv4 string
        GlobalDefinitions.Global.remoteEnd = self.stripquotes(
            cfg.get("operation", "RemoteEnd")
        )
        GlobalDefinitions.Global.UseRemote = cfg.getboolean("operation", "UseRemote")
        GlobalDefinitions.Global.APRS_port = self.stripquotes(
            cfg.get("operation", "APRSPort")
        )
        GlobalDefinitions.Global.ServerPeriod = int(
            cfg.get("operation", "ServerPeriod")
        )
        GlobalDefinitions.Global.inport = self.stripquotes(
            cfg.get("operation", "InwardPort")
        )
        GlobalDefinitions.Global.WebPort = int(cfg.get("operation", "WebPort"))
        GlobalDefinitions.Global.localshipplotter = ipaddress.ip_address(
            "192.168.80.24"
        )
        # entry in ini file for MappingTTL is in MINUTES not Seconds
        GlobalDefinitions.Global.MappingTTL = (
            int(cfg.get("operation", "MappingTTL")) * 60
        )

        #  parameter to alow controlled closedown
        self._CloseDown = False
        self._fragdictttl = cfg.get(
            "operation", "FragTTL"
        )  # time entries remain in fragment dictionary
        # region diagnostics
        #  collection of diagnostic levels
        GlobalDefinitions.Global.diagnostic = cfg.getboolean("debug", "diagnostic")
        GlobalDefinitions.Global.diagnostic2 = cfg.getboolean("debug", "diagnostic2")
        GlobalDefinitions.Global.diagnostic3 = cfg.getboolean("debug", "diagnostic3")
        GlobalDefinitions.Global.diagnostic_Level = cfg.getboolean(
            "debug", "diagnostic_Level"
        )
        GlobalDefinitions.Global.LogIncoming = cfg.getboolean("logging", "Log_incoming")
        GlobalDefinitions.Global.LogAPRS = cfg.getboolean("logging", "Log_outgoing")
        GlobalDefinitions.Global.LogServer = cfg.getboolean("logging", "LogServer")
        GlobalDefinitions.Global.APRSFileName = self.stripquotes(
            cfg.get("logging", "APRSDataFile")
        )
        GlobalDefinitions.Global.AISFileName = self.stripquotes(
            cfg.get("logging", "AISDataFile")
        )

        # really heavy stuff - redirecting std.out, std.err
        GlobalDefinitions.Global.stdout = self.stripquotes(
            cfg.get("installation", "STDOUT")
        )
        GlobalDefinitions.Global.stdin = self.stripquotes(
            cfg.get("installation", "STDIN")
        )
        GlobalDefinitions.Global.stderr = self.stripquotes(
            cfg.get("installation", "STDERR")
        )

        # now get AVCGA Data

        GlobalDefinitions.Global.AVCGASDict = ProcessAVCGAList()

        # and ensure logging/diagnostic files exist
        if len(GlobalDefinitions.Global.APRSFileName) != 0:
            try:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.APRSFileName,
                    "r",
                )
            except FileNotFoundError:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.APRSFileName,
                    "w",
                )
            f.close

        if len(GlobalDefinitions.Global.AISFileName) != 0:
            try:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.AISFileName,
                    "r",
                )
            except FileNotFoundError:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.AISFileName,
                    "w",
                )
            f.close

        # also a diagnostic file used if stderr has been redirected
        # this filename is hardcoded in GlobalDEfinitions and not set in ini file
        if len(GlobalDefinitions.Global.StderrFileName) != 0:
            try:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.StderrFileName,
                    "r",
                )
            except FileNotFoundError:
                f = open(
                    GlobalDefinitions.Global.WorkingDir
                    + "\\"
                    + GlobalDefinitions.Global.StderrFileName,
                    "w",
                )
            f.close

    def stripquotes(self, thisstring: str) -> str:
        if '"' in thisstring or "'" in thisstring:
            count = 0
            retstring = ""
            while count < len(thisstring):
                if thisstring[count] != "'" and thisstring[count] != '"':
                    retstring += thisstring[count]
                count += 1
            return retstring
        else:
            return thisstring
