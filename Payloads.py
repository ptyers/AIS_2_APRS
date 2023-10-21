from datetime import datetime, timezone
import logging
from GlobalDefinitions import Global
import struct
import sys

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
        # p_payload is binary_payload string
        self.payload = p_payload

        self.message_type = self.binary_item(0, 6)
        if not (1 <= self.message_type <= 27):
            logging.error("In Payload.__ini__ - Invalid Message Type not in 1-27")
            raise RuntimeError("Invalid Message Type not in 1-27")

        self.mmsi = self.create_mmsi()

        self.repeat_indicator = self.binary_item(6, 2)
        if not (0 <= self.repeat_indicator <= 3):
            logging.error("In Payload.__ini__ - Invalid Repeat Indicator not in 0-3")
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
            logging.error(
                "Error in ExtractString startpos = " + str(startpos) + " blength = " + str(
                    blength) + "binary_length = ")
            logging.error("Exception while ExtractString startpos", sys.exc_info()[0])
            raise

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
            logging.error("In Payload.binary_item() - Request to extract more bits which overrun end of binary payload")
            raise RuntimeError("Request to extract more bits which overrun end of binary payload")
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
        self.longitude = float(self.signed_binary_item(startpos, length))/600000

    def get_latitude(self, startpos: int, length: int = 27):
        # longitude is in various positions in differing blocks
        x = self.signed_binary_item(startpos, length)
        self.latitude = float(self.signed_binary_item(startpos, length)) / 600000

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
            logging.error("In Payload.signed_binary_item() - "
                          + "Request to extract more bits which overrun end of binary payload")
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
        #print('in get_flag_bit position, value ', position, self.binary_item(position, 1), self.payload[60])
        if self.binary_item(position, 1) == 1:
            self.raim_flag = True
        else:
            self.raim_flag = False


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


class CNB(Payload):
    # additional fields

    navigation_status: int
    rate_of_turn: float
    speed_over_ground: float
    position_accuracy: bool
    course_over_ground: float
    true_heading: int
    time_stamp: int
    maneouver_indicator: int

    def __init__(self, p_payload: str):
        super().__init__(p_payload)
        self.get_nav_status()
        self.get_ROT()
        self.getSOG()
        self.get_pos_accuracy()
        self.get_longitude(61, 28)
        self.get_latitude(89, 27)
        self.get_COG()
        self.get_tru_head()
        self.get_timestamp()
        self.get_man_indic()
        self.getfix(60)

        pass

    def get_nav_status(self) -> None:
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
        self.navigation_status = self.binary_item(38, 4)

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

        :return:
            sets mycnb.rate_of_turn (float)
        '''
        # ROT - Rate of Turn is scaled by 1000
        # signed integer scaled to float then calculated as divide by 4.733, retain sign but square it

        irot = self.signed_binary_item(42, 8)
        if irot >= 0:
            self.rate_of_turn = (float(irot) / 4.733) ** 2
        else:
            self.rate_of_turn = - (float(abs(irot)) / 4.733) ** 2

    def getSOG(self) -> None:
        '''

        Speed over ground is in 0.1-knot resolution from 0 to 102 knots.
        Value 1023 indicates speed is not available,
         value 1022 indicates 102.2 knots or higher.
        :return:
            set mycnb.speed_over_ground (float)
        '''

        intval = self.binary_item(50, 10)
        if 0 <= intval <= 1023:
            self.speed_over_ground = float(intval) / 10.0
        else:
            # should not happen max value 1023
            self.valid_item = False
            logging.error('In CNB.get_SOG - value outside range 0-102.3' , intval)
            raise RuntimeError('In CNB.get_SOG - value outside range 0-102.3' , intval)





    def get_COG(self) -> None:
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
            logging.error('In CNB.get_COG - value outside range 0-360'+ '{:d}'.format(intval))
            raise ValueError('In CNB.get_COG - value outside range 0-360 ' + '{:d}'.format(intval))


    def get_tru_head(self) -> None:
        '''
            true heading is integer value
            0-359 degrees
            511 not avaiulable

            routine checks validity sets to False if outside 0-259 and/or 511

        :return:
            sets mycnb.true_heading (integer)
        '''

        itru = self.binary_item(128, 9)
        if 0 <= itru <= 259 or itru == 511:
            self.true_heading = itru
        else:
            self.valid_item = False
            logging.error('In CNB.get_tru_head - value outside range 0-259 or != 511', itru)
            raise ValueError('In CNB.get_tru_head - value outside range 0-259 or != 511', itru)

    def get_pos_accuracy(self) -> bool:
        '''

        The position accuracy flag indicates the accuracy of the fix.
        A value of 1 indicates a DGPS-quality fix with an accuracy of < 10ms. 0,
        the default, indicates an unaugmented GNSS fix with accuracy > 10m.

        in bit 60 of binary payload
        :return:
            sets mycnb.position_accuracy (bool)
        '''

        self.position_accuracy = self.get_flag_bit(60)

    def get_timestamp(self) -> None:
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
            logging.error('In CNB.get_timestamp - value outside range 0-63', intval)
            raise RuntimeError('In CNB.get_timestamp - value outside range 0-63', intval)


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
            logging.error('In CNB.get_man indicator - value outside range 0-2' +'{:d}'.format(intval))
            raise ValueError('In CNB.get_man indicator - value outside range 0-2' +'{:d}'.format(intval))


class Basestation(Payload):
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
        super().__init__(p_payload)
        self.get_year()
        self.get_month()
        self.get_day()
        self.get_hour()
        self.get_minute()
        self.get_second()
        self.get_EPFD()
        self.getfix(78)
        self.getRAIMflag(148)

    def get_year(self):
        self.year = self.binary_item(38, 14)

    def get_month(self):
        self.month = self.binary_item(52, 4)

    def get_day(self):
        self.day = self.binary_item(56, 5)

    def get_hour(self):
        self.year = self.binary_item(61, 5)

    def get_minute(self):
        self.minute = self.binary_item(66, 6)

    def get_second(self):
        self.second = self.binary_item(72, 6)

    def get_EPFD(self):
        # enumerated 0-8, but other may appear, 15 not uncommen
        self.EPFD_type = self.binary_item(134, 4)

        pass


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


class SAR_aircraft_position_report(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


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
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Safety_relatyed_acknowledgement(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Safety_related_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Interrogation(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class DGNS_broadcast_binaty_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class ClassB_position_report(Payload):
    # to be implemented
    # type 18

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Extende_ClassB_position_report(Payload):
    # to be implemented
    # type 19

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Data_link_management_message(Payload):
    # to be implemented
    # type 20

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


class Aid_to_navigation_report(Payload):
    # to be implemented
    # type 21

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


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


class Static_data_report(Payload):
    # to be implemented
    # type 24

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


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


class Long_range_AIS_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)

        pass


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

    current_time: datetime
    payload: str
    mmnsi: str
    f_no: int
    f_count: int
    messid: int
    ftuple: tuple
    success: bool
    new_bin_payload: str

    def __init__(self, binary_payload: str, fragment_count: int, fragment_number: int, message_id: int):

        current_time = datetime.utcnow()
        f_count = fragment_count
        f_no = fragment_number
        messid = message_id
        payload = binary_payload
        ftuple = [f_count, f_no, messid, payload, current_time]
        inkey: str
        rtime: datetime
        success = False
        new_bin_payload = ''

        pass

    def put_frag_in_dict(self):
        # create a dictionary key comprising fragment_number and message_id
        key = str(self.f_no) + '-' + str(self.messid)
        Global.FragDict.update(key, self.ftuple)
        logging.debug('In Fragment.put_frag_in_dict dictionary  = ', Global.FragDict)

        pass

    def match_fragments(self, key: str):
        # pass through Global.Fragdict looking for identical keys
        inkey = key
        rtime = datetime.now()
        fraglist = []
        for fkey, ftuple in Global.FragDict.items():
            if fkey == key:
                fraglist.extend(ftuple)
            #
            # now while we are parsing dictionary clean out stale records
            if (datetime.utcnow() - ftuple[4]).total_seconds() > Global.FragDictTTL:
                Global.FragDict.pop(fkey)

        # how many records did we find?

        nr_recs = len(fraglist)

        # compare this with the number of fragments expected
        if nr_recs == self.f_count:
            # got requisite number of fragments
            # get fragments in order
            lump = 1
            while lump <= nr_recs:
                for ftuple in fraglist:
                    if ftuple[1] == 1:
                        self.new_bin_payload = ftuple[3]
                    elif ftuple[1] == lump:
                        self.new_bin_payload = self.new_bin_payload + ftuple[3]
                lump += 1
            self.success = True
        else:
            # not got all bits yet
            pass

        return self.success, self.new_bin_payload


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
            logging.error("In AISStream - packet_type not in AIVDM or AIVDO\n" + str_split[0])
            self.valid_message = False

        try:
            self.fragment_count = int(str_split[1])
        except ValueError:
            logging.error("In AISStream - fragment count not numeric\n" + str_split[1])
            self.fragment_count = 0
            self.valid_message = False
        try:
            self.fragment_number = int(str_split[2])
        except ValueError:
            logging.error("In AISStream - fragment number not numeric\n" + str_split[2])
            self.fragment_number = 0
            self.valid_message = False
        try:
            if len(str_split[3]) > 0:

                self.message_id = int(str_split[3])
            else:
                # null message_id
                self.message_id = 0
        except ValueError:
            logging.error("In AISStream - message_id not numeric\n" + str_split[3])
            self.message_id = 0
            self.valid_message = False

        self.channel = str_split[4]
        if self.channel not in ['A', 'B', '1', '2']:
            logging.error('In AISStream.split_string - invalid channel\n' + str_split[4])
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
                logging.error('In AISStream.split_string - invalid message+type\n' + str_split[5])
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
