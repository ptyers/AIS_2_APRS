import datetime
import MyPreConfigs
#import GlobalDefinitions
import logging
from Payloads import Static_data_report


class APRS:
    # static bool Diagnose_APRS = True

    #  defines APRS actions and parameters
    #  based on APRS Protocol Reference - Protocol Version 1.0.1
    #
    _relay_station: str = 'CG722'



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
        **kwargs
                ):

        self._longitude = ""
        self._latitude = ""
        self._course = ""
        self._speed = ""
        self._mmsi = ""
        self._name = ""
        self._callsign = ""
        self._comment = " "
        self._safetytext = ""
        self._isavcga = False


    def ConvertLongitude(self, longitude: float) -> str:

        #  takes in a float and converts to APRS format
        #  fixed 8 character field in degrees and decimalminutes to two places
        #  followed by either N or S
        #  eg 4903.50N represents 49 degrees 3 minutes 30 seconds North
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
        #  followed by either N or S
        #  eg 4903.50N represents 49 degrees 3 minutes 30 seconds North
        #
        if latitude <= 0:
            latitude = -latitude
            self._latitude = self.SplitLatitude(latitude) + "S"
        else:
            self._latitude = self.SplitLatitude(latitude) + "N"

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
        _speed = format(speed, "03d")

    def CreateObjectPosition(self, kill: bool, mydata) -> str:
        try:
            statuschar = ""
            typechar = "s"
            tablechar = "\\"  # single \

            self._mmsi = mydata.mmsi
            isAVCGA = mydata.isAVCGA

            if kill:
                logging.debug("supposedly killing {}  ".format(mydata.mmsi))


            try:
                if not kill:
                    statuschar = "*"
                    if self._mmsi in Static_data_report.T24Records:
                        record,time = Static_data_report.T24Records[self._mmsi]
                        if record['vessel_mame'] != '':
                            self.name = record['vessel_mame']
                        if record['callsign'] != '':
                            self.callsign = record['callsign']
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
            if self._mmsi[0:3] in _tablecharoption:
                tablechar = _tablecharoption[self._mmsi[0:3]]


            #  and finally cater for AVCGA vessels - transmit these as valid position reports
            #
            if isAVCGA:
                typechar = "C"  # Coastguard Vessel might be an 'L' modified table

            #  creates position report for object with time stamp
            thetime = datetime.datetime.utcnow()
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
                    #print(self._name, len(self._name))
                while self._callsign[:-1] == " " and len(self._callsign) > 1:
                    self._callsign = self._callsign[0:-2]

                self.txname = (self._name + " " + mydata.mmsi + " " + self._callsign)[
                    0:42
                ]

            message = (
                APRS._relay_station
                + ">APU25N,TCPIP*:;"
                + Xcallsign
                + statuschar
                + timestamp
                + self._latitude
                + tablechar
                + self._longitude
                + typechar
                + self._course
                + "/"
                + self._speed
                + self.txname
                + "\n"
                    )

            logging.debug(
                "in CreateObject with kill tcpbytes \n"
                + APRS._relay_station
                + ">APU25N,TCPIP*:;"
                + Xcallsign
                + statuschar
                + timestamp
                + self._latitude
                + tablechar
                + self._longitude
                + typechar
                + self._course
                + "/"
                + self._speed
                + self.txname
                + "\n"
            )

            return message
        except Exception as e:
            raise Exception('CreateObjectPosition', e) from e

    def CreateBasePosition(self) -> str:
        #  creates position report for base station (symbol triangle) with time stamp
        try:
            thetime = datetime.datetime.utcnow()
            # string timestamp = thetime.Day.ToString("0#") + thetime.Hour.ToString("0#") + thetime.Minute.ToString("0#") + "z"
            timestamp = thetime.strftime("%d%H%Mz")
            message = (
                APRS._relay_station
                + ">APU25N,TCPIP*:;"
                + self._mmsi
                + "*"
                + timestamp
                + self._latitude
                + "\\"
                + self._longitude
                + "L"
                + "\n"
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

    def CreateSafetyMessage(self, Bulletin: int) -> str:
        try:
            message = ""
            #  create a bulletin frame
            message = ""
            if self._safetytext != "":
                while len(self._safetytext) > 67:
                    self._safetytext = self._safetytext[0, 66]
                    message = (
                        message
                        + APRS._relay_station
                        + ">APU25N,TCPIP*::BLN"
                        + str(Bulletin)
                        + "     :"
                        + self._safetytext
                        + "\n"
                    )
                    self._safetytext = self._safetytext[67:]
                    Bulletin += 1
                    Bulletin = Bulletin % 10

                message = (
                    message
                    + APRS._relay_station
                    + ">APU25N,TCPIP*::BLN"
                    + str(Bulletin)
                    + "     :"
                    + self._safetytext
                    + "\n"
                )

            return message
        except Exception as e:
            logging.error('In CreateSafetyMessage \n' + str(e), stack_info=True)
            raise Exception('CreateSafetyMessage', e) from e


def main(self):
    pass


if __name__ == 'main':
    main()
