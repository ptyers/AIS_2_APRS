from datetime import datetime, timezone
import logging
from GlobalDefinitions import Global
import struct
import sys
from AISDictionary import AISDictionaries

'''
Group of Classes covering all breeds of payloads

Base Class is Payload all other classes inherit from this

'''


class Payload:
    # fields
    message_type: int
    repeat_indicator: int
    mmsi: str
    longitude: float
    latitude: float
    fix_quality: bool = False
    raim_flag: bool = 0  # default not in use
    radio_status: int = 0  # Not implemented
    payload: str  # binary payload
    valid_item: bool

    def __init__(self, p_payload: str):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        # p_payload is binary_payload string
        self.payload = p_payload

        self.message_type = self.binary_item(0, 6)
        if not (1 <= self.message_type <= 27):
            # logging.error("In Payload.__ini__ - Invalid Message Type not in 1-27")
            raise RuntimeError("Invalid Message Type not in 1-27")

        self.mmsi = self.create_mmsi()

        self.repeat_indicator = self.binary_item(6, 2)
        if not (0 <= self.repeat_indicator <= 3):
            # logging.error("In Payload.__ini__ - Invalid Repeat Indicator not in 0-3")
            raise RuntimeError("Invalid Repeat Indicator not in 0-3")

        self.longitude = 0.0
        self.latitude = 0.0
        self.raim_flag = False
        self.fix_quality = False
        self.valid_item = True

    def create_mmsi(self) -> str:
        # extract bits 8 to 37 from binary_payload, convert to int then to string zero filling (if nesecary)
        # to create 9 char MMSI zero filled on MSB

        # print('calling extract_int')
        # print('payload?', self.payload)

        immsi = self.extract_int(8, 30)
        # print(' after call ímmsi', immsi)
        _mmsi = "{:09d}".format(immsi)
        # print(' 0 filled  formatted version_mmsi', _mmsi)
        return _mmsi

    def extract_string(self, startpos: int, blength: int) -> str:
        # grab data 6 bit byte by byte checking that the
        # binary stream is not truncated from standard

        indexer = 0  # used to count number of bits extracted
        temp = 0
        cc = ' '
        buildit = ''

        try:
            while indexer < blength:
                if (startpos + indexer + 6) < len(self.payload):

                    temp = self.binary_item(startpos + indexer, 6)
                    # print("temp = ", temp)
                    temp = temp & 0x3F
                    temp = temp + 0x30
                    if temp > 0x57:
                        temp = temp + 0x8
                    # print('temp again', temp)
                    cc = chr(temp)
                    #                        Console.WriteLine("temp = " + temp + " cc = " + cc);
                    buildit = buildit + cc
                    # print('buildit ',buildit)
                    indexer = indexer + 6
                else:
                    indexer = blength

            # print("string returned = " + buildit);

            return buildit
        except:
            # logging.error(
            #     "Error in ExtractString startpos = " + str(startpos) + " blength = " + str(
            #         blength) + "binary_length = ")
            # logging.error("Exception while ExtractString startpos", sys.exc_info()[0])
            pass

    def extract_text(self, startpos: int, length: int):

        # given a payload , start position and a number of bits (which should be 0 modulo six)
        # return an ascii character string which is decoded in accordance with the AISDictionaries.nibble_to_text
        #

        # veracity test
        if length % 6 != 0:
            raise RuntimeError("Invalid number of bits {} defined in extract text".format(length))
        diction = AISDictionaries()

        # now get the text
        self.endpos = startpos + 6
        self.outstring = ''
        self.start = startpos
        while self.endpos < startpos + length + 6:
            #            print('in extract_text nibble presented ', self.payload[self.start: self.endpos+1])
            nibble = self.payload[self.start: self.endpos]
            self.outstring = self.outstring + diction.binary_to_char(nibble)
            self.start += 6
            self.endpos += 6
        #           print('in extract text startpos, supposed end, currect_end, outsring',
        #                  startpos, startpos+length, self.endpos, self.outstring)

        return self.outstring

    def extract_int(self, startpos: int, blength: int) -> int:  # int
        # extracts an integer from the binary payload
        # use Binary_Item to get the actual bits
        # print('extract int', startpos, blength)
        return self.binary_item(startpos, blength)

    def binary_item(self, startpos: int, blength: int) -> int:
        # convert bitarray to a string, use string slicing to get bits
        # then convert the slice to int using int(string,2)

        # veracity check
        if not (startpos + blength < len(self.payload)):
            # logging.error("In Payload.binary_item() - Request to extract more bits {} + {} "
            #               "which overrun end of binary payload {}".format(startpos, blength,len(self.payload)))
            raise RuntimeError("Request to extract more bits {} {} which overrun end of binary payload "
                               "{}".format(startpos, blength, len(self.payload)))
        reqbits = self.payload[startpos:startpos + blength]
        logging.debug('in Binary Item  reqbits = ', type(reqbits), ' value reqbits =', reqbits)
        if len(reqbits) != 0:
            return int(reqbits, 2)
        else:
            return 0

    def m_to_int(self, parameter: str) -> int:
        # takes in a encoded character  and returns positive integer
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

    def remove_at(self, input_p: str) -> str:
        '''
         remove_at strips trailing @ from string values

         :return:
             string without trailing @
         '''
        p = input_p
        str_pos = len(p) - 1
        p = input_p
        str_pos = len(p) - 1
        if p[str_pos] == '@':
            while p[str_pos] == '@':
                p = p[0:str_pos]
                if str_pos != 0:
                    str_pos -= 1
        return p

    def remove_space(self, input_p: str) -> str:
        '''
         remove_at strips trailing spaces from string values

         :return:
             string without trailing spaces
         '''
        p = input_p
        str_pos = len(p) - 1
        if p[str_pos] == ' ':
            while p[str_pos] == ' ':
                p = p[0:str_pos]
                if str_pos != 0:
                    str_pos -= 1
        return p

    def get_longitude(self, startpos: int, length: int = 28):
        # longitude is in various positions in differing blocks
        self.longitude = float(self.signed_binary_item(startpos, length)) / 600000

        # validation
        if not (-180.0 <= self.longitude <= 181.0):
            # print("error in get_longitude value returned ", self.longitude)
            self.valid_item = False
            raise ValueError

    def get_latitude(self, startpos: int, length: int = 27):
        # longitude is in various positions in differing blocks
        x = self.signed_binary_item(startpos, length)
        self.latitude = float(self.signed_binary_item(startpos, length)) / 600000
        # validation
        if not (-90.0 <= self.latitude <= 91.0):
            # print("error in get_latitude value returned ", self.latitude)
            self.valid_item = False
            raise ValueError

    def signed_binary_item(self, startpos: int, blength: int) -> int:
        '''
               signed_binary_item takes in a set of parameters start position, number of bits (blength)
               and extracts string of bits from the binary_payload.
               if MSBit is 1 the negetive. Do twos complement arithmetic to return a signed integer

                convert bitarray to a string, use string slicing to get bits
                then convert the slice as 2 complement binary
                two complement - if negetive invert all bits and add one to RHB
                so here if LHB is one then invert all bits and add 1 then return as negertive result


                :return:
                    signed integer value which will need scaling if necessary
            '''

        # veracity check

        if not (startpos + blength < len(self.payload)):
            # logging.error("In Payload.signed_binary_item() - "
            #             + "Request to extract more bits which overrun end of binary payload")
            raise RuntimeError("Request to extract more bits which overrun end of binary payload")

        reqbits = self.payload[startpos:startpos + blength]
        # check if LHB is one

        if reqbits[0] != '1':
            return int(reqbits, 2)
        else:
            newreqbits = ''
            for i in range(0, len(reqbits)):
                if reqbits[i] == "1":
                    newreqbits = newreqbits + '0'
                else:
                    newreqbits = newreqbits + '1'

        return -((int(newreqbits, 2) + 1))

    def get_flag_bit(self, position: int) -> bool:
        ''''
        Generic extract a boolean flag bit from given position
        :parameter:
            position - bit position in stream from which toextract the flag bit

        :return:
            returns boolean value of flag
        '''

        if self.binary_item(position, 1) == 1:
            self.flag = True
        else:
            self.flag = False

        return self.flag

    def getRAIMflag(self, position: int) -> None:
        '''
         The RAIM flag indicates whether Receiver Autonomous Integrity Monitoring is being used
          to check the performance  if the EPFD.
          0 = RAIM not in use (default),
          1 = RAIM in use.
          See [RAIM] for a detailed description of this flag.

          at bit position 148 in CNB, Base Station

         :return:
             sets Payload.RAIMflag
         '''
        # RAIM flag bool False = not in use
        # location varies in blocks

        self.raim_flag = self.get_flag_bit(position)

    def getfix(self, position: int) -> None:
        '''
            The position accuracy flag indicates the accuracy of the fix.
            A value of 1 indicates a DGPS-quality fix with an accuracy of < 10ms.
              0, the default, indicates an unaugmented GNSS fix with accuracy > 10m.

            :return:
              sets payload.fixquality
        '''
        # Fix Quality flag bool False = not in use
        # location varies in blocks
        self.fix_quality = self.get_flag_bit(position)


class Basic_Position(Payload):
    # basse class from mwhich CNB, Class B Aid to Nav objects will inherit

    speed_over_ground: float
    course_over_ground: float
    true_heading: int
    time_stamp: int
    ship_type: int  # enumerated see dictionary (eventually ) 0-99 but garbage not uncommen
    vessel_name: str
    ship_type: int  # enumerated see dictionary (eventually ) 0-99 but garbage not uncommen
    dim_to_bow: int
    dim_to_stern: int
    dim_to_port: int
    dim_to_stbd: int
    ais_version: int = 0  # enumerated normally 0, 1-3 future editions

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        # very little initiation done in this class just provides routines for use in CNB, Static, Class B

    def get_nav_status(self, position: int, length: int) -> None:
        '''
        Navigation Status is described in AISDictionary

        :input:
            bits 38-41 in self.payload

        :values:
            valid values 0-15, only four bits so cannot exceed  this range
        :return:
            sets self.navigation_status
        '''

        # at bits 38-41
        #
        self.navigation_status = self.binary_item(position, length)

    def getSOG(self, position: int, length: int) -> None:
        '''

        Speed over ground is in 0.1-knot resolution from 0 to 102 knots.
        Value 1023 indicates speed is not available,
         value 1022 indicates 102.2 knots or higher.
        :return:
            set mycnb.speed_over_ground (float)
        '''

        intval = self.binary_item(position, length)

        self.speed_over_ground = float(intval) / 10.0

    def get_COG(self, position: int, length: int) -> None:
        '''
        stored as inter value scaled up by 10
        Course over ground will be 3600 (0xE10) if that data is not available.

        :return:
            sets mycnb.course over_ground (float)
        '''
        # course over ground - scaled by 10
        intval = self.binary_item(116, 12)
        if 0 <= intval <= 3600:
            self.course_over_ground = round(float(intval) / 10.0, 1)
        else:
            self.valid_item = False
            errstr: str = 'In CNB.get_COG - value outside range 0-360 ' + '{:d}'.format(intval)
            # logging.error(errstr)
            raise ValueError

    def get_tru_head(self, position: int, length: int) -> None:
        '''
            true heading is integer value
            0-359 degrees
            511 not avaiulable

            routine checks validity sets to False if outside 0-359 and/or 511

        :return:
            sets mycnb.true_heading (integer)
        '''

        itru = self.binary_item(128, 9)
        if 0 <= itru <= 359 or itru == 511:
            self.true_heading = itru
        else:
            self.valid_item = False
            errstr: str = '{:d}'.format(itru)
            # logging.error('In get_tru_head - value outside range 0-359 or != 511 : ' + errstr)
            raise ValueError

    def get_timestamp(self, position: int, length: int) -> None:
        '''
        Seconds in UTC timestamp should be 0-59, except for these special values:

        60 if time stamp is not available (default)

        61 if positioning system is in manual input mode

        62 if Electronic Position Fixing System operates in estimated (dead reckoning) mode,

        63 if the positioning system is inoperative.

        bits 137-142 in binary_payload

        :return:
            sets mycnb.time_stamp (integer)
        '''
        # timestamp = second of UTC timestamp. 6 bits at 137
        intval = self.binary_item(137, 6)

        # validate
        if 0 <= intval <= 63:
            self.time_stamp = self.binary_item(137, 6)
        else:
            self.valid_item = False
            # logging.error('In CNB.get_timestamp - value outside range 0-63 ' + str(intval))
            raise ValueError

    def get_vessel_name(self, position: int, length: int) -> None:
        '''
        also obvioous - get ships name
        20 six bit free text characters
        :return:
            sets StaticData.ships_name
        '''

        try:
            self.vessel_name = self.extract_text(position, length)
        except RuntimeError:
            self.vessel_name = 'VesselName Unknown'
            # logging.error("In Static.get_vessel_name Runtime error")

        while self.vessel_name[len(self.vessel_name) - 1] == '@':
            self.vessel_name = self.vessel_name[0:len(self.vessel_name) - 1]

    def get_ship_type(self, position: int, length: int) -> None:
        '''
        dfecribed in AISDictionary
        range 0-99
        Note that garbage values greater than 99 are supposed to be unused,
        but are not uncommon in the wild; AIS transmitters seem prone to put junk in this field
        when it’s not explicitly set. Decoders should treat these like value 0 rather than throwing an exception
         until and unless the controlled vocabulary is extended to include the unknown values.
         :retur:
            sets StatcData.ship_type
        '''
        try:
            self.ship_type = self.binary_item(position, length)
            status = self.ship_type in AISDictionaries.Ship_Type
        except RuntimeError:
            # logging.error("In Static.get_ship_type Runtime error")
            self.ship_type = 0

        if self.ship_type not in AISDictionaries.Ship_Type:
            # logging.error('In Static.get_ship_type  type not in range 0-99')
            self.ship_type = 0

    def get_dim_to_bow(self, position: int, length: int) -> None:
        '''
                Ship dimensions will be 0 if not available.
                For the dimensions to bow and stern, the special value 511 indicates 511 meters or greater;
                for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

                ship dimensions should be set to the maximum rectangle size of the convoy

                :return:
                    sets StaticData.dim_to_bow

                '''

        try:
            self.dim_to_bow = self.binary_item(position, length)
        except RuntimeError:
            # logging.error("In Static.get_dim_to_bow got run time error")
            self.dim_to_stern = 0

    def get_dim_to_stern(self, position: int, length: int) -> None:
        '''
        Ship dimensions will be 0 if not available.
        For the dimensions to bow and stern, the special value 511 indicates 511 meters or greater;
        for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        :return:
            sets StaticData.dim_to_stern

        '''
        try:
            self.dim_to_stern = self.binary_item(position, length)
        except RuntimeError:
            # logging.error("In Static.get_dim_to_stern got run time error")
            self.dim_to_stern = 0

    def get_dim_to_port(self, position: int, length: int) -> None:
        '''
                Ship dimensions will be 0 if not available.
                For the dimensions to bow and stern, the special value 511 indicates 511 meters or greater;
                for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
                :return:
                    sets StaticData.dim_to_port

                '''

        try:
            self.dim_to_port = self.binary_item(position, length)
        except RuntimeError:
            # logging.error("In Static.get_dim_to_port got run time error")
            self.dim_to_stern = 0

    def get_dim_to_stbd(self, position: int, length: int) -> None:
        '''
                Ship dimensions will be 0 if not available.
                For the dimensions to bow and stern, the special value 511 indicates 511 meters or greater;
                for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
                :return:
                    sets StaticData.dim_to_stbd

                '''

        try:
            self.dim_to_stbd = self.binary_item(position, length)
        except RuntimeError:
            # logging.error("In Static.get_dim_to_stbd got run time error")
            self.dim_to_stern = 0

    def get_EPFD(self, position: int, length: int) -> None:
        '''
        The standard uses "EPFD" to designate any Electronic Position Fixing Device.
        Bits 134-137  length 4  Type of EPFD epfd  See "EPFD Fix Types" in Dictionary
        Valid 0-8 15 not uncommen
        :return:
            sets Base.EPFD_type for 9-14 logs error returns 0 but does not invalidate object
        '''
        self.EPFD_type = self.binary_item(position, length)
        if 9 <= self.EPFD_type <= 14:
            self.EPFD_type = 0
            # logging.error("In get_EPFD_type found value between 9 and 14")

    def get_ais_version(self, position: int, length: int) -> None:
        '''
        0=[ITU1371], 1-3 = future editions
        :return:
            sets StaticData.ais_version - returns zero currently until new edition specifies 1-3
        '''
        self.ais_version = self.binary_item(position, length)
        if self.ais_version != 0:
            if self.ais_version in [1, 2, 3]:
                # logging.error("In Static.get_ais_version found " + '{:d}'.format(self.ais_version) + " rather than 0")
                self.ais_version = 0


class CNB(Basic_Position):
    # additional fields

    navigation_status: int
    rate_of_turn: float
    # rate of turn has 3 special values
    # 1000.0 - No turn Indication available
    # 1005 turning right at more than 5 degrees/ 30 seconds
    # -1005.0 turning leftat more than 5 degrees/ 30 seconds
    # otherwise range is -708.0 t0 708.0 degrees per minute - negetive left, positivew right
    raw_rate_of_turn: int
    position_accuracy: bool
    maneouver_indicator: int

    def __init__(self, p_payload: str):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)
        self.get_CNB_nav_status()
        self.get_ROT()
        self.getCNB_SOG()
        self.get_pos_accuracy()
        self.get_longitude(61, 28)
        self.get_latitude(89, 27)
        self.getCNB_COG()
        self.getCNB_tru_head()
        self.getCNB_timestamp()
        self.get_man_indic()
        self.getfix(60)

        logging.basicConfig(level=logging.CRITICAL)

        pass

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type:        {self.message_type}\n'
                f'Repeat Indicator:    {self.repeat_indicator}\n'
                f'MMSI:                {self.mmsi}\n'
                f'Navigation Status:   {self.navigation_status}\n'
                f'Rate of Turn:        {self.rate_of_turn}\n'
                f'Speed over Ground:   {self.speed_over_ground}\n'
                f'Position\ Accuracy:  {self.position_accuracy}\n'
                f'Longitude:           {self.longitude}\n'
                f'Latitude:            {self.latitude}\n'
                f'Course over Ground:  {self.course_over_ground}\n'
                f'True Heading:        {self.true_heading}\n'
                f'Timestamp:           {self.time_stamp}\n'
                f'Maneuver Indicator:  {self.maneouver_indicator}\n'
                f'RAIM status:         {self.raim_flag}\n'
                )

    def get_CNB_nav_status(self):
        self.get_nav_status(38, 4)

    def get_ROT(self) -> None:
        '''
        # ROT - Rate of Turn is scaled by 1000 returns float
        # signed integer scaled to float then calculated as divide by 4.733, retain sign but square it
        Turn rate is encoded as follows:

        0 = not turning

        1…126 = turning right at up to 708 degrees per minute or higher

        1…-126 = turning left at up to 708 degrees per minute or higher

        127 = turning right at more than 5deg/30s (No TI available)

        -127 = turning left at more than 5deg/30s (No TI available)

        128 (80 hex) indicates no turn information available (default)

        Values between 0 and 708 degrees/min coded by ROTAIS=4.733 * SQRT(ROTsensor) degrees/min
        where ROTsensor is the Rate of Turn as input by an external Rate of Turn Indicator.
        ROTAIS is rounded to the nearest integer value. Thus, to decode the field value, divide by 4.733
        and then square it. Sign of the field value should be preserved when squaring it,
        otherwise the left/right indication will be lost.

        With 8 bits there cannot be any values out of range

        :return:
            sets mycnb.rate_of_turn (float)
        '''
        # ROT - Rate of Turn is scaled by 1000
        # signed integer scaled to float then calculated as divide by 4.733, retain sign but square it

        irot = self.signed_binary_item(42, 8)
        if irot >= 0 or irot == -128:
            if 0 <= irot <= 126:
                self.rate_of_turn = float(round((float(irot) / 4.733) ** 2))
            elif irot == 127:
                self.rate_of_turn = 1005.0  # indicates ROT of > 5 degres/30sec right (No Turn Indic available)
            elif irot == -128:
                self.rate_of_turn = 1000.0  # indicates No Turn Indication available - DEFAULT


        else:

            if irot < 0:
                if -126 <= irot <= -1:
                    self.rate_of_turn = - float(round((float(irot) / 4.733) ** 2))
                elif irot == -127:
                    self.rate_of_turn = -1005.0  # indicates ROT of > 5 degres/30sec left (No Turn Indic available)
            self.raw_rate_of_turn = irot

    def getCNB_SOG(self):
        self.getSOG(50, 10)

    def getCNB_COG(self):
        self.get_COG(116, 12)

    def getCNB_tru_head(self):
        self.get_tru_head(128, 9)

    def get_pos_accuracy(self) -> None:
        '''

        The position accuracy flag indicates the accuracy of the fix.
        A value of 1 indicates a DGPS-quality fix with an accuracy of < 10ms. 0,
        the default, indicates an unaugmented GNSS fix with accuracy > 10m.

        in bit 60 of binary payload
        :return:
            sets mycnb.position_accuracy (bool)
        '''

        self.position_accuracy = self.get_flag_bit(60)

    def getCNB_timestamp(self):
        self.get_timestamp(137, 6)

    def get_man_indic(self):
        '''
            The Maneuver Indicator (143-144) may have these values:

            Table 8. Maneuver Indicator
            0  Not available (default)
            1  No special maneuver
            2  Special maneuver (such as regional passing arrangement)

            range 0-2. Bits 143-144 in binary_payload

        :return:
            sets mycnb.maneouver_indicator (integer)
            validates that values are in 0-2, invalidates mycnb.success for value == 3
        '''
        # maneouver indicator. 0-2. Bits 143-144

        intval = self.binary_item(143, 2)
        if 0 <= intval <= 2:
            self.maneouver_indicator = intval
        else:
            self.valid_item = False
            errstr: str = '{:d}'.format(intval)
            # logging.error('In CNB.get_man indicator - value outside range 0-2' + errstr)
            raise ValueError


class Basestation(Basic_Position):
    # base station report - Type 4

    # items specific to base station
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    EPFD_type: int

    def __init__(self, p_payload: str):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)
        self.get_year()
        self.get_month()
        self.get_day()
        self.get_hour()
        self.get_minute()
        self.get_second(72, 6)
        self.get_Base_EPFD()
        self.getfix(78)
        self.getRAIMflag(148)

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type: {self.message_type}\n'
                f'MMSI:         {self.mmsi}\n'
                f'Year:         {self.year}\n'
                f'Month:        {self.month}\n'
                f'Day:          {self.day}\n'
                f'Hour:         {self.hour}\n'
                f'Minute :      {self.minute}\n'
                f'Second:       {self.second}\n'
                f'Longitude:    {self.longitude}\n'
                f'Latitude:     {self.latitude}\n'
                f'EPFDD Type:   {self.EPFD_type}\n'
                f'RAIM Flag:    {self.raim_flag}\n'
                )

    def get_year(self) -> None:
        '''
        Bits 38-51  length 14  Year (UTC)  year  UTC, 1-9999, 0 = N/A (default)

        :return:
            sets Base.year
        '''
        self.year = self.binary_item(38, 14)
        if not (0 <= self.year <= 9999):
            self.valid_item = False
            # logging.error("Base.year outside range 0-9999 " + '{:d}'.format(self.year))
            raise ValueError

    def get_month(self) -> None:
        '''
        Bits 52-55 length 4  Month (UTC) month  1-12; 0 = N/A (default)
        :return:
            sets Base.month
        '''

        self.month = self.binary_item(52, 4)
        if not (0 <= self.month <= 12):
            self.valid_item = False
            # logging.error("Base.month outside range 0-12 " + '{:d}'.format(self.month))
            raise ValueError

    def get_day(self) -> None:
        '''
        Bits 56-60  length 5  Day (UTC) day  1-31; 0 = N/A (default)
        :return:
            sets Base.day
        '''

        self.day = self.binary_item(56, 5)
        if not (0 <= self.day <= 31):
            # logging.error("Base.day outside range 0-31 " + '{:d}'.format(self.day))
            self.valid_item = False
            raise ValueError

        # now look for the strange cases
        self.get_year()
        self.get_month()
        # print(self.year, '  modulo', self.year % 4, ' ', self.month, ' ', self.day)
        if self.year % 4 == 0 and self.month == 2 and self.day > 29:
            # print(self.year, '  modulo', self.year % 4, ' ', self.month, ' ', self.day)
            # print('day greater 29')
            self.valid_item = False
            # logging.error("Base.day value returned for February leap year invalid " + '{:d}'.format(self.day))
            raise ValueError

        if self.year % 4 != 0 and self.month == 2 and self.day > 28:
            # logging.error(
            #    "Base.day value returned for February nonleap year invalid " + '{:d}'.format(self.day))
            self.valid_item = False
            raise ValueError

        if self.month in [4, 6, 9, 11]:
            if self.day > 30:
                # logging.error(
                #    "Base.day value returned for 30 day months  invalid" + '{:d}'.format(self.day))
                self.valid_item = False
                raise ValueError

    def get_hour(self):
        '''
            Bits 61-65 length 5  Hour (UTC) hour  0-23; 24 = N/A (default)
        :return:
            sets Base.hour
        '''
        self.hour = self.binary_item(61, 5)
        if not (0 <= self.hour <= 24):
            self.valid_item = False
            # logging.error("Base.hour outside range 0-24 " + '{:d}'.format(self.hour))
            raise ValueError

    def get_minute(self) -> None:
        '''
            Bits 66-71 length 6  Minute (UTC) minute  0-59; 60 = N/A (default)
        :return:
            sets Base.minute
        '''
        self.minute = self.binary_item(66, 6)
        if not (0 <= self.minute <= 60):
            self.valid_item = False
            # logging.error("Base.minute outside range 0-60 " + '{:d}'.format(self.minute))
            raise ValueError

    def get_second(self, position: int, length: int = 6) -> None:
        '''
                Bits 72-77 length 6  Second (UTC) second  0-59; 60 = N/A (default)
            :return:
                sets Base.second
            '''
        self.second = self.binary_item(72, 6)
        if not (0 <= self.second <= 60):
            self.valid_item = False
            # logging.error("Base.second outside range 0-60 " + '{:d}'.format(self.second))
            raise ValueError

    def get_Base_EPFD(self):
        self.get_EPFD(134, 4)


class StaticData(Basic_Position):
    # type 5
    '''
    Message has a total of 424 bits, occupying two AIVDM sentences.
    In practice, the information in these fields (especially ETA and destination) is not reliable,
    as it has to be hand-updated by humans rather than gathered automatically from sensors.
    Also note that it is fairly common in the wild for this message to have a wrong bit length (420 or 422).
    Robust decoders should ignore trailing garbage and deal gracefully with a slightly truncated destination field.
    '''

    imo_number: str
    callsign: str

    # fix type derived from super class
    eta_month: int
    eta_day: int
    eta_hour: int
    eta_min: int
    draught: float
    destination: str  # as above destination field may be truncated due to wrong bit length being supplied
    payload: str  # holds the "binary payload supplied as part of instatiation
    maxpayloadlen: int  # used to check for packet truncation

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)
        # first check actual payload length
        self.payload = p_payload
        self.maxpayloadlen = len(p_payload)  # will be used when attempting to get destination to avoid bit overrun

        self.create_mmsi()
        self.get_Base_ais_version()
        self.get_imo_number()
        self.get_callsign()
        self.get_Static_vessel_name()
        self.get_Static_dim_to_bow()
        self.get_Static_dim_to_stern()
        self.get_Static_dim_to_port()
        self.get_Static_dim_to_stbd()
        self.get_Static_ship_type()
        self.get_eta_month()
        self.get_eta_day()
        self.get_eta_hour()
        self.get_eta_minute()
        self.get_draught()
        self.get_destination()

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type: {self.message_type}\n'
                f'MMSI:         {self.mmsi}\n'
                f'AIS version:  {self.ais_version}\n'
                f'IMO Number:   {self.imo_number}\n'
                f'Callsign:    {self.callsign}\n'
                f'Vessel Name:  {self.vessel_name}\n'
                f'Ship Type :   {self.ship_type}\n'
                f'Dim to Bow:   {self.dim_to_bow}\n'
                f'Dim to Stern: {self.dim_to_stern}\n'
                f'Dim to Stbd:  {self.dim_to_stbd}\n'
                f'Fix Type:     {self.fix_quality}\n'
                f'ETA Month:    {self.eta_month}\n'
                f'ETA Month:    {self.eta_month}\n'
                f'ETA Day:      {self.eta_day}\n'
                f'ETA Hour:     {self.eta_hour}\n'
                f'ETA Minute:   {self.eta_minute}\n'
                f'Draught       {self.draught}\n'
                f'Destination   {self.destination}'
                )

        # dont invalidate object but flag error

    def get_Base_ais_version(self):
        self.get_ais_version(38, 2)

    def get_imo_number(self) -> None:
        '''
        IMO number is a unique identifier for ships, registered ship owners and management companies1.
        It consists of the three letters "IMO" followed by a seven-digit number assigned to all ships
         by IHS Fairplay123. The IMO number was introduced to improve maritime safety and security and
         to reduce maritime fraud1.

        [INLAND] specifies the following:

        the IMO Number field should be zeroed for inland vessels.
        ATIS code should be used for inland vessels

        :return:
            sets StaticData.imo_number
        '''
        try:
            self.intimo = self.binary_item(46, 30)
            self.imo_number = '{:07d}'.format(self.intimo)
        except RuntimeError:
            self.imo_number = '0000000'
            # logging.error("In Static.get_imo_number got RunTime Error")

        # little validation can be done here other than that number less equal 9999999

        if self.intimo <= 9999999:
            self.imo_number = '{:07d}'.format(self.intimo)
            self.valid_item = False
            # logging.error("In Static.get_imo_number found value greater than 99999999 - {:d}".format(self.intimo))
            self.imo_number = '0000000'
            raise ValueError

    def get_callsign(self) -> None:
        '''
        fairly obvious - get ships callsign 7 characters free text encoded as 6 bit chars
        :return:
            sets StaticData.callsign
        '''
        try:
            self.callsign = self.extract_text(70, 42)
        except RuntimeError:
            self.callsign = 'NoCall '
            # logging.error("In Static.get_callsign Runtime error")

    def get_Static_vessel_name(self):
        self.get_vessel_name(112, 120)

    def get_Static_ship_type(self):
        self.get_ship_type(232, 8)

    def get_Static_dim_to_bow(self):
        self.get_dim_to_bow(240, 9)

    def get_Static_dim_to_stern(self):
        self.get_dim_to_stern(249, 9)

    def get_Static_dim_to_port(self):
        self.get_dim_to_port(258, 6)

    def get_Static_dim_to_stbd(self):
        self.get_dim_to_stbd(264, 6)

    def get_eta_month(self) -> None:
        '''
        In practice, the information in these fields (especially ETA and destination) is not reliable,
        as it has to be hand-updated by humans rather than gathered automatically from sensors.
        1-12, 0=N/A (default)
        :return:
            sets StaticData.eta_month
        '''
        self.eta_month = self.binary_item(274, 4)
        # can possibly return > 12 - if so set to 0 default
        if self.eta_month > 12:
            # logging.error("In Static.get_eta>month value returned greater than 12")
            self.eta_month = 0

    def get_eta_day(self) -> None:
        '''
                In practice, the information in these fields (especially ETA and destination) is not reliable,
                as it has to be hand-updated by humans rather than gathered automatically from sensors.
                1-31, 0=N/A (default)
                :return:
                    sets StaticData.eta_day
                '''
        self.eta_day = self.binary_item(278, 5)

        # cant return > 31 in 5 bits soi no need to check for this
        # check if self.eta_month = 2 and if self.eta_day > 29
        # and that for 30 day months day < 31

        if self.eta_month == 2 and self.eta_day > 29:
            # logging.error("In Static.get_eta_day february day set > 29")
            self.valid_item = False
            raise ValueError

        if self.eta_month in [4, 6, 9, 11] and self.eta_day > 30:
            # logging.error("In Static.get_eta_day 30 day month day set > 30")
            self.valid_item = False
            self.eta_day = 0
            raise ValueError

    def get_eta_hour(self) -> None:
        '''
                In practice, the information in these fields (especially ETA and destination) is not reliable,
                as it has to be hand-updated by humans rather than gathered automatically from sensors.
                0-23, 24=N/A (default)
                :return:
                    sets StaticData.eta_hour
                '''
        try:
            self.eta_hour = self.binary_item(283, 5)
        except RuntimeError:
            # logging.error("In Static.get_eta_hour got run time error")
            self.eta_hour = 24

        # 5 bits can get values above 24 will be flagged and reset to 24 the default

        if not (0 <= self.eta_hour <= 24):
            self.eta_hour = 24
            # logging.error("In Static.get_eta_hour value outside range 0-24")
            raise ValueError

    def get_eta_minute(self) -> None:
        '''
                In practice, the information in these fields (especially ETA and destination) is not reliable,
                as it has to be hand-updated by humans rather than gathered automatically from sensors.

                0-59, 60=N/A (default)
                :return:
                    sets StaticData.eta_minute
                '''
        try:
            self.eta_minute = self.binary_item(288, 6)
        except RuntimeError:
            # logging.error("In Static.get_eta_minute got run time error")
            self.eta_minute = 60

        # 5 bits can get values above 60 will be flagged and reset to 24 the default

        if not (0 <= self.eta_minute <= 60):
            self.eta_minute = 60
            # logging.error("In Static.get_eta_minute value outside range 0-60")
            raise ValueError

    def get_draught(self) -> None:
        '''
        draught information should be rounded up to nearest decimeter
        Meters/10
        :return:
        '''

        try:
            self.draught = round(float(self.binary_item(294, 8)) / 10.0, 1)
        except RuntimeError:
            # logging.error("In Static.draught Runtime error")
            self.draught = 0.0

    def get_destination(self) -> None:
        '''
        In practice, the information in these fields (especially ETA and destination) is not reliable,
        as it has to be hand-updated by humans rather than gathered automatically from sensors.

        For the destination, UN/LOCODE and ERI terminal codes should be used

        As noted this field may be truncated due to incorrect payload bit counts being given.
        Use  self.maxpayloadlen to avoid bit overrun

        :return:
            sets StaticData.eta_minute
        '''
        if 421 > self.maxpayloadlen:
            # will need to truncate the call to Extract String
            self.destination = self.extract_text(302, self.maxpayloadlen - 302)
        else:
            self.destination = self.extract_text(302, 120)

        while self.destination[len(self.destination) - 1] == '@':
            self.destination = self.destination[0:len(self.destination) - 1]


class Binary_addressed_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Binary_acknowledge(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Binary_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class SAR_aircraft_position_report(Basic_Position):
    '''
    Type 9: Standard SAR Aircraft Position Report
    Tracking information for search-and-rescue aircraft. Total number of bits is 168.

    Altitude is in meters.
    The special value 4095 indicates altitude is not available; 4094 indicates 4094 meters or higher.

    Speed over ground is in knots, not deciknots as in the common navigation block; planes go faster.
    The special value 1023 indicates speed not available, 1022 indicates 1022 knots or higher.

    Position Accuracy, Longitude, Latitude, and Course over Ground are encoded identically
        as in the common navigation block and are even at the same bit offsets.
    Time stamp has the same special values as in the common navigation block, but is at a different offset.

    '''

    altitude: int
    speed_over_ground: int
    course_over_ground: float
    time_stamp: int
    dte: bool
    assigned: bool

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.get_altitude()
        self.get_speed_over_ground()
        self.get_course_over_ground()
        self.get_time_stamp()
        self.get_dte()
        self.get_assigned()

    def __repr__(self):

        return (f'{self.__class__.__name__}\n'
                f'Message Type:          {self.message_type}\n'
                f'MMSI:                  {self.mmsi}\n'
                f'Altitude:              {self.altitude}\n'
                f'Speed over Ground:     {self.speed_over_ground}\n'
                f'Position Accuracy:     {self.fix_quality}\n'
                f'Longitudee:            {self.longitude}\n'
                f'Latitude :             {self.latitude}\n'
                f'Course over Ground:    {self.course_over_ground}\n'
                f'TimeStamp:             {self.time_stamp}\n'
                f'DTE Status:            {self.dte}\n'
                f'RAIM flag:             {self.raim_flag}\n'
                )

    def get_altitude(self):
        '''
            Altitude is in meters.
            The special value 4095 indicates altitude is not available; 4094 indicates 4094 meters or higher.
            :return:
                sets mysar.altitude

            '''
        # no real checking possible , range 0-4095

        self.altitude = self.binary_item(38, 12)

        pass

    def get_speed_over_ground(self):
        '''
        Speed over ground is in knots, not deciknots as in the common navigation block; planes go faster.
        The special value 1023 indicates speed not available, 1022 indicates 1022 knots or higher.
        10 bits range 0-1023

        :return:
            sets mysar.speed_over_ground
        '''

        self.speed_over_ground = self.binary_item(50, 10)

    def get_course_over_ground(self):

        '''
        stored as inter value scaled up by 10
        Course over ground will be 3600 (0xE10) if that data is not available.

        :return:
            sets mycnb.course over_ground (float)
        '''
        # course over ground - scaled by 10
        intval = self.binary_item(116, 12)
        if 0 <= intval <= 3600:
            self.course_over_ground = round(float(intval) / 10.0, 1)
        else:
            self.valid_item = False
            errstr: str = 'In SAR.get_COG - value outside range 0-360 ' + '{:d}'.format(intval)
            # logging.error(errstr)
            raise ValueError

    def get_time_stamp(self):
        self.time_stamp = self.binary_item(128, 6)

    def get_dte(self):
        self.dte = self.get_flag_bit(142)

    def get_assigned(self):
        self.assigned = self.get_flag_bit(146)


class UTC_date_enquiry(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)


class UTC_date_response(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Addressed_safety_related_message(Payload):
    '''
        Pragmatic note:
        On [AISHUB] the actual content of these messages is highly variable,
        ranging from fairly plain English ("PLEASE REPORT TO JOBOURG TRAFFIC CHANNEL 13")
        through snippets of tabular data ("PAX 589 FG 36 IX 74 MOTO 10 CREW 108+1" through
        what look like opaque commercial codes ("EP285 IX46 FG3 DK8 PL56") to empty strings
        and content that looks like line noise ("]XFD5D/\7`>PA!Q DX0??K?8?>D").

        Such apparently garbled content does not mean there is an error in your decoder.
        It may indicate faulty encoders, operator error, or even the use of private
        encodings for non-ASCII character sets.
    '''

    # message type, Repeat Indicator, Source MMSI inherited from base class

    sequence_number: int  # range 0-3bits 38-39, 2 bits
    destination_mmsi: str  # 9 digits unsigned integer but stored as str bits 40-69
    retransmit_flag: bool  # bit 70, 0 no retransmit, 1 transmitted
    safety_text: str  # 1-156 characters of six bit text. starts at bit 72, may be shorter than 936 bits
    # almost certainly will be derived from aggregated fragments

    payload: str  # the binary payload deriverd from the AIS Stream

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.payload = p_payload

        self.get_sequence_number()
        self.get_destination_mmsi()
        self.get_retransmit_flag()
        self.get_safety_text()

    def __repr__(self):

        formatted_safety_text = ''
        start_text = 0

        if len(self.safety_text) > 60:
            while start_text + 60 < len(self.safety_text):
                formatted_safety_text = formatted_safety_text + self.safety_text[start_text: start_text + 60] + '\n'
                start_text += 60

        # and the last line
        formatted_safety_text = formatted_safety_text + self.safety_text[start_text:] + '\n'

        return (f'{self.__class__.__name__}\n'
                f'Message Type:          {self.message_type}\n'
                f'MMSI:                  {self.mmsi}\n'
                f'Sequence_Number:       {self.sequence_number}\n'
                f'Destination MMSI:      {self.destination_mmsi}\n'
                f'Safety Text:           {formatted_safety_text}\n'
                f'Retransmit Flag:       {self.retransmit_flag}\n'
                )

    def get_sequence_number(self):
        self.sequence_number = self.binary_item(38, 2)

    def get_repeat_indicator(self):
        self.repeat_indicator = self.binary_item(6, 2)

    def get_destination_mmsi(self):
        self.destination_mmsi = '{:09d}'.format(self.binary_item(40, 30))

    def get_retransmit_flag(self):
        self.retransmit_flag = self.get_flag_bit(70)

    def get_safety_text(self):
        text_start = 72

        text_length = len(self.payload) - 72
        # ensure we get ony six bit count
        while text_length % 6 != 0:
            text_length -= 1

        # going to make assumption that the safety_text runs from bit 72 to the end of the binary payload

        self.safety_text = self.extract_text(72, text_length)

        while self.safety_text[len(self.safety_text) - 1] == '@' and len(self.safety_text) != 1:
            self.safety_text = self.safety_text[0:len(self.safety_text) - 1]

        # accounting for empty text
        if len(self.safety_text) == 1 and self.safety_text == '@':
            self.safety_text = ''


class Safety_related_acknowledgement(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Safety_related_broadcast_message(Payload):
    '''
        Pragmatic note:
        On [AISHUB] the actual content of these messages is highly variable,
        ranging from fairly plain English ("PLEASE REPORT TO JOBOURG TRAFFIC CHANNEL 13")
        through snippets of tabular data ("PAX 589 FG 36 IX 74 MOTO 10 CREW 108+1" through
        what look like opaque commercial codes ("EP285 IX46 FG3 DK8 PL56") to empty strings
        and content that looks like line noise ("]XFD5D/\7`>PA!Q DX0??K?8?>D").

        Such apparently garbled content does not mean there is an error in your decoder.
        It may indicate faulty encoders, operator error, or even the use of private
        encodings for non-ASCII character sets.
    '''

    # message type, Repeat Indicator, Source MMSI inherited from base class

    safety_text: str  # 1-161 characters of six bit text. starts at bit 72, may be shorter than 968 bits
    # almost certainly will be derived from aggregated fragments

    payload: str  # the binary payload derived from the AIS Stream

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.payload = p_payload
        self.get_safety_text()

    def __repr__(self):

        formatted_safety_text = ''
        start_text = 0

        if len(self.safety_text) > 60:
            while start_text + 60 < len(self.safety_text):
                formatted_safety_text = formatted_safety_text + self.safety_text[start_text: start_text + 60] + '\n'
                start_text += 60

        # and the last line
        formatted_safety_text = formatted_safety_text + self.safety_text[start_text:] + '\n'

        return (f'{self.__class__.__name__}\n'
                f'Message Type:          {self.message_type}\n'
                f'MMSI:                  {self.mmsi}\n'
                f'Safety Text:           {formatted_safety_text}\n'
                )

    def get_safety_text(self):
        text_start = 40
        text_length = len(self.payload) - 40
        # ensure we get ony six bit count
        while text_length % 6 != 0:
            text_length -= 1

        # going to make assumption that the safety_text runs from bit 72 to the end of the binary payload

        self.safety_text = self.extract_text(40, text_length)

        while self.safety_text[len(self.safety_text) - 1] == '@':
            self.safety_text = self.safety_text[0:len(self.safety_text) - 1]


class Interrogation(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class DGNS_broadcast_binary_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class ClassB_position_report(Basic_Position):
    '''
    A less detailed report than types 1-3 for vessels using Class B transmitters. 
    Omits navigational status and rate of turn. 
    Fields are encoded as in the common navigation block. 168 bits total.

    In [IALA] (and [ITU1371]) bits 141-145 were designated "Spare"; 
    the bit-flag semantics given here are from ITU-1371-3 and were communicated by Kurt Schwehr. 
    Kurt warns that "the spec does not do a good job of explaining these fields…
    ​ I don’t think that I totally understand these fields."

    # type 18
    # message_type, repeat_indicator, mmsi, longitude, latitude, speed over_ground, position_accuracy,
    # course_over_ground, True heading, time stamp DSC flag, assigned flag raim flag 
    #derived from base position report class *** To be written to allow CNB to be derived from it also ****
    # CNB will require a rewrite accordingly 
    '''

    cs_unit: bool  # 0=Class B SOTDMA unit 1=Class B CS (Carrier Sense) unit
    display_flag: bool  # 0=No visual display, 1=Has display, (Probably not reliable).
    band_flag: bool  # Base stations can command units to switch frequency.
    # If this flag is 1, the unit can use any part of the marine channel.
    message22_flag: bool  # If 1, unit can accept a channel assignment via Message Type 22.

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.get_cs_unit()
        self.get_display_flag()
        self.get_band_flag()
        self.get_message22_flag()
        self.getfix(56)

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type:        {self.message_type}\n'
                f'Repeat Indicator:    {self.repeat_indicator}\n'
                f'MMSI:                {self.mmsi}\n'
                f'Speed over Ground:   {self.speed_over_ground}\n'
                f'Position Accuracy:   {self.fix_quality}\n'
                f'Longitude:           {self.longitude}\n'
                f'Latitude:            {self.latitude}\n'
                f'Course over Ground:  {self.course_over_ground}\n'
                f'True Heading:        {self.true_heading}\n'
                f'Timestamp:           {self.time_stamp}\n'
                f'CS Unit Flag:        {self.cs_unit}\n'
                f'Display Flag:        {self.display_flag}\n'
                f'Band Flag:           {self.band_flag}\n'
                f'Message22 Flag:      {self.message22_flag}\n'
                f'RAIM status:         {self.raim_flag}\n'
                )

    def get_cs_unit(self):
        self.cs_unit = self.get_flag_bit(141)

    def get_display_flag(self):
        self.display_flagdi = self.get_flag_bit(142)

    def get_band_flag(self):
        self.band_flag = self.get_flag_bit(144)

    def get_message22_flag(self):
        self.message22_flag = self.get_flag_bit(145)


class Extende_ClassB_position_report(Basic_Position):
    '''
    A slightly more detailed report than type 18 for vessels using Class B transmitters.
    Omits navigational status and rate of turn. Fields are encoded as in the common navigation block
    and the Type 5 message. Note that until just before the reserved field at bit 139
    this is identical to message 18. 312 bits total.

    In practice, the information in the ship name and dimension fields is not reliable,
    as it has to be hand-entered by humans rather than gathered automatically from sensors.

    # to be implemented
    # type 19
    The following are derived from parent classes Payloads an d BasicPosition

    message_type: int
    repeat_indicator: int
    mmsi: str
    longitude: float
    latitude: float
    fix_quality: bool = False
    raim_flag: bool = 0  # default not in use
    radio_status: int = 0  # Not implemented
    payload: str  # binary payload
    valid_item: bool
    speed_over_ground: float
    course_over_ground: float
    true_heading: int
    time_stamp: int
    ship_name: str
    dims to bow, ster, port and starboard

    '''

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.get_CLB_SOG()
        self.getfix(56)
        self.get_CLB_longitude()
        self.get_CLB_latitude()
        self.get_CLB_COG()
        self.get_CLB_Tru_head()
        self.get_CLB_timestamp()
        self.get_CLB_vessell_name()
        self.get_CLB_ship_type()
        self.get_CLB_dim_to_bow()
        self.get_CLB_dim_to_stern()
        self.get_CLB_dim_to_port()
        self.get_CLB_dim_to_stbd()
        self.get_CLB_EPFD()
        self.get_CLB_raim_flag()
        self.getr_CLB_dte()

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type:         {self.message_type}\n'
                f'Repeat Indicator:     {self.repeat_indicator}\n'
                f'MMSI:                 {self.mmsi}\n'
                f'Speed over Ground:    {self.speed_over_ground}\n'
                f'Positionn Accuracy:   {self.position_accuracy}\n'
                f'Longitude:            {self.longitude}\n'
                f'Latitude:             {self.latitude}\n'
                f'Course over Ground:   {self.course_over_ground}\n'
                f'True Heading:         {self.true_heading}\n'
                f'Timestamp:            {self.time_stamp}\n'
                f'Vessel Name:          {self.vessel_name}\n'
                f'Ship Type :           {self.ship_type}\n'
                f'Dim to Bow:           {self.dim_to_bow}\n'
                f'Dim to Stern:         {self.dim_to_stern}\n'
                f'Dim to Stbd:          {self.dim_to_stbd}\n'
                f'Fix Type:             {self.fix_quality}\n'
                f'RAIM status:          {self.raim_flag}\n'
                )

    def get_CLB_SOG(self):
        self.getSOG(46, 10)

    def get_CLB_fix(self):
        self.position_accuracy = self.get_flag_bit(56)

    def get_CLB_longitude(self):
        self.get_longitude(57, 28)

    def get_CLB_latitude(self):
        self.get_latitude(85, 27)

    def get_CLB_COG(self):
        self.get_COG(112, 12)

    def get_CLB_Tru_head(self):
        self.get_tru_head(124, 9)

    def get_CLB_timestamp(self):
        self.get_timestamp(133, 6)

    def get_CLB_vessell_name(self):
        self.get_vessel_name(143, 120)

    def get_CLB_ship_type(self):
        self.get_ship_type(263, 8)

    def get_CLB_dim_to_bow(self):
        self.get_dim_to_bow(271, 9)

    def get_CLB_dim_to_stern(self):
        self.get_dim_to_bow(280, 9)

    def get_CLB_dim_to_port(self):
        self.get_dim_to_bow(289, 6)

    def get_CLB_dim_to_stbd(self):
        self.get_dim_to_bow(295, 6)

    def get_CLB_EPFD(self):
        self.get_EPFD(301, 4)

    def get_CLB_raim_flag(self):
        self.raim_flag = self.get_flag_bit(305)

    def getr_CLB_dte(self):
        self.dte = self.get_flag_bit(306)


class Data_link_management_message(Payload):
    # to be implemented
    # type 20

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Aid_to_navigation_report(Basic_Position):
    '''
    Identification and location message to be emitted by aids to navigation such as buoys and lighthouses.

    This message is unusual in that it varies in length depending on the presence and size of the Name Extension field.
     May vary between 272 and 360 bits.
     Will implty that the get_extension text fiunction needs to check where the end is

     The name field is up to 20 characters of 6-bit ASCII.
     If this field is full (has no trailing @ characters) the decoder should interpret the
     Name Extension field later in the message (no more than 14 6-bit characters)
      and concatenate it to this one to obtain the full name.

    [IALA] describes bits 219-248 As "Dimension/Reference for Position",
    implying that it is vessel dimensions as in message type 5.

    The Off-Position Indicator is for floating Aids-to-Navigation only:
    0 means on position;
    1 means off position.
    Only valid if UTC second is equal to or below 59.

    The Virtual Aid flag is interpreted as follows:
    0 = default = real Aid to Navigation at indicated position;
    1 = virtual Aid to Navigation simulated by nearby AIS station.

    If present, the Name Extension consists of packed six-bit ASCII characters
    followed by 0-6 bits of padding to an 8-bit boundary.
    The [IALA] description says "This parameter should be omitted when no more than 20 characters
    for the name of the A-to-N are needed in total. Only the required number of characters should be transmitted,
    i.e. no @-character should be used." A decoder can deduce the bit length of the name extension field
    by subtracting 272 from the total message bit length.

    # type 21

    '''

    aid_type: int  # described in AISDictionaries
    off_position_indicator: bool
    virtual_aid_flag: bool
    name_extension: str
    assigned_mode: bool
    utc_second: int

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)
        self.get_aid_type()
        self.get_NAV_name()
        self.getfix(163)
        self.get_NAV_longitude()
        self.get_NAV_latitude()
        self.get_NAV_dim_to_bow()
        self.get_NAV_dim_to_stern()
        self.get_NAV_dim_to_port()
        self.get_NAV_dim_to_stbd()
        self.get_NAV_EPFD()
        self.get_NAV_UTC_second()
        self.get_NAV_off_position_indicator()
        self.get_NAV_raim_flag()
        self.get_NAV_virtual_aid_flag()
        self.get_NAV_assigned_flag()
        self.get_NAV_name_extension()

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type:             {self.message_type}\n'
                f'Repeat Indicator:         {self.repeat_indicator}\n'
                f'MMSI:                     {self.mmsi}\n'
                f'Aid Type:                 {self.aid_type}\n'
                f'Name:                     {self.vessel_name}\n'
                f'Fix Type:                 {self.fix_quality}\n'
                f'Longitude:                {self.longitude}\n'
                f'Latitude:                 {self.latitude}\n'
                f'Dim to Bow:               {self.dim_to_bow}\n'
                f'Dim to Stern:             {self.dim_to_stern}\n'
                f'Dim to Port:              {self.dim_to_port}\n'
                f'Dim to Stbd:              {self.dim_to_stbd}\n'
                f'EPFD Type:                {self.EPFD_type}\n'
                f'UTC Second:               {self.utc_second}\n'
                f'Off Position Indicator:   {self.off_position_indicator}\n'
                f'RAIM Flag:                {self.raim_flag}\n'
                f'Virtual Aid Flag :        {self.virtual_aid_flag}\n'
                f'Assigned Mode Flag :      {self.assigned_mode}\n'
                f'Name Extension:           {self.name_extension}\n'
                )

    def get_aid_type(self):
        # 5 bits at 38-42 range 0-31 so no range validation required
        self.aid_type = self.binary_item(38, 5)

    def get_NAV_name(self):
        self.get_vessel_name(43, 120)

    def get_NAV_longitude(self):
        self.get_longitude(164, 28)

    def get_NAV_latitude(self):
        self.get_latitude(192, 27)

    def get_NAV_dim_to_bow(self):
        self.get_dim_to_bow(219, 9)

    def get_NAV_dim_to_stern(self):
        self.get_dim_to_stern(228, 9)

    def get_NAV_dim_to_port(self):
        self.get_dim_to_port(237, 6)

    def get_NAV_dim_to_stbd(self):
        self.get_dim_to_stbd(243, 6)

    def get_NAV_EPFD(self):
        self.get_EPFD(249, 4)

    def get_NAV_UTC_second(self):
        self.utc_second = self.binary_item(253, 6)

    def get_NAV_off_position_indicator(self):
        self.off_position_indicator = self.get_flag_bit(259)

    def get_NAV_raim_flag(self):
        self.raim_flag = self.get_flag_bit(268)

    def get_NAV_virtual_aid_flag(self):
        self.virtual_aid_flag = self.get_flag_bit(269)

    def get_NAV_assigned_flag(self):
        self.assigned_mode = self.get_flag_bit(270)

    def get_NAV_name_extension(self):

        # needs work to check for length of payload to avoid overun
        extlen = len(self.payload) - 272
        # allowance for no name extension field
        if extlen <= 0:
            self.name_extension = ''
            self.vessel_name = self.vessel_name + self.name_extension
            return

        while extlen % 6 != 0:
            extlen -= 1

        self.name_extension = self.extract_text(272, extlen)

        while self.name_extension[len(self.name_extension) - 1] == '@' and len(self.name_extension) != 1:
            self.name_extension = self.name_extension[0:len(self.name_extension) - 1]

        # accounting for null extension
        if len(self.name_extension) == 1 and self.name_extension == '@':
            self.name_extension = ''

        self.vessel_name = self.vessel_name + self.name_extension


class Channel_management(Payload):
    # to be implemented
    # type 22

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Group_assigment_command(Payload):
    # to be implemented
    # type 23

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Static_data_report(Basic_Position):
    '''
    # to be implemented
    # type 24
    Equivalent of a Type 5 message for ships using Class B equipment.
    Also used to associate an MMSI with a name on either class A or class B equipment.

    A "Type 24" may be in part A or part B format; According to the standard,
    parts A and B are expected to be broadcast in adjacent pairs;
    in the real world they may (due to quirks in various aggregation methods) be separated
    by other sentences or even interleaved with different Type 24 pairs;
    decoders must cope with this.
    The interpretation of some fields in Type B format changes depending on the range of the Type B MMSI field.
    160 bits for part A, 168 bits for part B.

    According to the standard, both the A and B parts are supposed to be 168 bits.
    However, in the wild, A parts are often transmitted with only 160 bits,
    omitting the 'spare' 7 bits at the end. Implementers should be permissive about this.

    Many of the parameters are inherited from classes Playload and BasicPosition

    '''

    part_number: int  # determines whether a "Part A"or "Part B" packet

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)
        self.payload = p_payload
        self.create_mmsi()
        self.get_part_number()

    def get_part_number(self):
        self.part_number = self.binary_item(38, 2)

        if not (0 <= self.part_number <= 1):
            # logging.error('Invalid Part Number ' + '{:d}'.format(self.part_number) + ' returned in Type25 Base' )
            self.valid_item = False
            raise ValueError


class Static_data_PartA(Static_data_report):
    '''
    # to be implemented
    # type 24
    Equivalent of a Type 5 message for ships using Class B equipment.
    Also used to associate an MMSI with a name on either class A or class B equipment.

    A "Type 24" may be in part A or part B format; According to the standard,
    parts A and B are expected to be broadcast in adjacent pairs;
    '''

    part_number: int  # determines whether a "Part A"or "Part B" packet

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.get_24_vessel_name()
        pass

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Message Type:         {self.message_type}\n'
                f'Repeat Indicator:     {self.repeat_indicator}\n'
                f'MMSI:                 {self.mmsi}\n'
                f'Part_number:    {self.part_number}\n'
                f'Vessel Name:          {self.vessel_name}\n'
                )

    def get_24_vessel_name(self):
        self.get_vessel_name(40, 120)


class Static_data_PartB(Static_data_report):
    '''
    # to be implemented
    # type 24
    Equivalent of a Type 5 message for ships using Class B equipment.
    Also used to associate an MMSI with a name on either class A or class B equipment.

    A "Type 24" may be in part A or part B format; According to the standard,
    parts A and B are expected to be broadcast in adjacent pairs;

    Interpretation of the 30 bits 132-162 in Part B is variable.
    If the MMSI at 8-37 is that of an auxiliary craft,
    the entry is taken to refer to a small attached auxiliary vessel
    and these 30 bits are read as the MMSI of the mother ship.
    Otherwise the 30 bits describe vessel dimensions as in Message Type 5.

    According to [MMSI], an MMSI is associated with an auxiliary craft when it is of the form 98XXXYYYY, where
    (1) the '98' in positions 1 and 2 is required to designate an auxiliary craft,
    (2) the digits XXX in the 3, 4 and 5 positions are the MID
    (the three-digit country code as described in [ITU-MID])
    and
    (3) YYYY is any decimal literal from 0000 to 9999.

    '''

    vendor_id: str
    pre1371_4_vendor_id: str
    unit_model_code: int
    callsign: str
    mothership_mmsi: str

    def __init__(self, p_payload):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        super().__init__(p_payload)

        self.get_24_ship_type()
        self.get_vendor_id()
        self.get_unit_model_code()
        self.get_serial_number()
        self.get_callsign()
        self.get_24_dim_to_bow()
        self.get_24_dim_to_stern()
        self.get_24_dim_to_port()
        self.get_24_dim_to_stbd()
        self.get_mothership_mmsi()

        pass

    def __repr__(self):
        if self.mmsi[0:2] == '98':
            return (f'{self.__class__.__name__}\n'
                    f'Message Type:         {self.message_type}\n'
                    f'Repeat Indicator:     {self.repeat_indicator}\n'
                    f'MMSI:                 {self.mmsi}\n'
                    f'Part_number:          {self.part_number}\n'
                    f'Ship Type :           {self.ship_type}\n'
                    f'Vendor ID:            {self.vendor_id}\n'
                    f'Pre1371_4_Vendor ID:  {self.pre1371_4_vendor_id}\n'
                    f'Unit Model Code:      {self.unit_model_code}\n'
                    f'Serial Number:        {self.serial_number}\n'
                    f'Callsign:             {self.callsign}\n'
                    f'Mothership MMSI:      {self.mothership_mmsi}\n'
                    )
        else:
            return (
                f'{self.__class__.__name__}\n'
                f'Message Type:         {self.message_type}\n'
                f'Repeat Indicator:     {self.repeat_indicator}\n'
                f'MMSI:                 {self.mmsi}\n'
                f'Part_number:          {self.part_number}\n'
                f'Ship Type :           {self.ship_type}\n'
                f'Vendor ID:            {self.vendor_id}\n'
                f'Pre1371_4_Vendor ID:  {self.pre1371_4_vendor_id}\n'
                f'Unit Model Code:      {self.unit_model_code}\n'
                f'Serial Number:        {self.serial_number}\n'
                f'Callsign:             {self.callsign}\n'
                f'Dim to Bow:           {self.dim_to_bow}\n'
                f'Dim to Stern:         {self.dim_to_stern}\n'
                f'Dim to Port:          {self.dim_to_port}\n'
                f'Dim to Stbd:          {self.dim_to_stbd}\n'
            )

    def get_24_ship_type(self):
        # ship type described in AISDictionaries
        # validation done in class BasicPosition
        # testing will only need to check if a correct name returned - checks bit location parameters
        self.get_ship_type(40, 8)

    def get_vendor_id(self):
        '''
        Bits 48-89 are as described in ITU-R 1371-4.
        In earlier versions to 1371-3 this was one sixbit-encoded 42-bit (7-character) string field,
        the name of the AIS equipment vendor.
        The last 4 characters of the string are reinterpreted as a model/serial numeric pair.
        It is not clear that field practice has caught up with this incompatible change.
        Implementations would be wise to decode that but span in both ways and trust human eyes
        to detect when the final 4 characters of the string or the model and serial fields are garbage.

        :return:
        '''
        # 3 six bit characters (or possibly one 7 character string in 1371-3)

        self.vendor_id = self.extract_text(48, 18)
        self.pre1371_4_vendor_id = self.extract_text(48, 42)

    def get_unit_model_code(self):
        # int 4 bits
        self.unit_model_code = self.binary_item(66, 4)

    def get_serial_number(self):
        self.serial_number = self.binary_item(70, 20)

    def get_callsign(self):
        self.callsign = self.extract_text(90, 42)

    def get_24_dim_to_bow(self):
        self.get_dim_to_bow(132, 9)

    def get_24_dim_to_stern(self):
        self.get_dim_to_stern(141, 9)

    def get_24_dim_to_port(self):
        self.get_dim_to_port(150, 6)

    def get_24_dim_to_stbd(self):
        self.get_dim_to_stbd(156, 6)

    def get_mothership_mmsi(self):
        self.mothership_mmsi = '{:09d}'.format(self.binary_item(132, 30))


class Single_slot_binary_message(Payload):
    # to be implemented
    # type 25

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Multiple_slot_binary_message(Payload):
    # to be implemented
    # type 26

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Long_range_AIS_broadcast_message(Basic_Position):
    GNSS_position_status: bool

    def __init__(self, p_payload):
        super().__init__(p_payload)
        self.payload = p_payload
        self.create_mmsi()
        self.fix_quality = self.get_flag_bit(38)
        self.raim_flag = self.get_flag_bit(39)
        self.navigation_status = self.get_nav_status(38, 4)
        self.get_27longitude(44, 18)
        self.get_27latitude(62, 17)
        self.getSOG(79, 6)
        self.get_COG(85, 9)
        self.GNSS_position_status = self.get_flag_bit(94)

        pass

    def __repr__(self):
        pass

    def get_27longitude(self, startpos: int, length: int = 18) -> None:
        # longitude is in various positions in differing blocks
        # in long distance AIS Broadcast the scaling factors have been changed
        self.longitude = float(self.signed_binary_item(startpos, length)) / 600.0

    def get_27latitude(self, startpos: int, length: int = 17) -> None:
        # longitude is in various positions in differing blocks
        # in long distance AIS Broadcast the scaling factors have been changed
        self.latitude = float(self.signed_binary_item(startpos, length)) / 600.0


class Fragments:
    #
    # class to allow handling of fragments
    # input parameter message is the whole AIS string to be split to alllow consolidation of
    # payloads
    # as well as the normal payload it uses the fragment_count, fragment_number fields

    # if a stream with fragment count > 1 found pass it to this and hopefully when enough
    # portions are found a success = True (1) will be returned and a merged payload and payload_length will be valid
    # using fragment_number can detyect if all fragments are available before merging.
    # a cleanm up will also be done to flush out stale fragments from Fragment Dictionary.
    #       Timeout set in Global_Parameters
    #

    # current_time: datetime
    # payload: str
    # mmnsi: str
    # f_no: int
    # f_count: int
    # messid: int
    # data: tuple
    # success: bool
    # new_bin_payload: str

    def __init__(self, binary_payload: str, fragment_count: int, fragment_number: int, message_id: int):

        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        # print("initialing fragment")
        self.current_time = datetime.utcnow()
        self.f_count = fragment_count
        self.f_no = fragment_number
        self.messid = message_id
        self.payload = binary_payload
        self.data = self.f_count, self.f_no, self.payload, self.current_time
        self.inkey: str = ''
        self.rtime: datetime = datetime.now()
        self.success = False
        self.new_bin_payload = ''

        # print(self)

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Current Time:         {self.current_time}\n'
                f'Fragment Count:       {self.f_count}\n'
                f'Fragment Number:      {self.f_no}\n'
                f'Payload:              {self.payload}\n'
                f'The Tuple :           {self.data}\n'
                f'Inkey:                {self.inkey}\n'
                f'Success Flag:         {self.success}\n'
                f'New Payload:          {self.new_bin_payload}\n'
                )

    def put_frag_in_dict(self, merge: bool = False):
        # create a dictionary key comprising fragment_number and message_id
        key = str(self.messid) + ',' + str(self.f_no)
        Global.FragDict.update({key: self.data})
        logging.debug('In Fragment.put_frag_in_dict dictionary  = ', Global.FragDict)
        # print('In Fragment.put_frag_in_dict dictionary  = ', Global.FragDict)

        # having put the fragment into the dictionary we need to check if we can amalgemate fragments

        if merge:
            self. success, self.new_bin_payload = self.match_fragments(key)

    def match_fragments(self, key: str) -> tuple:
        # pass through Global.Fragdict looking for identical keys
        # look for common message ids, strip off the fragment number from the key passed in
        inkey = key.split(',')[0]
        fraglist = {}
        for fkey, data in Global.FragDict.items():
            if fkey.strip(',')[0] == inkey:
                fno = data[1]
                pload = data[2]
                fraglist.update({fno: pload})

            #
            # now while we are parsing dictionary clean out stale records
            if (datetime.utcnow() - data[3]).total_seconds() > Global.FragDictTTL:
                logging.info('In Fragments.match_records deleting outdated record ', fkey, data)
                print('In Fragments.match_records deleting outdated record ', fkey, data)
                Global.FragDict.pop(fkey)

        # how many records did we find?

        nr_recs = len(fraglist)
        #print('len fraglist', nr_recs)

        # compare this with the number of fragments expected
        new_bin_payload = ''
        if nr_recs == self.f_count:
            # got requisite number of fragments
            # get fragments in order
            for fnumber in range(1, nr_recs + 1):
                new_bin_payload = new_bin_payload + fraglist[fnumber]
                #print('ne payload ', new_bin_payload)
                # and flush the fragment records from Global.Fragdict
                #print('deleting ', inkey + ',' + str(fnumber) )
                Global.FragDict.pop(inkey + ',' + str(fnumber))
            self.success = True
        else:
            # not got all bits yet
            new_bin_payload = ''

        return self.success, new_bin_payload


class AISStream:
    # comprises the entire AIS message as received

    packet_id: str
    fragment_count: int
    fragment_number: int
    message_id: int  # may be null
    channel: str
    payload: str
    binary_payload: str
    binary_payload_length: int
    byte_payload: bytearray
    byte_payload_length: int
    trailer: str
    valid_message: bool
    message_type: int  # only used to validate payload

    def __init__(self, input: str):

        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')

        self.valid_message = True
        self.split_string(input)

        # only if crude validation passed continue
        if self.valid_message:
            # now create the string form binary_payload
            self.create_binary_payload()  # now create the string form binary_payload
            self.create_bytearray_payload()  # not currently used but for future usage
            #
            # before we return the stream will be crudely validated

            self.validate_stream()

    def split_string(self, stream: str):
        self.valid_message = True
        str_split: list = stream.split(',')

        if (str_split[0] == '!AIVDM') or (str_split[0] == '!AIVDO'):
            self.packet_id = str_split[0]
        else:
            # logging.error("In AISStream - packet_type not in AIVDM or AIVDO " + str_split[0])
            self.valid_message = False

        try:
            self.fragment_count = int(str_split[1])
        except ValueError:
            # logging.error("In AISStream - fragment count not numeric " + str_split[1])
            self.fragment_count = 0
            self.valid_message = False
        try:
            self.fragment_number = int(str_split[2])
        except ValueError:
            # logging.error("In AISStream - fragment number not numeric " + str_split[2])
            self.fragment_number = 0
            self.valid_message = False
        try:
            if len(str_split[3]) > 0:

                self.message_id = int(str_split[3])
            else:
                # null message_id
                self.message_id = 0
        except ValueError:
            # logging.error("In AISStream - message_id not numeric " + str_split[3])
            self.message_id = 0
            self.valid_message = False

        self.channel = str_split[4]
        if self.channel not in ['A', 'B', '1', '2']:
            # logging.error('In AISStream.split_string - invalid channel ' + str_split[4])
            self.valid_message = False

        self.payload = str_split[5]
        # validate message type from first six bits of self.payload
        # this really should live with payload processing but for easy dumping of stream
        # will also be done here

        # only applies for packet where fragment_number = 1, for other packets ignored
        if self.fragment_number == 1:
            # grab first six bits - by shifting right the bits related to repeat indicator
            messbyte: int = self.m_to_int(self.payload[0])
            logging.debug('In AISStream - messbyte = ' + '{:0d}'.format(messbyte))
            if not (1 <= messbyte <= 27):
                # logging.error('In AISStream.split_string - invalid message+type ' + str_split[5])
                self.valid_message = False
            else:
                self.message_type = messbyte

        self.trailer = str_split[6]

    def create_binary_payload(self) -> None:
        # based on using a supersized string rather than bytearray
        #
        # print("ïnput payload "+ p_payload)
        #
        # define a null string
        _abinary_payload = ''
        _byte_payload = bytearray()
        _byte_payload.extend(self.payload.encode())
        # print('bytearray version of payload\n', _byte_payload,
        #       '\nhex version\n', _byte_payload.hex(),
        #       '\nfrom \n',p_payload)

        for i in range(0, len(self.payload)):
            # print('in create binary payload ', len(p_payload), i)
            # iterate through the string payload masking to lower 6 bits
            xchar = self.payload[i]

            nibble = self.m_to_int(xchar) & 0x3F  # ensures only 6 bits presented
            # print(xchar, nibble, p_payload[i], i, len(p_payload))

            logging.debug('nibble', bin(nibble))

            # now append the nibble to the stream
            _abinary_payload = _abinary_payload + format(nibble, '06b')

        _binary_payload = _abinary_payload

        # print(_abinary_payload)

        self.binary_payload = _abinary_payload

    def create_bytearray_payload(self) -> tuple:
        # based on using a supersized string rather than bytearray
        #
        printdiag = False
        #
        # define a null bytearray
        _byte_payload = bytearray()
        # convert from str to the bytearray
        _byte_payload.extend(self.payload.encode())
        # print('bytearray version of payload\n', _byte_payload,
        #       '\nhex version\n', _byte_payload.hex(),
        #       '\nfrom \n',p_payload)

        newbytes = bytearray()
        _binlength = len(self.payload)
        for i in range(0, len(self.payload)):
            if printdiag:
                print('in create binary payload ', len(self.payload), i)
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
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 1:
                    # mask to 2 MSB and put them into outbyte
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x30) >> 4) + _byte_payload[outbyte]
                    # now put 4 LSB into MSB of next outbyte
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1
                    _byte = (newbytes[innibble] & 0x0F) << 4
                    _byte_payload.extend(struct.pack("B", _byte))
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 2:
                    # mask  four MSB, move to lower bits  of outbyte
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x3F) >> 2) + _byte_payload[outbyte]
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1
                    # put 2 LSB into MSB of next outbyte
                    _byte_payload.extend(struct.pack("B", (newbytes[innibble] & 0x03) << 6))
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))

                case 3:
                    # put 6 MSBbits into LSB of next outbyte
                    _byte_payload[outbyte] = ((newbytes[innibble] & 0x3F)) + _byte_payload[outbyte]
                    logging.debug("nibble {} input byte {:08b}  output byte number {} output byte content " +
                                  "{:08b}".format(innibble, newbytes[innibble], outbyte, _byte_payload[outbyte]))
                    outbyte += 1

                case _:
                    _byte_payload = bytearray()
                    _binlength = 0
                    raise RuntimeError("error in selecting bytes in create_bytearray_payload")

        logging.debug(_byte_payload.hex())
        self.byte_payload = _byte_payload

    def m_to_int(self, parameter: str) -> int:
        # takes in a encoded string of variable length and returns positive integer
        my_int: int
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

    def validate_stream(self) -> bool:

        # first check packet_id
        if self.packet_id != '!AIVDM' and self.packet_id != '!AIVDO':
            return False

        # then check self.self.fragment_count
