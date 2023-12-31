import sys
import struct
import logging
from AISDictionary import AISDictionaries


def Dissemble_encoded_string(encoded_string: str):
    # takes an encoded string and breaks it up into its
    # (hopefiully seven components
    breakdown = encoded_string.split(',')
    if len(breakdown) == 7:
        talker = breakdown[0]
        fragcount = breakdown[1]
        fragno = breakdown[2]
        messid = breakdown[3]
        channel = breakdown[4]
        payload = breakdown[5]
        trailer = breakdown[6]
        return breakdown
    else:
        return ('!AIVDM', '1', '1', '', 'A', 'N000000000000000', '0')


class AIS_Data:
    '''
    first the constructor stuff
    because there are multiple forms need to use the **kwargs
    (multiple keyword arguments) approach and iterate through the argument list
    kwargs is a dictionary of keywod:value pairs

    Within the AIS record there are a number of payloads
    each has a set of attributes all of which are described in
        http://www.catb.org/gpsd/AIVDM.html

    CURRENTLY ONLY types 1, 2 3, 4, 5, 18 and 24 are processed in this script

    Payload ids 1,2 and 3 (Position Reports) have attributes
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Nav Status
        Rate of Turn ROT
        Speed over Ground SOG
        Position Accuracy
        Longitude
        Latitude
        Course over Groung COG
        True Heading
        Time Stamp
        Manouver Indicator
        RAIM Flag
        Radio Status

    Payload id 4 (Base Station Report) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Year
        Month
        Day
        Hour
        Minute
        Second
        Fix Quality
        Longitude
        Latitude
        Type of EPFD
        RAIM Flag
        SOTDMAState

    Payload 5 (Static and Voyage RElated Data) has Parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        AIS Version
        IMO Number
        Callsign
        Vessel Name
        Ship Type
        Dimension to Bow
        Dimension to Stern
        Dimension to Port
        Dimension to Starboard
        Position Fix Type
        ETA Month
        ETA Day
        ETA Hour
        ETA Minute
        Draught
        Destination
        DTE

    Payload Id 6 (Binary Addressed Message has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Sequence Number
        Destination MMSI
        Retransmit Flag
        Designated Area Code
        Functional Id
        Data

    Payload id 7 (Binary Acknowledge) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        MMSI No 1
        MMSI No 2
        MMSI No 3
        MMSI No 4

    Payload id 8 (Binary Broadcast Message) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Designated Area Code
        Functional Id
        Data

    payload id 9 (SAR Aircraft Position Report) has attributes
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits

    payload id 10 (UTC/.Date Enquiry) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Altitude
        SOG
        Position Accuracy
        Longitude
        Latitude
        COG
        TimeStamp
        DTE
        Assigned
        RAIM Flag
        Radio Status

    payload id 11 (UTC/Date Response) has sme parameters as id 4

    payload id 12 (Addressed Safety Related Message) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Sequence Number
        Destination MMSI
        Retransmit Flag
        Text

    payload id 13 (Safety Related Acknowledgement) has same parameters as id 7

    payload 14 (Safety Related Broadcast) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Text

    payload 15 (Interrogation) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Interrogated MMSI
        First msg Type
        First Slot offset
        Second Msg Type
        Second Slot offset
        Interrogated MMSI
        First messge TYpe
        First slot offset

    payload id 16 (Assignment Mode Command) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Destination A MMSI
        Offset A
        Increment A
        Destination B MMSI
        Offset B
        Increment B

    payload 17 (DGNSS Broadcast Binary Message) has parameters
        Message Type 1-3
        Repeat Indicator
        Source MMSI 9 digits
        Longitude
        Latitude
        Payload

    payload 18 (Class B Position Report) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Speed over Ground SOG
        Position Accuracy
        Longitude
        Latitude
        Course over Groung COG
        True Heading
        Time Stamp
        CS Unit
        Display Flag
        DSC Flag
        Band Flag
        Message22 Flag
        Manouver Indicator
        RAIM Flag
        Radio Status

    payload 19 (Extended Class B Position Report) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Speed Over Ground SOG
        Postion Accuracy
        Latitude
        Longitude
        Course Over Ground COG
        True Heading
        Type of Ship and Cargo
        Dimension to Bow
        Dimension to Stern
        Dimension to Port
        Dimension to Starboard
        Position Fix Type
        RAIM Flag
        DTE
        Assigned Mode Flag

    payload id 20 (Data LInk Mgt Message) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Offset no 1
        Reserved Slots
        Timeout
        Increment
        Offset no2
        Timeout
        Increment
        Offset no3
        Timeout
        Increment
        Offset no4
        Timeout
        Increment

    payload id 21 (Aid to Navigation REport) has parameterrs
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Aid Type
        Name
        Position Accuracy
        Longitude
        Latitude
        Dimension to Bow
        Dimension to Stern
        Dimension to Port
        Dimension to Starboard
        Type of EPFD
        UTC Second
        Off Position Indicator
        RAIM Flag
        Virtual Aid Flag
        Assigned Mode Flag
        Name Extension

    payload 22 (Channel Mgt) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Channel A
        Channel B
        Tx/Rx mode
        Power
        NE Longitude
        NE Latitude
        SW Longitude
        SW Latitude
        MSSI1
        MSSI2
        Addressed
        Channel A Band
        Channel B Band
        Zone Size

    payload 23 (Group Assignment Command) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        NE Longitude
        NE Latitude
        SW Longitude
        SW Latitude
        Station Type
        Ship Type
        Tx/RX Mode
        Report Interval
        Quite Time

    payload id 24 (Static Data Report) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Part Number
        Vessel Name
        Ship Type
        Vendor Id
        Unit Model Code
        Serial Number
        Callsaign
        Dimension to Bow
        Dimension to Stern
        Dimension to Port
        Dimension to Starboard
        Mothership MMSI

    payload id 25 (Single Slot Bianary MNessage) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Destination Indicator
        Binary Data Flag
        Destination MMSI
        Application Id
        Data

    payload id 26 (Multiple Slot Binary Message) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Destination Indicator
        Binary Data Flag
        Destination MMSI
        Application Id
        Data
        Radio Status

    payload id 27 (Long Range AIS Broadcast) has parameters
        Message Type 1-3
        Repeat Indicator
        MMSI 9 digits
        Position Accuracy
        RAIM Flag'Navigation Status
        Longitude
        Latitude
        Speed over Ground SOG
        Course over Ground COG
        GNSS Position Status

    '''

    _rot = 128  # not available
    _altitude = float(0)  # special for Type 9 (SAR aircraft) records
    _sog = 0
    _long = 0  # longitude
    _lat = 0  # latitude
    _cog = 0
    _truhead = 0
    _raim: int  # RAIM not in use
    _rad_status = 0  # special radio status generally unused
    _time = 0
    _man = 0
    _name = ''  # string
    _call = ''  # string
    _destination = ''  # string
    _nstatus = 15  # not defined
    _pa: int  # unaugmented GPS fix
    _disp: int = 0  # Display flag derived from type 18
    _dsc: int  = 0  # DSC flag - unit attached to VHF radio with DSC capability
    _band: int  = 0
    # base stations can command units to switch frequency
    # if True unit can use any part of band
    _m22: int = 0
    # Unit can accept channel assignment via message type 22
    _assigned: int = 0
    # Assigned mode flag False = autonomous, true = assigned mode
    _version = 0
    _IMO = 0
    _type = 0
    _d2bow = 0
    _d2stern = 0
    _d2port = 0
    _d2starboard = 0
    _fix_type = 0
    _ETA_month = 0
    _ETA_day = 0
    _ETA_hour = 0
    _ETA_minute = 0
    _draught = 0
    _DTE = 0
    _t14text = ''  # Type 14 Safety Announcement text
    _isavcga:int = 0
    _trailer = ''
    _flat = float(0)
    _flong = float(0)
    _talker = ''
    _Frag = 0
    _Fragno = 0
    _Message_ID = -1
    _channel = ''  # string
    _Payload_ID = 0
    _payload = ''  # string
    _repeat = 3  # dont
    _binary_length = 0
    _mmsi = 0
    _smmsi = '000000000'
    _binary_payload = ''

    # ########################## ######################### ###################
    # for diagnostic purposes - may be deleted in production module
    def print_AIS(self):
        # prints out all internal parametersd of AIS Data

        print('AIS Data')
        print('altitude ', self._altitude)
        # special for Type 9 (SAR aircraft) records
        print('SOG ', self._sog)
        print('long  ', self._long)
        print('lat  ', self._lat)
        print('COG ', self._cog)
        print('TruHead ', self._truhead)
        print('RAIM ', self._raim)
        print('rad_status ', self._rad_status)
        print('time ', self._time)
        print('man ', self._man)
        print('name ', self._name)
        print('call ', self._call)
        print('destination ', self._destination)
        print('nstatus ', self._nstatus)
        print('pa ', self._pa)
        print('displacement ', self._disp)
        print('dsc ', self._dsc)
        print('band ', self._band)
        print('m22 ', self._m22)
        print('assigned ', self._assigned)
        print('version ', self._version)
        print('IMO ', self._IMO)
        print('type ', self._type)
        print('d2bow ', self._d2bow)
        print('d2stern ', self._d2stern)
        print('d2port ', self._d2port)
        print('d2stb ', self._d2starboard)
        print('fixtype ', self._fix_type)
        print('ETAMonth ', self._ETA_month)
        print('ETADay ', self._ETA_day)
        print('ETAHour ', self._ETA_hour)
        print('ETAMinute ', self._ETA_minute)
        print('draught ', self._draught)
        print('DTE ', self._DTE)
        print('t14text ', self._t14text)
        print('isavcga ', self._isavcga)
        print('trailer ', self._trailer)
        print('flat ', self._flat)
        print('flong ', self._flong)
        print('FragCount ', self._Frag)
        print('FragNo ', self._Fragno)
        print('Message_ID ', self._Message_ID)
        print('channel ', self._channel)
        print('Payload_ID ', self._Payload_ID)
        print('Payload ', self._payload)
        print('binarylength ', self._binary_length)
        print('mmsi ', self._mmsi)
        print('binaryPayLoad ', self._binary_payload)

    # ########################## ######################## #################

    def get_AIS_FragCount(self):
        return self._Frag

    # AIS_FragCount = property(get_AIS_FragCount)

    def get_AIS_FragNo(self):
        return self._Fragno

    '''
    def get_xx(self):
        return self.yy
    xx = property(get_xx)
    '''

    def get_Message_ID(self) -> str:
        return self._Message_ID

    def set_Message_ID(self, value: str) -> None:
        if isinstance(value, str):
            self._Message_ID = value
        else:
            raise RuntimeError(
                "Incorrect type not string supplied to set Message_ID")

    # AIS_Message_ID = property(get_Message_ID)

    def get_AIS_Channel(self):
        return self._channel

    def set_ais_Channel(self, value: str):
        if isinstance(value, str):
            self._channel = value
        else:
            raise RuntimeError(
                "Incorrect type not string supplied to set AIS_Channel")

    # AIS_Channel = property(get_AIS_Channel)

    def get_AIS_Payload(self) -> str:
        return self._payload

    def set_AIS_Payload(self, value: str) -> None:
        if isinstance(value, str):
            self._payload = value
        else:
            raise RuntimeError(
                "Incorrect type not string supplied to set AIS_Payload")

    # AIS_Payload = property(get_AIS_Payload)

    def get_AIS_Binary_Payload(self):
        # print("To be returned ",self._binary_payload)
        return self._binary_payload

    def set_AIS_Binary_Payload(self, value: str):
        self._binary_payload = ''
        if isinstance(value, str):
            # print("setting ", value)
            # print("current ", self._binary_payload)
            self._binary_payload = value
            # print("after ", self._binary_payload)
        else:
            raise RuntimeError(
                "Incorrect type not string supplied to set AIS_Binary_Payload")

    def get_AIS_Binary_Payload_length(self):

        return self._binary_length

    def set_AIS_Binary_Payload_length(self, value):
        if isinstance(value, int):
            self._binary_length = value
        else:
            raise RuntimeError(
                "Error setting binary payload length - non integer presented")

    # AIS_Binary_Payload_length = property(
    #     get_AIS_Binary_Payload_length,
    #     set_AIS_Binary_Payload_length
    # )

    def set_AIS_Payload_ID(self, value: int) -> None:
        if not isinstance(value, int):
            raise RuntimeError(
                "Error setting binary payload ID - non integer presented")

        if value in range(1, 27):
            self._Payload_ID = value
        else:
            raise ValueError("Error setting binary payload ID - non valid ID type")

    def get_AIS_Payload_ID(self) -> int:
        return self._Payload_ID

    def __init__(self, talker: str, fragcount: str, fragno: str,
                 messid: str, channel: str, payload: str, trailer: str):
        # first predefine the known internals
        # if no args then we may assume it's the AISSData(enconded_string) form
        # and afterwards execute tne initialise_encoded function
        # otherwise it contains the following
        # talker,fragcount ,fragno ,_messid,channel ,payload,trailer variables
        #
        argcount = 0
        _parameter = ''

        _parameter = talker + ',' \
                     + fragcount + ',' \
                     + fragno + ',' \
                     + messid + ',' \
                     + channel + ',' \
                     + payload + ',' \
                     + trailer
        try:
            self.m_initialise()
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            raise RuntimeError("Unexpected error:", e) from e
        try:
            self.m_setup(_parameter)
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            raise RuntimeError("Unexpected error:", e) from e

    # now predefine all the functions necessary to initialise the class

    def m_initialise(self):
        _Frag = -1
        _Message_ID = 0
        _channel = ''  # String.Empty
        _Payload_ID = 0
        _payload = ''  # String.Empty

    def m_setup(self, Encoded_String: str):
        diction = AISDictionaries()
        nr_items = 0
        # dictionary used to avoid a case statement in AIS_Data
        # translates channel number
        # if non standard 1 or 2 used

        diagnostic3 = False
        diagnostic4 = False


        logging.debug('ïn AIS_Data.m_setup encoded string = {}'.format(Encoded_String))

        try:
            # under c# discrete_items would be a string array,
            # using pythin its a list
            discrete_items = Encoded_String.split(",")
            nr_items = int(len(discrete_items))
        except:
            print("Error Splitting AIS_DATA string", sys.exc_info()[0])
            # System.ArgumentException argEx =
            # new System.ArgumentException("Error Splitting AIS_DATA string")
            raise

        # foreach (string Data in discrete_items)
        for Data in discrete_items:
            # Console.WriteLine(Data)
            # now confirms its a valid AIVDM string
            # throw an error if not

            if discrete_items[0] == "!AIVDM":
                if nr_items > 4:
                    logging.debug('in m_setup valid string')
                    # number of fragments to make complete message
                    self.set_fragment(int(int(discrete_items[1])))
                    self.set_fragnumber(value=int(discrete_items[2]))
                    # current fragment number
                    xx = discrete_items[3]
                    # message id for multifragment message
                    if (len(xx) > 0):
                        self.set_Message_ID(discrete_items[3])

                    if discrete_items[4] in diction.ch_numb_dict:
                        self.set_ais_Channel(diction.ch_numb_dict[discrete_items[4]])  # radio channel used
                    else:
                        raise RuntimeError(
                            "channel number not in range {A,B,1,2")
                    try:
                        self.set_AIS_Payload(discrete_items[5])
                        # actual payload of the message, may need to be
                    except:
                        print("Error in extracting payload", sys.exc_info()[0])
                        raise

                    logging.debug('in m_setup _Frag = {}\r\n_Frag_no = {}\r\n_channel = {}\r\n_payload = {}'
                                  .format(
                                self._Frag,
                                    self._Fragno,
                                    self._channel,
                                    self._payload
                                  ))

                else:
                    print("Insufficient fields in string " + Encoded_String, sys.exc_info()[0])
                    raise

                intid: int = self.m_to_int(self._payload[0])  # payload type
                self.set_AIS_Payload_ID(intid)  # payload type)
                logging.debug('in m_setup_Payload_ID = {}'.format( self._Payload_ID))
                self._binary_payload, self._binary_length = (
                    self.create_binary_payload(self._payload))  # binary form of payload

                self.set_AIS_Binary_Payload(self._binary_payload)
                self.set_AIS_Binary_Payload_length(self._binary_length)

                # not currently used but available if converting to use bytearray instead of str for binary payload
                # _byte_payload = AIS_Data.create_bytearray_payload(self._payload)
                # self._binary_length = len(_byte_payload)

                logging.debug('in m_setup_binary_Payload = {}'.format( self._binary_payload))

                # if message type is 14 we need to create the safety message text
                #
                if self._Payload_ID == 14:
                    self.set_SafetyText(self.ExtractString(40, self._binary_length - 41))
            else:
                print("Invalid Talker ID", sys.exc_info()[0])
                raise RuntimeError("Invalid Talker ID")

    def set_Encoded_String(self, value: str) -> None:
        if isinstance(value, str):
            self._parameter = value
        else:
            raise (TypeError, "Value passed to set_Encoded_String not a string")

    def get_Encoded_String(self) -> str:
        return self._parameter

    def set_fragment(self, value: int) -> None:
        if 0 <= value <= 9:
            self._Frag = value
        else:
            self._Frag = 0
            raise ValueError("Number of fragments cannot exceed 9")

    def get_fragment(self) -> int:
        return self._Frag

    def set_fragnumber(self, *, value: int = 0) -> None:
        if 0 <= value <= 9:
            self._Fragno = value
        else:
            self._Fragno = 0
            raise ValueError("Number of fragments cannot exceed 9")

    def get_fragno(self) -> int:
        return self._Fragno

    def set_channel(self, value: str) -> None:
        diction = AISDictionaries()
        if not isinstance(value, str):
            raise (TypeError, "Value passed to set_channel not a string")

        if value in diction.ch_numb_dict:
            self._channel = diction.ch_numb_dict[value]
        else:
            raise ValueError

    def get_channel(self) -> str:
        return self._channel

    def set_trailer(self, value):
        if isinstance(value, str):
            self._trailer = value
        else:
            raise (TypeError, "Value passed to set_trailer not a string")

    def extract_random_mmsi(self,  startpos: int, length: int) -> tuple:
        immsi = self.Binary_Item(startpos, length)
        smmsi = "{:09d}".format(immsi)
        # string mmsi derived from immsi
        logging.debug(" return string MMSI = {}".format( smmsi))
        return immsi, smmsi

    def set_mmsi(self, value: int):
    # mmsi is nine digits which may start with any digit from 0 to 9.
    # string MMSI will be zero filled MSC if not 9 chars long
        immsi = value
        if 0 <= value <= 999999999:
            self._mmsi = value
            self._smmsi = "{:09}".format(value)
        else:
            self._mmsi = 0
            self._smmsi = '000000000"'
            raise ValueError("attempted to set MMSI outside 0-999999999")

    def get_mmsi(self):
        return self._mmsi

    def get_smmsi(self):
        return self._smmsi




    def get_String_MMSI(self) -> str:
        s_mmsi = str(self._mmsi)
        if len(s_mmsi) == 9:
            return s_mmsi
        else:
            while (len(s_mmsi) < 9):
                # zero fill on the left
                s_mmsi = "0" + s_mmsi
            # Console.WriteLine(" return string MMSI = " + s_mmsi)
        return s_mmsi


    def do_function(self, keyword, value):
        # create a dictionary of functions related to keywords that might be being initialised
        Funcdict = \
            {
                'Encoded_String': self.set_Encoded_String,
                'fragcount': self.set_fragment,
                'channel': self.set_channel,
                'payload': self.set_AIS_Payload,
                'trailer': self.set_trailer,
                'RepeatIndicator': self.set_RepeatIndicator,
                'SOG': self.set_SOG,
                'int_HDG': self.set_int_HDG,
                'Altitude': self.set_Altitude,
                'int_ROT': self.set_int_ROT,
                'NavStatus': self.set_NavStatus,
                'int_latitude': self.set_int_latitude,
                'int_longitude': self.set_int_longitude,
                'Pos_Accuracy': self.set_Pos_Accuracy,
                'int_COG': self.set_int_COG,
                'Timestamp': self.set_Timestamp,
                'MAN_Indicator': self.set_MAN_Indicator,
                'RAIM': self.set_RAIM,
                'Name': self.set_Name,
                'Callsign': self.set_Callsign,
                'IMO': self.set_IMO,
                'Version': self.set_Version,
                'Destination': self.set_Destination,
                'Display': self.set_Display,
                'DSC': self.set_DSC,
                'BAND': self.set_BAND,
                'Message22': self.set_Message22,
                'Assigned': self.set_Assigned,
                'ShipType': self.set_ShipType,
                'Dim2Bow': self.set_Dim2Bow,
                'Dim2Stern': self.set_Dim2Stern,
                'Dim2Port': self.set_Dim2Port,
                'Dim2Starboard': self.set_Dim2Starboard,
                'FixType': self.set_FixType,
                'ETA_Month': self.set_ETA_Month,
                'ERA_Day': self.set_ETA_Day,
                'ETA_Hour': self.set_ETA_Hour,
                'ETA_Minute': self.set_ETA_Minute,
                'Draught': self.set_Draught,
                'DTE': self.set_DTE,
                'SafetyText': self.set_SafetyText,
                'isAVCGA': self.set_isAVCGA
            }
        if keyword in Funcdict:
            return Funcdict[keyword](value)
        else:
            raise (ValueError, "parameter name unknown")

    def get_SOG(self) -> float:
        self._fsog = float(self._sog)
        return self._fsog / 10

    def set_SOG(self, value) -> None:
        self._sog = int(value)

    def get_int_HDG(self) -> int:
        # print('getting int HDG')
        return self._truhead

    def set_int_HDG(self, value) -> None:
        # print ('setting int HDG ', value)
        self._truhead = value

    # int_HDG = property(get_int_HDG, set_int_HDG)

    def ROT(self) -> float:
        # ROT is coded as 4.733 * SQRT(p_rot)
        # to decode divide bcoded value by 4.733 then square.
        # Returns rate in degrees per minute to three decimal places
        self._frot = float(0)
        # switch (_rot)
        if (self._rot > 0) and (self._rot < 127):
            self._frot = self._rot
            self._frot = (self._frot / 4.733)
            self._frot = round(self._frot * self._frot, 3)
        elif self._rot < 0:
            if self._rot == -127:  # turning left at more than 5 deg/30sec
                pass
            else:
                self._frot = self._frot  # preserve sign of RO
        elif self._rot == 127:  # turning right at more than 5 deg/30 sec
            pass
        elif self._rot == 128:  # not available
            pass

        # Console.WriteLine("Rate of turn = " + self._frot)

        return float(self._frot)

    def get_Altitude(self) -> int:
        return self._altitude

    def set_Altitude(self, value: int) -> None:
        if value >= 0 and value <= 4095:
            self._altitude = value
        else:
            raise ValueError

    def get_int_ROT(self) -> int:
        return self._rot

    def set_int_ROT(self, value) -> None:
        self._rot = value

    int_ROT = property(get_int_ROT, set_int_ROT)

    def get_NavStatus(self) -> int:
        return self._nstatus

    def set_NavStatus(self, value: int) -> None:
        if value in range(1, 15):
            self._nstatus = value
        else:
            raise ValueError

    def set_int_latitude(self, value) -> None:
        # print(' setting int latitude', value)
        # in 1/10000 of a minute  +/- 180 degrees
        if not isinstance(value, int):
            raise RuntimeError(
                "incorrect type {} in set_ini_latitude should be int".format(type(value)))
        if (value >= -108000000) and  (value <= 108000000):
            self._lat = value
            self._flat = float(self._lat / 6000000)
        else:
            raise ValueError(
                "Latitude range +/- 180 degrees")

    def get_int_latitude(self) -> int:  # unused
        return self._lat

    def set_int_longitude(self, value: int) -> None:
        # print (' setting int longitude', value)
        # in 1/10000 of a minute  +/- 180 degrees
        if not isinstance(value, int):
            raise RuntimeError(
                "incorrect type {} in set_ini_longitude should be int".format(type(value)))

        if (value >= -108000000) and (value <= 108000000):
            self._long = value
            self._flong = float(self._long / 6000000)
        else:
            raise ValueError(
                "Longitude range +/- 180 degrees")

    def get_int_longitude(self) -> int:  # unused
        return self._long

    def get_Latitude(self) -> float:
        return self._flat


    def get_Longitude(self) -> float:
        return self._flong

    def get_Pos_Accuracy(self) -> int:
        return self._pa

    def set_Pos_Accuracy(self, *, value: int = 0):
        self._pa = value

    Pos_Accuracy = property(get_Pos_Accuracy, set_Pos_Accuracy)

    def get_COG(self) -> float:
        return  self._cog

    def set_COG(self, value: int) -> None:
        if 0 <= value <= 3600:
            self._cog = float (value/10)
        else:
            print('in AISDATA setting COG got incorect value = ', value)
            raise ValueError


    def set_int_COG(self, value) -> None:
        self.set_COG(value)

    def get_int_COG(self) -> int:  # not used
        return int(self._cog)


    def get_HDG(self) -> int:
        return self._truhead

    def set_HDG(self, value: int) -> None:
        if value >= 0 and value <= 359:
            self._truhead = value
        else:
            print('Error setting heading incorrect value  got ', value)


    # need to pass back the number of bits in the payload
    # it looks as though type 5 static data packets may
    # not conform to standard (destination truncated
    def Binary_length(self) -> int:
        return int(self._binary_length)

    def get_Timestamp(self) -> int:
        # seconds of UTC Timestamp
        # 60 timestamp unavailable
        # 61 positioning system in manual input mode
        # 62 Position Fixing System operating in Dead Reckoning Mode
        # 63 if positioning system inoperative
        return int(self._time)

    def set_Timestamp(self, value: int) -> None:
        if value in range(0,63):
            self._time = int(value)
        else:
            raise ValueError('UTC seconds timestamp outside 0-63')


    def set_MAN_Indicator(self, value: int) -> None:
        if value in range(0,2):
            self._man = int(value)
        else:
            raise ValueError('Maneuver Indicator outside 0-2')

    def get_MAN_Indicator(self):
        return self._man

    def set_RepeatIndicator(self, value: bin) -> None:
        if value in range(0, 1):
            self._repeat = value
        else:
            raise ValueError("Repeart Indicator must be integer 0/1")

    def get_RepeatIndicator(self) -> int:
        return self._repeat


    def set_RAIM(self, value) -> None:
        if value in range(0,1):
            self._raim = value
        else:
            raise ValueError("RAIM must be integer 0/1")

    def get_RAIM(self) -> int:

            return self._raim

    def get_Name(self) -> str:
        # Console.WriteLine("returning p_name = " + p_name);
        # name can be padded with trailing @ which needs removing
        if self._name.find('@') > 0:
            self._name = self._name[0: self._name.find('@')]
            return str(self._name)
        else:
            if self._name.find('@') == 0:
                return ''
            else:
                return str(self._name)

    def set_Name(self, value) -> None:
        if isinstance(value, str):
            self._name = value
            self._name = self.Remove_at(self._name)
            self._name = self.Remove_space(self._name)
        else:
            self._name = ''
            raise TypeError("Name not a string")

    Name = property(get_Name, set_Name)

    def get_Callsign(self) -> str:
        if self._call.find('@') > 0:
            self._call = self._call[0: self._call.find('@')]
            return str(self._call)
        else:
            if self._call.find('@') == 0:
                return ''
            else:
                return str(self._call)

    def set_Callsign(self, value: str) -> None:
        if isinstance(value, str):
            self._call = value
            self._call = self.Remove_at(self._call)
            self._call = self.Remove_space(self._call)
        else:
            self._call = ''
            raise TypeError("Callsign must be string")


    def get_IMO(self) -> int:
        return int(self._IMO)

    def set_IMO(self, value: int) -> None:
        # IMO Number nominally a text indentifier "IMO" and seven digits
        if value in range(0,9999999):
            self._IMO = value
        else:
            self._IMO = 0  # CHECK THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            raise ValueError("IMO must be 7 digit integer > 0")


    def get_Version(self) -> int:
        return self._version

    def set_Version(self, value) -> None:
        if value in range(0,3):
            self._version = value
        else:
            self._version = 0
            raise ValueError('Version should be integer 0-3')


    def get_Destination(self) -> str:
        if self._destination.find('@') > 0:
            self._destination = self._destination[0: self._destination.find('@')]
            return str(self._destination)
        else:
            if self._destination.find('@') == 0:
                return ''
            else:
                return str(self._destination)

    def set_Destination(self, value) -> None:
        if isinstance(value, str):
            self._destination = value
            self._destination = self.Remove_at(self._destination)
            self._destination = self.Remove_space(self._destination)
        else:
            self._destination = ''
            raise TypeError('Destination must be string')

    Destination = property(get_Destination, set_Destination)

    def get_Display(self) -> bool:
        return self._disp

    def set_Display(self, value) -> None:
        if isinstance(value, bool):
            self._disp = value
        else:
            self._disp = False
            raise ValueError('Display must be boolean')


    # public bool DSC
    def get_DSC(self) -> bool:
        return self._dsc

    def set_DSC(self, value) -> None:
        if isinstance(value, bool):
            self._dsc = value
        else:
            self._dsc = False
            raise ValueError("DSC must be boolean")

    DSC = property(get_DSC, set_DSC)

    def get_BAND(self) -> int:
        return self._band

    def set_BAND(self, value: int) -> None:
        if value in range(0, 1):
            self._band = value
        else:
            self._band = 0
            raise ValueError("BAND must be boolean")


    def get_Message22(self) -> int:
        return self._m22

    def set_Message22(self, value: int) -> None:
            if value in range(0, 1):
                self._m22 = value
            else:
                self._m22 = 0
                raise ValueError("Message 22 Flag  must be boolean")


    # public bool Assigned
    def get_Assigned(self) -> int:
        return self._assigned

    def set_Assigned(self, value: int) -> None:
        if value in range(0,1):
            self._assigned = value
        else:
            self._assigned = 0
            raise ValueError('Assigned must be boolean')



    # public int ShipType
    def get_ShipType(self) -> int:
        return self._type

    def set_ShipType(self, value) -> None:
        # Ship TYpe range 0-99 values above 99 set to zero (coders in the wild unreliable)
        if 0 <= value <= 99:
            self._type = value
        elif value < 256:
            self._type = 0
        else:
            self._type = 0
            raise ValueError("Ship TYpe outside range 0-256 - with > 99 set to 0")



    # public int Dim2Bow
    def get_Dim2Bow(self):
        return int(self._d2bow)

    def set_Dim2Bow(self, value) -> None:
        # in metres
        if value in range(1,1023):
            self._d2bow = value
        else:
            self._d2bow = 0
            raise ValueError("Dim2bow must be integer 1 _ 1023")

    Dim2bow = property(get_Dim2Bow, set_Dim2Bow)

    # public int Dim2Stern
    def get_Dim2Stern(self) -> int:
        # in metres
        return int(self._d2stern)

    def set_Dim2Stern(self, value) -> None:
        # in metres
        if value in range(1,1023):
            self._d2stern = value
        else:
            self._d2stern = 0
            raise ValueError("Dim2stern must be integer 1 _ 1023")

    # public int Dim2Port
    def get_Dim2Port(self) -> int:
        return int(self._d2port)

    def set_Dim2Port(self, value) -> None:
        # in metres
        if value in range(1,63):
            self._d2port = value
        else:
            self._d2port = 0
            raise ValueError("Dim2bow must be integer 1 _ 63")

    # public int Dim2Starboard
    def get_Dim2Starboard(self) -> int:
        return int(self._d2starboard)
        # set { p_d2starboard = value; }

    def set_Dim2Starboard(self, value) -> None:
        # in metres
        if isinstance(value, int):
            self._d2starboard = value
        else:
            self._d2starboard = 0
            raise TypeError('Dim2Starboard must be integer')

    # Dim2Starboard = property(get_Dim2Starboard, set_Dim2Starboard)

    # public int FixType
    def get_FixType(self) -> int:
        return int(self._fix_type)

    def set_FixType(self, value: int) -> None:
        # range 0-8 valid, 15 often appears as undefined, 9-14 shouldn't happen
        if value in range(0, 8 or value == 15):
            self._fix_type = value
        else:
            self._fix_type = 15
            raise ValueError('FixType must be integer 0-8 or 15')


    # public int ETA_Month
    def get_ETA_Month(self) -> int:
        return int(self._ETA_month)

    def set_ETA_Month(self, value: int) -> None:
        if value in range(0, 12):
            self._ETA_month = value
        else:
            self.ETA_month = 0
            raise ValueError('ETA Month must be integer 0-12')



    # public int ETA_Day
    def get_ETA_Day(self) -> int:
        return int(self._ETA_Day)

    def set_ETA_Day(self, value: int) -> None:
        if value >= 0 and value <= 31:
            self._ETA_Day = value
        else:
            self.ETA_Day = 0
            raise ValueError('ETA Day must be integer 0-31')




    # public int ETA_Hour
    def get_ETA_Hour(self) -> int:
        return int(self._ETA_hour)

    def set_ETA_Hour(self, value) -> None:
        if value >= 0 and value <= 24:
            self._ETA_hour = value
        else:
            self._ETA_hour = 0
            raise ValueError('ETA Hour must be integer 0-24')


    # public int ETA_Minute
    def get_ETA_Minute(self) -> int:
        return int(self._ETA_minute)

    def set_ETA_Minute(self, value) -> None:
        # 60 == Not Applicable
        if 0 <= value <= 60:
            self._ETA_minute = value
        else:
            self.ETA_Minute = 0
            raise ValueError('ETA Minute must be integer 0-60')


    ETA_Minute = property(get_ETA_Minute, set_ETA_Minute)

    # public int Draught
    def get_Draught(self) -> int:
        # value returned is scaled up by 10
        return int(self._draught)

    def set_Draught(self, value: int) -> None:
        # metres  scaled by 10 stored as raw value
        if value in range(0, 511):
            self._draught = value
        else:
            self._draught = 0
            raise ValueError('Draught must be integer 0-511, scaled by factor of 10')




    # public int DTE
    def get_DTE(self) -> int:
        return int(self._DTE)

    def set_DTE(self, value: int) -> None:
        if value in range(0, 1):
            self._DTE = value
        else:
            self.DTE = 0
            raise ValueError('DTE boolean must be 0 or 1')



    def Radio_Status(self):
        raise NameError("Radio Status Unavailable")
    
    def get_Radio_Status(self):
        return "Radio Status Unavailable"

    def Type24PartNo(self) -> int:
        # if p_payload_ID is 24 then extract bits 38-39 and return integer value
        # valid values are 0 or 1, if called with non-valid payload type returns -1
        # throws exception if data stream returns 2 or 3

        if self._Payload_ID == 24:
            self.part = int(self.Binary_Item(38, 2))
            if (self.part < 2):
                return int(self.part)
            else:
                raise ValueError("Invalid Part No in Type 24 payload = " + str(self.part))
        else:
            return -1

    # public string Safetytext
    def get_SafetyText(self) -> str:
        return str(self._t14text)

    def set_SafetyText(self, value):
        if isinstance(value, str):
            self._t14text = value
        else:
            self._t14text = ''
            raise TypeError('SafetyText must be string')


    # public bool isAVCGA
    def get_isAVCGA(self) -> int:
        return int(self._isavcga)

    def set_isAVCGA(self, value: int):
        if value == 0 or value == 1:
            self._isavcga = value
        else:
            self._isavcga = 0
            raise ValueError('isAVCGA must be boolean 0/1', value)

    isAVCGA = property(get_isAVCGA, set_isAVCGA)

    def ExtractString(self, startpos: int, blength: int) -> str:
        # grab data 6 bit byte by byte checking that the
        # binary stream is not truncated from standard
        try:
            indexer = 0  # used to count number of bits extracted
            temp = 0
            cc = ' '
            buildit = ''

            while indexer < blength:
                if (startpos + indexer + 6) < self._binary_length:

                    temp = self.Binary_Item(startpos + indexer, 6)
                    #print("temp = ", temp)
                    temp = temp & 0x3F
                    temp = temp + 0x30
                    if temp > 0x57:
                        temp = temp + 0x8
                    #print('temp again', temp)
                    cc = chr(temp)
                    #print("character to be returned ", cc)
                    #                        Console.WriteLine("temp = " + temp + " cc = " + cc);
                    buildit = buildit + cc
                    #print('buildit ',buildit)
                    indexer = indexer + 6
                else:
                    indexer = blength
            #            Console.WriteLine("string returned = " + buildit);

            return buildit
        except:
            print(
                "Error in ExtractString startpos = " + str(startpos) + " blength = " + str(
                    blength) + "binary_length = " + str(self._binary_length))
            print("Exception while ExtractString startpos", sys.exc_info()[0])
            raise

    def ExtractInt(self, startpos: int, blength: int) -> int:  # int
        # extracts an integer from the binary payload
        # use Binary_Item to get the actual bits
        return int(self.Binary_Item(startpos, blength))

    def Binary_Item(self, startpos: int, blength: int) -> int:
        # newer version concept only
        # convert bitarray to a string, use string slicing to get bits
        # then convert the slice to int using int(string,2)

        reqbits = self._binary_payload[startpos:startpos + blength]
        logging.debug('in Binary Item type reqbits = {} value reqbits = {}'.format( type(reqbits), reqbits))
        if len(reqbits) != 0:
            return int(reqbits, 2)
        else:
            return 0

    # endregion
    # region Private Methods
    def create_binary_payload(self, p_payload: str) -> tuple:
        # based on using a supersized string rather than bytearray
        #
        #print("ïnput payload "+ p_payload)
        #
        # define a null string
        _abinary_payload = ''
        _byte_payload = bytearray()
        _byte_payload.extend(p_payload.encode())
        # print('bytearray version of payload\n', _byte_payload,
        #       '\nhex version\n', _byte_payload.hex(),
        #       '\nfrom \n',p_payload)
        for i in range(0, len(p_payload)):
            #print('in create binary payload ', len(p_payload), i)
            # iterate through the string payload masking to lower 6 bits
            xchar = p_payload[i]

            nibble = self.m_to_int(xchar) & 0x3F  # ensures only 6 bits presented
            #print(xchar, nibble, p_payload[i], i, len(p_payload))

            logging.debug('nibble {}'.format(bin(nibble)))

            # now append the nibble to the stream
            _abinary_payload = _abinary_payload + format(nibble, '06b')



        _binary_payload = _abinary_payload

        #print(_abinary_payload)

        return _abinary_payload, len(_abinary_payload)

    def create_bytearray_payload(p_payload: str) -> tuple:
        # based on using a supersized string rather than bytearray
        #
        printdiag = False
        #
        # define a null bytearray
        _byte_payload = bytearray()
        # convert from str to the bytearray
        _byte_payload.extend(p_payload.encode())
        # print('bytearray version of payload\n', _byte_payload,
        #       '\nhex version\n', _byte_payload.hex(),
        #       '\nfrom \n',p_payload)

        newbytes = bytearray()
        _binlength = len(p_payload)
        for i in range(0, len(p_payload)):
            if printdiag:
                print('in create binary payload ', len(p_payload), i)
            # iterate through the string payload masking to lower 6 bits
            thebyte: int = int(_byte_payload[i])
            thebyte = thebyte - 48
            if thebyte > 40:
                newbytes.extend((thebyte - 8).to_bytes(1, "big"))
            else:
                newbytes.extend(thebyte.to_bytes(1, "big"))

        # now repack the bytearray as a string of 6 bit nibbles
        _byte_payload = bytearray()

        # need to keep track of the 8 bit byte into which we are putting the nibble part
        #  (splits across bytes generally)
        # for each 4 nibbles 3 output bytes will be created.
        #
        outbyte = 0

        for innibble in range(_binlength):
            # use modulas to keep track of where we are in sequence
            ii = innibble % 4

            match ii:
                case 0:
                    # mask to 6 bits and shift to MSB of outbyte
                    _byte = (newbytes[innibble] & 0x3F) << 2
                    _byte_payload.extend(struct.pack("B", (newbytes[innibble] & 0x3F) << 2))
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 1:
                    # mask to 2 MSB and put them into outbyte
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x30) >> 4) + _byte_payload[outbyte]
                    # now put 4 LSB into MSB of next outbyte
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1
                    _byte = (newbytes[innibble] & 0x0F) << 4
                    _byte_payload.extend(struct.pack("B", _byte))
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 2:
                    # mask  four MSB, move to lower bits  of outbyte
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x3F) >> 2) + _byte_payload[outbyte]
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1
                    # put 2 LSB into MSB of next outbyte
                    _byte_payload.extend(struct.pack("B", (newbytes[innibble] & 0x03) << 6))
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 3:
                    # put 6 MSBbits into LSB of next outbyte
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x3F)) + _byte_payload[outbyte]
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " 
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1

                case _:
                    _byte_payload = bytearray()
                    _binlength = 0
                    raise RuntimeError("error in selecting bytes in create_bytearray_payload")

        logging.debug('{}'.format(_byte_payload.hex()))
        return _byte_payload, len(_byte_payload)

    def m_to_int2(self, parameter: str) -> int:
        return int(parameter)

    def m_to_int(self, parameter: str) -> int:
        # takes in a encoded string of variable length and returns positive integer
        # print('entering m_to_int parameter = ', parameter)
        my_int = int(0)
        my_byte = ord(parameter)
        # print(len(parameter), ' ', my_byte)

        if len(parameter) == 1:
            my_int = int(my_byte)
            # need to mask off the upper 2 bits

            if (my_int - 48) > 40:
                my_int = my_int - 56
            else:
                my_int = my_int - 48

            # print('myint ', my_int, ' binary myint ', bin(my_int))
        else:
            print("multiple characters not yet handled in m_to_int\r\n", sys.exc_info()[0])
            raise RuntimeError('In m_to_int\r\n')
            # multi character integer values are made up of 6 bit "bytes"
            # in either signed or unsigned versions
        return my_int

    def Remove_at(self, p: str) -> str:
        if (p.find('@') > 0):
            pp = ''
            for i in p:
                if not (i == '@'):
                    pp = pp + i
            return pp

        else:

            if (p.find('@') == 0):
                return p  # equivalent to String.Empty
            else:
                return p

    def Remove_space(self, p: str) -> str:
        if (p.find(' ') > 0):
            pp = ''
            for i in p:
                if not (i == ' '):
                    pp = pp + i
            return pp

        else:

            if (p.find(' ') == 0):
                return p  # equivalent to String.Empty
            else:
                return p


_hasbeenDisposed = False

# region Disposals
