import math
import sys
import array as arr
import MyPreConfigs


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
    _raim = False  # RAIM not in use
    _rad_status = 0  # special radio status generally unused
    _time = 0
    _man = 0
    _name = ''  # string
    _call = ''  # string
    _destination = ''  # string
    _nstatus = 15  # not defined
    _pa = False  # unaugmented GPS fix
    _disp = False  # Display flag derived from type 18
    _dsc = False  # DSC flag - unit attached to VHF radio with DSC capability
    _band = False
    # base stations can command units to switch frequency
    # if True unit can use any part of band
    _m22 = False
    # Unit can accept channel assignment via message type 22
    _assigned = True
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
    _isavcga = False
    _trailer = ''
    _flat = float(0)
    _flong = float(0)
    _talker = ''
    _Frag = 0
    _Fragno = 0
    _messid = ''
    _Message_ID = -1
    _channel = ''  # string
    _Payload_ID = 0
    _payload = ''  # string
    _repeat = 3  # dont
    _binary_length = 0
    _mmsi = 0
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
        print('talker ', self._talker)
        print('FragCount ', self._Frag)
        print('FragNo ', self._Fragno)
        print('messid ', self._messid)
        print('Message_ID ', self._Message_ID)
        print('channel ', self._channel)
        print('Payload_ID ', self._Payload_ID)
        print('Payload ', self._payload)
        print('repeat ', self._repeat)
        print('binarylength ', self._binary_length)
        print('mmsi ', self._mmsi)
        print('binaryPayLoad ', self._binary_payload)

    # ########################## ######################## #################

    def get_AIS_FragCount(self):
        return self._Frag

    AIS_FragCount = property(get_AIS_FragCount)

    def get_AIS_FragNo(self):
        return self._Fragno

    AIS_FragNo = property(get_AIS_FragNo)
    '''
    def get_xx(self):
        return self.yy
    xx = property(get_xx)
    '''

    def get_Message_ID(self):
        return self._Message_ID

    AIS_Message_ID = property(get_Message_ID)

    def get_AIS_Channel(self):
        return self._channel

    AIS_Channel = property(get_AIS_Channel)

    def get_AIS_Payload(self):
        return self._payload

    AIS_Payload = property(get_AIS_Payload)

    def get_AIS_Binary_Payload(self):
        return self._binary_payload

    def set_AIS_Binary_Payload(self, value):
        if isinstance(value, str):
            self._binary_payload = value
        else:
            raise RuntimeError(
                "Incorrect type not string supplied to set AIS_Binary_Payload")

    AIS_Binary_Payload = property(
        get_AIS_Binary_Payload,
        set_AIS_Binary_Payload)

    def get_AIS_Binary_Payload_length(self):
        return self._binary_length

    def set_AIS_Binary_Payload_length(self, value):
        if isinstance(value, int):
            self._binary_length = value
        else:
            raise RuntimeError(
                "Error setting binary payload length - non integer presented")

    AIS_Binary_Payload_length = property(
        get_AIS_Binary_Payload_length,
        set_AIS_Binary_Payload_length
    )

    def set_AIS_Payload_ID(self, value):
        if isinstance(value, int):
            self._binary_length = value
        else:
            raise RuntimeError(
                "Error setting binary payload length - non integer presented"
            )

    def get_AIS_Payload_ID(self):
        return self._Payload_ID

    AIS_Payload_ID = property(get_AIS_Payload_ID, set_AIS_Payload_ID)

    def __init__(self, talker: str, fragcount: str, fragno: str,
                 messid: str, channel: str, payload: str, trailer: str):
        # first predefine the known internals
        # if no args then we may assume its the AISSData(enconded_string) form
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
        nr_items = 0
        # dictionary used to avoid a case statement in AIS_Data
        # translates channel number
        # if non standard 1 or 2 used

        ch_numb_dict = {'1': 'A', '2': 'B', 'A': 'A', 'B': 'B'}
        diagnostic3 = False
        diagnostic4 = False

        if (diagnostic3):
            print('ïn AIS_Data.m_setup encoded string = ', Encoded_String)

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
                    if diagnostic4:
                        print('in m_setup valid string')
                    self._Frag = int(discrete_items[1])
                    # number of fragments to make complete message
                    self._Frag_no = int(discrete_items[2])
                    # current fragment number
                    xx = discrete_items[3]
                    # message id for multifragment message
                    if (len(xx) > 0):
                        self._Message_ID = int(discrete_items[3])
                    self._channel = discrete_items[4]  # radio channel used
                    if self._channel in ch_numb_dict:
                        self._channel = ch_numb_dict[self._channel]
                    else:
                        raise RuntimeError(
                            "channel number not in range {A,B,1,2"
                        )
                    try:
                        self._payload = discrete_items[5]
                        # actual payload of the message, may need to be
                    except:
                        print("Error in extracting payload", sys.exc_info()[0])
                        raise
                    if diagnostic4:
                        print('in m_setup _Frag = ', self._Frag,
                              '\r\n_Frag_no = ', self._Frag_no,
                              '\r\n_channel = ', self._channel,
                              '\r\n_payload = ', self._payload
                              )

                else:
                    print("Insufficient fields in string " + Encoded_String, sys.exc_info()[0])
                    raise

                self._Payload_ID = AIS_Data.m_to_int(self._payload[0])  # payload type
                if diagnostic4:
                    print('in m_setup_Payload_ID = ', self._Payload_ID)
                self._binary_payload, self._binary_length = AIS_Data.create_binary_payload(
                    self._payload)  # binary form of payload
                if diagnostic4:
                    print('in m_setup_binary_Payload = ', bin(self._binary_payload))
                # Console.WriteLine("Payload_ID = " + p_Payload_ID)

                # if message type is 14 we need to create the safety message text
                #
                if self._Payload_ID == 14:
                    _t14text = self.ExtractString(40, self._binary_length - 41)
            else:
                print("Invalid Talker ID", sys.exc_info()[0])
                raise RuntimeError("Invalid Talker ID")

    def set_Encoded_String(self, value):
        if isinstance(value, str):
            self._parameter = value
        else:
            raise (TypeError, "Value passed to set_Encoded_String not a string")

    def set_fragment(self, value):
        self._fragment = value

    def set_fragno(self, value):
        if isinstance(value, str):
            self._fragno = value
        else:
            raise (TypeError, "Value passed to set_fragno not a string")

    def set_messid(self, value):
        if isinstance(value, str):
            self._messid = value
        else:
            raise (TypeError, "Value passed to set_messid not a string")

    def set_channel(self, value):
        if isinstance(value, str):
            self._channel = value
        else:
            raise (TypeError, "Value passed to set_channel not a string")

    def set_payload(self, value):
        if isinstance(value, str):
            self._payload = value
        else:
            raise (TypeError, "Value passed to set_payload not a string")

    def set_trailer(self, value):
        if isinstance(value, str):
            self._trailer = value
        else:
            raise (TypeError, "Value passed to set_trailer not a string")

    def get_MMSI(self):
        # print('getting MMSI in get_MMSI')
        return self._mmsi

    def set_MMSI(self, value):
        # print('  setting MMSI in set_MMSI')
        self._mmsi = value

    MMSI = property(get_MMSI, set_MMSI)

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

    String_MMSI = property(get_String_MMSI)

    def set_talker(self, value):
        if isinstance(value, str):
            self._talker = value
        else:
            raise (TypeError, "Value passed to set_talker not a string")

    def do_function(self, keyword, value):
        # create a dictionary of functions related to keywords that might be being initialised
        Funcdict = \
            {
                'Encoded_String': self.set_Encoded_String,
                'talker': self.set_talker,
                'fragcount': self.set_fragment,
                'fragno': self.set_fragno,
                'messid': self.set_messid,
                'channel': self.set_channel,
                'payload': self.set_payload,
                'trailer': self.set_trailer,
                'MMSI': self.set_MMSI,
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

    # region Public Properties

    def get_RepeatIndicator(self):
        return self._repeat

    def set_RepeatIndicator(self, value):
        self._repeat = value

    RepeatIndicator = property(get_RepeatIndicator, set_RepeatIndicator)

    def get_SOG(self):
        self._fsog = float(self._sog)
        return self._fsog / 10

    def set_SOG(self, value):
        self._sog = int(value)

    SOG = property(get_SOG, set_SOG)

    def get_int_HDG(self):
        # print('getting int HDG')
        return self._truhead

    def set_int_HDG(self, value):
        # print ('setting int HDG ', value)
        self._truhead = value

    int_HDG = property(get_int_HDG, set_int_HDG)

    def ROT(self):
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

    def get_Altitude(self):
        return self._altitude

    def set_Altitude(self, value):
        self._altitude = value

    Altitude = property(get_Altitude, set_Altitude)

    def get_int_ROT(self):
        return self._rot

    def set_int_ROT(self, value):
        self._rot = value

    int_ROT = property(get_int_ROT, set_int_ROT)

    def get_NavStatus(self):
        return self._nstatus

    def set_NavStatus(self, value):
        self._nstatus = value

    NavStatus = property(get_NavStatus, set_NavStatus)

    def set_int_latitude(self, value):
        # print(' setting int latitude', value)
        if isinstance(value, int):
            self._lat = value
            self._flat = float(self._lat) / 600000
        else:
            raise RuntimeError(
                "incorrect type {} in set_ini_latitude should be int".format(type(value)))

    def get_int_latitude(self):  # unused
        return 0

    int_latitude = property(get_int_latitude, set_int_latitude)

    def set_int_longitude(self, value):
        # print (' setting int longitude', value)
        if isinstance(value, int):
            self._long = value
            self._flong = float(self._long) / 600000
        else:
            raise RuntimeError(
                "incorrect type {} in set_ini_longitufde should be int".format(type(value))
            )

    def get_int_longitude(self):  # unused
        return 0

    int_longitude = property(get_int_longitude, set_int_longitude)

    def get_Latitude(self):
        return self._flat

    Latitude = property(get_Latitude)

    def get_Longitude(self):
        return self._flong

    Longitude = property(get_Longitude)

    def get_Pos_Accuracy(self):
        return self._pa

    def set_Pos_Accuracy(self, value):
        self._pa = value

    Pos_Accuracy = property(get_Pos_Accuracy, set_Pos_Accuracy)

    def get_COG(self):
        return float(round((float(self._cog) / 10), 1))

    def set_COG(self, value):
        if isinstance(value, float):
            self._cog = int(value)
        elif isinstance(value, int):
            self._cog = value
        else:
            print('in AISDATA setting COG got incorect type not int or float type = ', type(value))
        self._cog = value

    COG = property(get_COG, set_COG)

    def set_int_COG(self, value):
        if isinstance(value, float):
            self._cog = int(value)
        elif isinstance(value, int):
            self._cog = value
        else:
            print(
                'in AISDATA setting int_COG got incorect type not int or float type = ',
                type(value))

    def get_int_COG(self):  # not used
        return 0

    int_COG = property(get_int_COG, set_int_COG)

    def get_HDG(self):
        # print('getting HDG ', float(self._truhead))
        return float(self._truhead)

    def set_HDG(self, value):
        # print('setting HDG ', float(value))
        if isinstance(value, float):
            self._truhead = int(value)
        elif isinstance(value, int):
            self._truhead = value
        else:
            print('Error setting heading incorrect type excpected int or float got ', type(value))

    HDG = property(get_HDG, set_HDG)

    # need to pass back the number of bits in the payload
    # it looks as though type 5 static data packets may
    # not conform to standard (destination truncated
    def Binary_length(self):
        return int(self._binary_length)

    def get_Timestamp(self):
        # seconds of UTC Timestamp
        # 60 timestamp unavailable
        # 61 positioning system in manual input mode
        # 62 Position Fixing System operating in Dead Reckoning Mode
        # 63 if positioning system inoperative
        return int(self._time)

    def set_Timestamp(self, value):
        self._time = int(value)

    Timestamp = property(get_Timestamp, set_Timestamp)

    def get_MAN_Indicator(self):
        return int(self._man)

    def set_MAN_Indicator(self, value):
        self._man = int(value)

    MAN_Indicator = property(get_MAN_Indicator, set_MAN_Indicator)

    def get_RAIM(self):
        # boolean
        # Receiver Augmented Integrity Monitoring
        return self._raim

    def set_RAIM(self, value):
        if isinstance(value, bool):
            self._raim = value
        else:
            raise TypeError("RAIM must be boolean")

    RAIM = property(get_RAIM, set_RAIM)

    def get_Name(self):
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

    def set_Name(self, value):
        if isinstance(value, str):
            self._name = value
            self._name = self.Remove_at(self._name)
            self._name = self.Remove_space(self._name)
        else:
            self._name = ''
            raise TypeError("Name not a string")

    Name = property(get_Name, set_Name)

    def get_Callsign(self):
        if self._call.find('@') > 0:
            self._call = self._call[0: self._call.find('@')]
            return str(self._call)
        else:
            if self._call.find('@') == 0:
                return ''
            else:
                return str(self._call)

    def set_Callsign(self, value):
        if isinstance(value, str):
            self._call = value
            self._call = self.Remove_at(self._call)
            self._call = self.Remove_space(self._call)
        else:
            self._call = ''
            raise TypeError("Callsign must be string")

    Callsign = property(get_Callsign, set_Callsign)

    def get_IMO(self):
        return int(self._IMO)

    def set_IMO(self, value):
        if isinstance(value, int):
            self._IMO = value
        else:
            self._IMO = 0  # CHECK THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            raise TypeError("IMO must be integer")

    IMO = property(get_IMO, set_IMO)

    def get_Version(self):
        return int(self._version)

    def set_Version(self, value):
        if isinstance(value, int):
            self._version = value
        else:
            self._version = 0
            raise TypeError('Version should be integer')

    Version = property(get_Version, set_Version)

    def get_Destination(self):
        if self._destination.find('@') > 0:
            self._destination = self._destination[0: self._destination.find('@')]
            return str(self._destination)
        else:
            if self._destination.find('@') == 0:
                return ''
            else:
                return str(self._destination)

    def set_Destination(self, value):
        if isinstance(value, str):
            self._destination = value
            self._destination = self.Remove_at(self._destination)
            self._destination = self.Remove_space(self._destination)
        else:
            self._destination = ''
            raise TypeError('Destination must be string')

    Destination = property(get_Destination, set_Destination)

    def get_Display(self):
        return self._disp

    def set_Display(self, value):
        if isinstance(value, bool):
            self._disp = value
        else:
            self._disp = False
            raise TypeError('Display must be boolean')

    Display = property(get_Display, set_Display)

    # public bool DSC
    def get_DSC(self):
        return self._dsc

    def set_DSC(self, value):
        if isinstance(value, bool):
            self._dsc = value
        else:
            self._dsc = False
            raise TypeError("DSC must be boolean")

    DSC = property(get_DSC, set_DSC)

    def get_BAND(self):
        return self._band

    def set_BAND(self, value):
        if isinstance(value, bool):
            self._band = value
        else:
            self._band = False
            raise TypeError("BAND must be boolean")

    BAND = property(get_BAND, set_BAND)

    def get_Message22(self) -> bool:
        return self._m22

    def set_Message22(self, value):
        if isinstance(value, bool):
            self._m22 = value
        else:
            self._m22 = False
            raise TypeError("Message22 must be boolean")

    Message22 = property(get_Message22, set_Message22)

    # public bool Assigned
    def get_Assigned(self):
        return self._assigned

    def set_Assigned(self, value):
        if isinstance(value, bool):
            self._assigned = value
        else:
            self._assigned = False
            raise TypeError('Assigned must be boolean')

    Assigned = property(get_Assigned, set_Assigned)

    # public int ShipType
    def get_ShipType(self) -> int:
        return self._type

    def set_ShipType(self, value):
        if isinstance(value, int):
            self._type = value
        else:
            self._type = 0  # CHECK THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            raise TypeError("ShipType must integer")

    ShipType = property(get_ShipType, set_ShipType)

    # public int Dim2Bow
    def get_Dim2Bow(self):
        return int(self._d2bow)

    def set_Dim2Bow(self, value):
        if isinstance(value, int):
            self._d2bow = value
        else:
            self._d2bow = 0
            raise TypeError("Dim2bow must be integer")

    Dim2bow = property(get_Dim2Bow, set_Dim2Bow)

    # public int Dim2Stern
    def get_Dim2Stern(self) -> int:
        return int(self._d2stern)

    def set_Dim2Stern(self, value):
        if isinstance(value, int):
            self._d2stern = value
        else:
            self._d2stern = 0
            raise TypeError('Dim2Stern must be integer')

    # public int Dim2Port
    def get_Dim2Port(self) -> int:
        return int(self._d2port)

    def set_Dim2Port(self, value):
        if isinstance(value, int):
            self._d2port = value
        else:
            self._d2port = 0

    # public int Dim2Starboard
    def get_Dim2Starboard(self) -> int:
        return int(self._d2starboard)
        # set { p_d2starboard = value; }

    def set_Dim2Starboard(self, value):
        if isinstance(value, int):
            self._d2starboard = value
        else:
            self._d2starboard = 0
            raise TypeError('Dim2Starboard must be integer')

    Dim2Starboard = property(get_Dim2Starboard, set_Dim2Starboard)

    # public int FixType
    def get_FixType(self) -> int:
        return int(self._fix_type)

    def set_FixType(self, value):
        if isinstance(value, int):
            self._fix_type = value
        else:
            self._fix_type = 0
            raise TypeError('FixType must be integer')

    FixType = property(get_FixType, set_FixType)

    # public int ETA_Month
    def get_ETA_Month(self) -> int:
        return int(self._ETA_month)

    def set_ETA_Month(self, value):
        if isinstance(value, int):
            self._ETA_month = value
        else:
            self._ETA_month = 0
            raise TypeError('ETA_Month must be integer')

    ETA_Month = property(get_ETA_Month, set_ETA_Month)

    # public int ETA_Day
    def get_ETA_Day(self) -> int:
        return int(self._ETA_day)

    def set_ETA_Day(self, value):
        if isinstance(value, int):
            self._ETA_day = value
        else:
            self._ETA_day = 0
            raise TypeError('ETA_Day must be integer')

    ETA_Day = property(get_ETA_Day, set_ETA_Day)

    # public int ETA_Hour
    def get_ETA_Hour(self) -> int:
        return int(self._ETA_hour)

    def set_ETA_Hour(self, value):
        if isinstance(value, int):
            self._ETA_hour = value
        else:
            self._ETA_hour = 0
            raise TypeError('ETA_Hour must be integer')

    ETA_Hour = property(get_ETA_Hour, set_ETA_Hour)

    # public int ETA_Minute
    def get_ETA_Minute(self) -> int:
        return int(self.self._ETA_minute)

    def set_ETA_Minute(self, value):
        if isinstance(value, int):
            self._ETA_minute = value
        else:
            self._ETA_minute = 0
            raise TypeError('ETA_Minute must be integer')

    ETA_Minute = property(get_ETA_Minute, set_ETA_Minute)

    # public int Draught
    def get_Draught(self) -> int:
        return int(self._draught)

    def set_Draught(self, value):
        if isinstance(value, int):
            self._draught = value
        else:
            self._draught = 0
            raise TypeError('Draught must be integer')

    Draught = property(get_Draught, set_Draught)

    # public int DTE
    def get_DTE(self) -> int:
        return int(self._DTE)

    def set_DTE(self, value):
        if isinstance(value, int):
            self._DTE = value
        else:
            self._DTE = 0
            raise TypeError('DTE must be integer')

    DTE = property(get_DTE, set_DTE)

    def Radio_Status(self):
        raise NameError("Radio Status Unavailable")

    def Type24PartNo(self):
        # if p_payload_ID is 24 then extract bits 38-39 and return integer value
        # valid values are 0 or 1, if called with non-valid payload type returns -1
        # throws exception if data stream returns 2 or 3

        if self._Payload_ID == 24:
            self.part = int(self.Binary_Item(38, 2))
            if (self.part < 2):
                return int(self.part)
            else:
                raise NameError("Invalid Part No in Type 24 payload = " + str(self.part))
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

    SafetyText = property(get_SafetyText, set_SafetyText)

    # public bool isAVCGA
    def get_isAVCGA(self):
        return int(self._isavcga)

    def set_isAVCGA(self, value):
        if isinstance(value, bool):
            self._isavcga = value
        else:
            self._isavcga = False
            raise TypeError('isAVCGA must be boolean')

    isAVCGA = property(get_isAVCGA, set_isAVCGA)

    def set_rad_status(self, value):
        self._rad_status = value

    def get_rad_status(self):
        return self._rad_status

    Rad_status = property(get_rad_status, set_rad_status)

    # endregion

    # region Private Properties

    # endregion
    # region Constructors

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
                    # print("temp = " + temp);
                    temp = temp & 0x3F
                    if (temp < 31):
                        temp = temp + 0x40
                    # print('temp again', temp)
                    cc = str(temp)
                    # print(cc)
                    #                        Console.WriteLine("temp = " + temp + " cc = " + cc);
                    buildit = buildit + cc
                    # print('buildit ',buildit)
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

    def ExtractInt(self, startpos: int, blength: int):  # int
        # extracts an integer from the binary payload
        # use Binary_Item to get the actual bits
        return int(self.Binary_Item(startpos, blength))

    def Binary_Item(self, startpos: int, blength: int) -> int:
        # newer version concept only
        # convert bitarray to a string, use string slicing to get bits
        # then con vert the slice to int using int(string,2)

        reqbits = self._binary_payload[startpos:startpos + blength]
        # print('in Binary Item type reqbits = ', type(reqbits), ' value reqbits =', reqbits)
        if len(reqbits) != 0:
            return int(reqbits, 2)
        else:
            return 0

    # endregion
    # region Private Methods
    def create_binary_payload(p_payload: str):
        # based on using a supersized string rather than bytearray
        #
        printdiag = False
        #
        # define a null string
        _binary_payload = ''
        for i in range(0, len(p_payload)):
            if printdiag:
                print('in create binary payload ', len(p_payload), i)
            # iterate through the string payload masking to lower 6 bits
            xchar = p_payload[i]

            nibble = AIS_Data.m_to_int(xchar) & 0x3F  # ensures only 6 bits presented
            if printdiag:
                print('nibble', bin(nibble))

            # now append the nible to the stream
            _binary_payload = _binary_payload + format(nibble, '06b')

            if printdiag:
                print(_binary_payload)

        return _binary_payload, len(_binary_payload)

    def m_to_int(parameter: str) -> int:
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
            p = p[0: p.find('@')]
            return p
        else:

            if (p.find('@') == 0):
                return ''  # equivalent to String.Empty
            else:
                return p

    def Remove_space(self, p: str) -> str:
        if len(p) > 0 and p[- 1: 1] == " ":
            while p[len(p) - 1: 1] == " ":
                if (len(p) > 1):
                    p = p[0: len(p) - 1]
                else:
                    p = ''  # String.Empty
        return p

    _hasbeenDisposed = False

# region Disposals
