from datetime import datetime
import GlobalDefinitions
import logging
from Payloads import Static_data_report, Payload, Addressed_safety_related_message, Safety_related_broadcast_message
from Map import Map, MapItem
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, SOCK_DGRAM


class APRS:
    # static bool Diagnose_APRS = True

    #  defines APRS actions and parameters
    #  based on APRS Protocol Reference - Protocol Version 1.0.1
    #

    # region Public Properties

    def get_Course(self):
        return self._course

    def set_Course(self, value):
        if isinstance(value, str):
            self._course = value
        else:
            self._course = ""
            raise TypeError("Course must be string")

    def get_Speed(self):
        return self._speed

    def set_Speed(self, value):
        if isinstance(value, str):
            self._speed = value
        else:
            self._speed = ""
            raise TypeError("Speed must be string")

    def get_Name(self):
        return self._name

    def set_Name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            self._name = ""
            raise TypeError("Name must be string")

    def get_Callsign(self):
        return self._callsign

    def set_Callsign(self, value):
        if isinstance(value, str):
            self._callsign = value
        else:
            self._callsign = ""
            raise TypeError("Callsign must be string")

    def get_MMSI(self):
        return self._callsign

    def set_MMSI(self, value):
        if isinstance(value, str):
            self._mmsi = value
        else:
            self._mmsi = "Unknown"
            raise TypeError("Callsign must be string")

    # endregion
    # endregion
    # region Constructors
    def __init__(
            self,
            mmsi: str,
            latitude: float,
            longitude: float,
            heading: float,
            speed: float,
            comment: str,
            IsAVCGA: int,
            relay_station: str = GlobalDefinitions.Global.Station,
            **kwargs
    ):

        self._longitude = self.ConvertLongitude(longitude)
        self._latitude = self.ConvertLatitude(latitude)
        self.set_Course(f'{heading:03}')
        self.set_Speed(f'{speed:03}')
        self.set_MMSI(mmsi)
        self._name = ""
        self._callsign = ""
        self._comment = comment
        self._safetytext = ""
        self._isavcga = IsAVCGA
        self._relay_station: str = relay_station

    def __repr__(self):
        return (
            f'MMSI                      {self._mmsi}\n'
            f'Latitude                  {self._latitude}\n'
            f'Longitude                 {self._longitude}\n'
            f'Heading                   {self._course}\n'
            f'Comment                   {self._comment}\n'
            f'Callsign                  {self._callsign}\n'
            f'isAVCGA                   {self._isavcga}\n'
            f'Relay Station             {self._relay_station}\n'
        )

    def ConvertLongitude(self, longitude: float) -> str:

        #  takes in a float and converts to APRS format
        #  fixed 8 character field in degrees and decimalminutes to two places
        #  followed by either E or W ( +ve East, -ve West)
        #  eg 4903.50N represents 49 degrees 3 minutes 30 seconds East
        #
        #  incoming longitude has format degrees and decimal degrees "DDD.dddd"
        #  needs to be converted to DDDMM.dd{E,W}
        if longitude <= 0:
            longitude = -longitude
            self._longitude = self.SplitLongitude(longitude) + "W"
        else:
            self._longitude = self.SplitLongitude(longitude) + "E"
        return self._longitude

    def SplitLongitude(self, longitude: float) -> str:

        degrees = int(longitude)
        minutes_f = float((longitude - degrees) * 60)
        minutes = int(minutes_f)
        decimals = int(((minutes_f - minutes) * 100.0))
        return (
                format(degrees, "03d")
                + format(minutes, "02d")
                + "."
                + format(decimals, "02d")
        )

    def ConvertLatitude(self, latitude: float) -> str:
        #  takes in a float and converts to APRS format
        #  fixed 8 character field in degrees and decimalminutes to two places
        #  followed by either N or S (+ve North)
        #  eg 4903.50N represents 49 degrees 3 minutes 30 seconds North
        #
        if latitude <= 0:
            latitude = -latitude
            self._latitude: str = self.SplitLatitude(latitude) + "S"
        else:
            self._latitude: str = self.SplitLatitude(latitude) + "N"

        return self._latitude

    def SplitLatitude(self, latitude: float) -> str:
        degrees = int(latitude)
        minutes_f = float((latitude - degrees) * 60)
        minutes = int(minutes_f)
        decimals = int(((minutes_f - minutes) * 100.0))
        return (
                format(degrees, "02d")
                + format(minutes, "02d")
                + "."
                + format(decimals, "02d")
        )

    def ConvertSpeed(self, speed: int):

        self._speed = format(speed, "03d")

    def CreateObjectPosition(self, kill: bool, mydata: Payload) -> str:
        try:
            statuschar = ""
            typechar = "s"
            tablechar = "\\"  # single \

            self._mmsi = mydata.mmsi

            isAVCGA = self._isavcga

            if kill:
                logging.debug("supposedly killing {}  ".format(mydata.mmsi))

            try:
                if not kill:
                    statuschar = "*"
                    if self._mmsi in Map.Themap:
                        #mmsi, callsign, vessel_name, destination, timestamp, killflag = Map.Themap[self._mmsi]
                        thisitem =Map.Themap[self._mmsi]
                        vessel_name = thisitem.vessel_name
                        mmsi = thisitem.mmsi
                        callsign = thisitem.callsign
                        destination = thisitem.destination
                        killflag = thisitem.kill
                        if vessel_name != '':
                            self._name = vessel_name
                        if callsign != '':
                            self._callsign = callsign
                    if self._name != "":
                        self._comment = self._name + " " + self._mmsi + " " + self._callsign
                        self.callsign = self._name
                        # add the mmsi to the comment field
                    else:
                        self._callsign = self._mmsi

                else:
                    statuschar = "_"
                    _callsign = self._mmsi
            except Exception as e:
                raise Exception('APRS.CreateObjectPosition line 197', e) from e

            if self._name == "" or kill:
                Xcallsign = self._mmsi
            else:
                Xcallsign = self._name

            while len(Xcallsign) < 9:  # for reasons of compatibility with APRS standard
                #  callsign must be fixed 9 chars if doing object reporting
                Xcallsign = Xcallsign + " "

            #  allowance for callsign exceeding 9 chars
            Xcallsign = Xcallsign[0:9]

            #  now cater for special types
            _typecharoption = {"111": "^", "974": "!"}
            _tablecharoption = {"974": "/"}

            """
                    case "111":  #  SAR aircraft   typechar = "^"
                    {
                    case "970":  #  AIS SART
                    case "972":  #  MOB
                    case "974":  #  EPIRB
                     } tablechar = "/" typechar = "."
                    default:
                """
            if self._mmsi[0:3] in _typecharoption:
                typechar = _typecharoption[self._mmsi[0:3]]
            elif mydata.message_type == 9:
                typechar = '^'

            if self._mmsi[0:3] in _tablecharoption:
                tablechar = _tablecharoption[self._mmsi[0:3]]

            #  and finally cater for AVCGA vessels - transmit these as valid position reports
            #
            if isAVCGA:
                typechar = "C"  # Coastguard Vessel might be an 'L' modified table

            #  creates position report for object with time stamp
            thetime = datetime.utcnow()
            # string timestamp = thetime.Day.ToString("0#") +
            # thetime.Hour.ToString("0#") +
            # thetime.Minute.ToString("0#") + "z"
            timestamp = thetime.strftime("%d%H%Mz")
            """
            Format of APRS information block is like
                For Object report (where APRSDataIdentifier = ';')
                CG722>APU25N,TCPIP*,<ThisStation>:<APRSDataIdentifier><callsign><StatusChar><Timestamp>
                <latitude(8.2){S/N}><SymbolTable Identifier><Longitude(9.2){E/W}<SymbolTable Character>
                <Course(3.0)>"/"<Speed(3.0)><CommentField(generally Name)>\r
    
    
            StatusChar = {Live Object = '*', Kill Object = '_'}
            Symbol Table Identifier = {Primary Symbol Table = '/', Secondary Symbol Table = '\'}
            Symbol Table Character = index into symbol table = {Ship = 's', SAR Aircraft = '^',
            Emergency  = '!', Nav Mark = 'N', CoastGuard = 'C'}
            Where we have a callsign append MMSI to name field (truncate to 43 if necessary)
            
            
            """
            if Xcallsign[0:8] != mydata.mmsi:
                # strip trailing spaces off name/callsign
                while self._name[:-1] == " " and len(self._name) > 1:
                    self.name = self._name[0:-2]
                    # print(self._name, len(self._name))
                while self._callsign[:-1] == " " and len(self._callsign) > 1:
                    self._callsign = self._callsign[0:-2]

                self.txname = (self._name + " " + mydata.mmsi + " " + self._callsign)[0:42]

            message = (f'{self._relay_station}>APU25N,TCPIP*:;{Xcallsign}{statuschar}{timestamp}{self._latitude}'
                       f'{tablechar}{self._longitude}{typechar}{self._course}/{self._speed}{self.txname}\n')

            logging.debug(f'in CreateObject with kill tcpbytes \n{self._relay_station}>APU25N,TCPIP*:;'
                          f'{Xcallsign}{statuschar}{timestamp}{self._latitude}{tablechar}'
                          f'{self._longitude}{typechar}{self._course}{self._speed}/{self.txname}\n'
                          , stacklevel=True)

            return message

        except Exception as e:
            raise Exception('CreateObjectPosition', e) from e

    def CreateBasePosition(self, kill: bool, mydata: Payload) -> str:
        #  creates position report for base station (symbol triangle) with time stamp
        try:
            thetime = datetime.utcnow()
            # string timestamp = thetime.Day.ToString("0#") + thetime.Hour.ToString("0#") + thetime.Minute.ToString("0#") + "z"
            timestamp = thetime.strftime("%d%H%Mz")
            if not kill:
                killchar = '*'
            else:
                killchar = '_'
            message = (
                f'{self._relay_station}>APU25N,TCPIP*:;{self._mmsi}{killchar}{timestamp}'
                f'{self._latitude}\\{self._longitude}L\n'
            )

            return message
        except Exception as e:
            logging.error('CreateBasePosition' + str(e), stack_info=True)
            raise Exception('CreateBasePosition', e) from e

    """
    def CreatePosition(self) -> str:
        #  create a position report for a valid coastguard vessel
        #
        thetime = datetime.datetime.utcnow()
        # string timestamp = thetime.Day.ToString("0#") + thetime.Hour.ToString("0#") + thetime.Minute.ToString("0#") + "z"
        timestamp = thetime.strftime("%d%H%Mz")
        message = self._mmsi + ">APU25N,TCPIP*:/" + timestamp + self._latitude + "\\" + self._longitude \
            + "s" + self._course + "/" + self._speed + self._name + "\n"

        return message
    """

    def CreateSafetyMessage(self, Bulletin: int, mydata: Payload) -> str:
        try:
            # myaprs = APRS(mydata.mmsi, 0.0, 0.0, 0.0, 0.0, 'Safety', 0)
            logging.debug(f'entering create safety message Type = {mydata.message_type}')
            if mydata.message_type == 14:
                my14: Safety_related_broadcast_message = mydata
                self._safetytext = my14.safety_text
                logging.debug(f'Inside type 14 process self._safety_text = {self._safetytext}')
                #  create a bulletin frame
                self.message = ""
                while self._safetytext != "":
                    logging.debug(f'length safetytext {len(self._safetytext)}')
                    while len(self._safetytext) > 67:

                        self.bulltext = self._safetytext[0:66]
                        logging.debug(f'where safetytext > 67 bulltext = {self.bulltext}')
                        self.message = self.message + (f'{self._relay_station}>APU25N,TCPIP*'
                                                       f'::BLN{str(Bulletin)}     :{self.bulltext}\n')
                        if len(self._safetytext) > 67:
                            self._safetytext = self._safetytext[66:]
                        Bulletin += 1
                        Bulletin = Bulletin % 10

                    logging.debug(f'where safetytext < 67 self.safetytext = {self._safetytext}')
                    self.message = self.message + (f'{self._relay_station}>APU25N,TCPIP*::BLN'
                                                   f'{str(Bulletin)}     :{self._safetytext}\n')
                    self._safetytext = ''
            elif mydata.message_type == 12:
                my12: Addressed_safety_related_message = mydata
                logging.debug('processing type 12 ')
                self.message = ''
                self._safetytext = my12.safety_text
                if self._safetytext != "":
                    while self._safetytext != "":
                        while len(self._safetytext) > 67:
                            self.bulltext = self._safetytext[0:66]

                            while len(my12.destination_mmsi) < 9:  # this should be redundant but in case
                                my12.destination_mmsi = my12.destination_mmsi + ' '

                            self.message = self.message + (f'{self._relay_station}>APU25N,TCPIP*'
                                                           f':{my12.destination_mmsi}:{self.bulltext}\n')
                            self._safetytext = self._safetytext[66:]
                            Bulletin += 1
                            Bulletin = Bulletin % 10

                        self.message = self.message + (f'{self._relay_station}>APU25N,TCPIP*'
                                                       f':{my12.destination_mmsi}:{self._safetytext}\n')
                        self._safetytext = ''

            return self.message
        except Exception as e:
            logging.error(f'In CreateSafetyMessage \n{str(e)}', stack_info=True)
            raise Exception('CreateSafetyMessage', e) from e


############################################################################################################

def SendAPRS(p, mydata, kill: bool, Bulletin: int, test: bool = False):
    # print('into sendAPRS with message type {} '.format(mydata.message_type))
    # bool test is used during unit testing, otherwise unused

    #  takes analysed AIS stream and at periodic intervals sends to APRS server
    tcpbytes = bytearray("", "utf-8")
    try:
        if p not in [12, 14]:
            myaprs = APRS(
                mydata.mmsi,
                mydata.latitude,
                mydata.longitude,
                mydata.course_over_ground,
                mydata.speed_over_ground,
                mydata.vessel_name,
                mydata.isAVCGA
            )

        else:
            myaprs = APRS(
                mydata.mmsi,
                0.0,
                0.0,
                0.0,
                0.0,
                'Safety',
                0
            )

        myaprs.MMSI = mydata.mmsi

        if mydata.message_type in [5,24]:
            if len(mydata.callsign) > 0:
                myaprs.Callsign = mydata.callsign
                if mydata.callsign == "":
                    xcallsign = mydata.mmsi
                else:
                    xcallsign = mydata.callsign
        else:
            xcallsign = mydata.mmsi


    except Exception as e:
        raise RuntimeError("Error creating myaprs in SendAPRS", e) from e


    try:
        # using match statement - needs python 3.10 and upwards
        match mydata.message_type:
            case 1:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 2:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 3:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 4:
                tcpbytes = dobase(mydata, myaprs)
            case 5:
                tcpbytes = datareport(mydata, myaprs,  kill)
            case 9:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 12:
                tcpbytes = dosafety(mydata, myaprs, Bulletin)
            case 14:
                tcpbytes = dosafety(mydata, myaprs, Bulletin)
            case 18:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 19:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 21:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case 24:
                tcpbytes = datareport(mydata, myaprs,  kill)
            case 27:
                tcpbytes = doposition(mydata, myaprs, 0, kill)
            case default:
                pass

    except Exception as e:
        raise Exception('SendAPRS line 78 tcpbytes definition p= {}'.format(p), e) from e

    #  now queue the aprs stream
    try:
        if not test:
            logging.debug(f'Called QueueAPRS with Xcallsign {xcallsign} '
                          f'and bytearray {tcpbytes}', stack_info=True)
            QueueAPRS(xcallsign, tcpbytes)
        else:
            return xcallsign,  tcpbytes
    except Exception as e:
        raise Exception('SendAPRS line 83 QueueAPRS ', e) from e

    try:
        logging.debug(f'Called TransmitAPRS bytearray {tcpbytes}', stack_info=True)
        TransmitAPRS()
    except Exception as e:
        raise RuntimeError(
            "Error Attempting to Transmit APRS following queuing", e
        ) from e

    # finished with myaprs dispose of it
    del myaprs


def donothing(args, dummy: int, kill: bool):
    # print('In SendAPRS.donothing')
    pass


def doposition(mydata, myaprs, dummy: int, kill: bool):
    logging.debug('In SendAPRS.doposition')
    try:
        tcpbytes = bytearray(myaprs.CreateObjectPosition(kill, mydata), "utf-8")

        logging.debug(f'in doposition tcpbytes {tcpbytes}')

        return tcpbytes

    except Exception as e:
        raise RuntimeError(
            "Exception while processing (queue) Type 1,2,3,9,18", e
        ) from e


def dobase(mydata, myaprs):
    # 'In SendAPORS.do4')

    # print(myaprs.CreateObjectPosition())
    try:
        tcpbytes = bytearray(myaprs.CreateBasePosition(False, mydata), " utf-8")
    except Exception as e:
        raise Exception('SendAPRS .do4 line 490', e) from e

    return tcpbytes


def dosafety(mydata, myaprs, Bulletin: int):
    # print('In SendAPORS.do14')
    try:
        tcpbytes = bytearray(myaprs.CreateSafetyMessage(Bulletin, mydata), "utf-8")
        return tcpbytes
    except Exception as e:
        raise RuntimeError("Exception while processing (queue) Type 14", e) from e


def datareport(mydata, myaprs,  kill: bool):
    # print('In SendAPORS.do5_24')
    try:
        # APRS myaprs = new APRS(mydata.String_MMSI, mydata.Latitude, mydata.Longitude, mydata.COG, mydata.SOG, "")
        try:
            myaprs._course = str(mydata.course_over_ground)
            myaprs._speed = str(mydata.speed_over_ground)
        except Exception as e:
            raise Exception('In SendAPRS.datareport updating speed and course', e) from e

        try:
            tcpbytes = bytearray(myaprs.CreateObjectPosition(kill, mydata), "utf-8")
        except Exception as e:
            raise Exception('In SendAPRS.datareport failed to create object position', e) from e

        return tcpbytes

    except Exception as e:
        raise RuntimeError("Exception while processing (queue) Type 5,24", e) from e


def QueueAPRS(Callsign: str, tcpbytes, test: bool = False):
    # print('In SendAPORS.QueueAPRS')
    #  queues APRS text streams deleting duplicates
    #  uses dictionary ServerQueue to hold APRS byte steam keyed on the Callsign field
    #
    #  need to convert the byte array tcpbytes to a string before attempting to check for duplicates
    #

    """# FOR TESTING
    #############################################
    print('FOR TESTING\r\nEntering QueueAPRS\r\nCallsign= {}\r\ntcpbytes ={}' \
    .format(Callsign,tcpbytes))

    ##############################################
    """
    try:
        aprsstring = tcpbytes.decode()

        ServerQueue = GlobalDefinitions.Global.ServerQueue


        logging.info(f'In QueueAPRS aprsstring = {aprsstring}')

        try:
            if Callsign in ServerQueue:
                #  already an entry in the queue
                try:
                    if ServerQueue[Callsign] != aprsstring:
                        # print('in queue aprs replacing\n', ServerQueue[Callsign], 'with\n', aprsstring)
                        #  need to delete current value in queue and replace by new value
                        ServerQueue[Callsign] = aprsstring
                except KeyError:
                    pass

                    logging.info(f"In QueueAPRS Queue Count = {len(ServerQueue)}")
                    for xx in ServerQueue:
                        logging.info(f"MMSI {xx} Data {ServerQueue[xx]} ")

                    #  otherwise do nothing its a duplicate

            else:
                #  Create an entry in queue
                logging.info(f"adding record to QueueAPRS {Callsign}: {aprsstring}" )

                ServerQueue.update({Callsign: aprsstring})

                logging.info(f"In QueueAPRS Queue NewEntry Count = {len(ServerQueue)}")

        except Exception as e:
            logging.error("Error while queuing APRS")
            raise RuntimeError("Error in Queue APRS\r\n", e) from e

    except Exception as e:
        raise Exception('Queue APRS ', e) from e


def Do_diag_print(DiagBool, diagstr):
    if DiagBool:
        print(diagstr)


def TransmitAPRS(test: bool = False):
    logging.debug(f'entering transmit_aprs test = {test}')
    try:
        # print('In SendAPORS.TransmitAPRS')

        StatsQ = GlobalDefinitions.Global.Statsqueue
        UseRemote = GlobalDefinitions.Global.UseRemote
        LogAPRS = GlobalDefinitions.Global.LogAPRS
        APRSLogFile = GlobalDefinitions.Global.APRSFileName

        LastTransmit = GlobalDefinitions.Global.LastTransmit
        ServerQueue = GlobalDefinitions.Global.ServerQueue
        NoConnect = GlobalDefinitions.Global.NoConnect
        NoConnect = True
        try:  # all encompassing exception  catch all to pass up the tree

            aprs_stream = socket(AF_INET, SOCK_STREAM)
            aprs_stream.close()

            #  having queued APRS stream now we see if it should be sent
            #  compare current time with LastTransmit time
            current = datetime.now()
            difference = current - GlobalDefinitions.Global.LastTransmit

            logging.debug(f'tx timedifference {difference.total_seconds()}')

            if difference.total_seconds() > GlobalDefinitions.Global.ServerPeriod or test:
                logging.debug('about to do a transmit')
                if NoConnect:
                    try:
                        aprs_stream = socket(AF_INET, SOCK_STREAM)
                    except OSError as e:
                        raise RuntimeError(
                            "Error creating socket in sendAPRS: %s\n" % e
                        ) from e

                    # Second try-except block -- connect to given host/port
                    try:

                        aprs_stream.connect(define_server_address(UseRemote))
                    except ConnectionRefusedError as e:
                        raise RuntimeError(
                            "Connection Refused error in SendAPRS:\r\n'\
                        ' Address %s Port %d\n\r %s"
                            % GlobalDefinitions.Global.ServerAddress,
                            GlobalDefinitions.Global.APRSPort,
                            e,
                        ) from e
                    except ConnectionError as e:
                        raise RuntimeError("Connection error in sendAPRS: %s'\n" % e) from e

                    except TimeoutError as e:
                        do_print_server_address(UseRemote)
                        raise RuntimeError("Timeout error in sendAPRS: %s'\n" % e) from e

                    except Exception as e:
                        raise RuntimeError(
                            "Unspecified Connection Error connecting to server in sendAPRS: '\r''\n %s '\n'\r"
                            % e
                        ) from e

                    logging.debug('apparently connected')

                    GlobalDefinitions.Global.NoConnect = (
                        False  # we now have valid connection
                    )

                    # count number frames sent this time
                    period_frame_count = 0

                    logging.debug(f'In TransmitAPRS Queue Count = {len(ServerQueue)}')


                    for de in ServerQueue:
                        logging.debug('processing server queue')
                        if ServerQueue[de] != "string2":
                            tcpbytes = bytearray(
                                ServerQueue[de], "utf-8"
                            )  # convert the APRS string to bytes prior to TX

                            try:  # Attempt to send
                                logging.debug(f'would send tcp data {tcpbytes.decode()}')

                                do_log_aprs(LogAPRS, APRSLogFile, tcpbytes)

                                aprs_stream.sendall(tcpbytes)
                                period_frame_count += 1

                            #  end try attempt to send
                            except Exception as e:
                                raise RuntimeError("Error writing APRS to Server", e) from e

                    # have sent the block
                    GlobalDefinitions.Global.LastTransmit = current
                    # now clear the queued items
                    ServerQueue.clear()
                    # update stats

                    StatsQ.put(
                        (
                            "Nr_APRS_permin",
                            int(
                                period_frame_count
                                * 60
                                / GlobalDefinitions.Global.ServerPeriod
                            ),
                        )
                    )
                    StatsQ.put(("Nr_APRS_TX", period_frame_count))

                    # now tidy up - given that we aggregate dont need to leave socket permanently open
                    aprs_stream.shutdown(SHUT_RDWR)
                    aprs_stream.close()
                    GlobalDefinitions.Global.NoConnect = True
            else:  # not ready to transmit yet
                # make sure we know where we arte with the socket
                try:  # I would assume this is going to fail everytime
                    aprs_stream.shutdown(SHUT_RDWR)
                    aprs_stream.close()
                except Exception:
                    pass

                GlobalDefinitions.Global.NoConnect = True

        except Exception as e:
            raise RuntimeError("Error dequeing in Transmit APRS \n %s", e) from e
    except Exception as e:
        raise Exception('TransmitAPRS', e) from e


def define_server_address(useremote: bool):
    if useremote:
        serveraddress = (
            GlobalDefinitions.Global.remoteEnd,
            int(GlobalDefinitions.Global.APRSPort),
        )
    else:
        serveraddress = (
            GlobalDefinitions.Global.ServerAddress,
            int(GlobalDefinitions.Global.APRSPort),
        )

    return serveraddress


def do_print_server_address(useremote: bool):
    if useremote:
        print(
            GlobalDefinitions.Global.remoteEnd,
            GlobalDefinitions.Global.APRSPort,
        )
    else:
        print(
            GlobalDefinitions.Global.ServerAddress,
            GlobalDefinitions.Global.APRSPort,
        )

    return None


def do_log_aprs(logaprs: bool, aprslogfile, tcpbytes):

    logging.debug(f'in do_log logfilename = {aprslogfile}')
    try:
        if logaprs:
            with open(aprslogfile, "a") as f:
                f.write(tcpbytes.decode())

    except Exception as e:
        raise RuntimeError("Exception while appending to logfile %s \n", e) from e
    return None


#################################################################################################################
def main(self):
    pass


if __name__ == 'main':
    main()
