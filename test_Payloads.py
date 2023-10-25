from unittest import TestCase
from AISDictionary import AISDictionaries
import Payloads
import random
import logging
import math


class TestBinary_addressed_message(TestCase):
    pass


class TestBinary_acknowledge(TestCase):
    pass


class TestBinary_broadcast_message(TestCase):
    pass


class TestSAR_aircraft_position_report(TestCase):
    pass


class TestUTC_date_enquiry(TestCase):
    pass


class TestUTC_date_response(TestCase):
    pass


class TestAddressed_safety_related_message(TestCase):
    pass


class TestSafety_relatyed_acknowledgement(TestCase):
    pass


class TestSafety_related_broadcast_message(TestCase):
    pass


class TestInterrogation(TestCase):
    pass


class TestDGNS_broadcast_binaty_message(TestCase):
    pass


class TestClassB_position_report(TestCase):
    pass


class TestExtende_ClassB_position_report(TestCase):
    pass


class TestData_link_management_message(TestCase):
    pass


class Test_aid_to_navigation_report(TestCase):
    pass


class TestChannel_management(TestCase):
    pass


class TestGroup_assigment_command(TestCase):
    pass


class TestStatic_data_report(TestCase):
    pass


class TestSingle_slot_binary_message(TestCase):
    pass


class TestMultiple_slot_binary_message(TestCase):
    pass


class TestLong_range_AIS_broadcast_message(TestCase):
    pass


class TestFragments(TestCase):

    def test_put_frag_in_dict(self):
        self.fail()

    def test_match_fragments(self):
        self.fail()


class TestPayload(TestCase):

    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        mystream = Payloads.AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05')
        return diction, mystream

    def test_create_mmsi(self):
        diction, mystream = self.initialise()

        print('Testing create mmsi')

        smmsi_list: list = [
            '850312345', '503543210', '050398765', '005037651', '111504678',
            '998761234', '984135432', '970654987', '972654321', '974765432',
            '999999999'
        ]

        # the mmsi field is bits 8-37 of the binary payload string
        # so split the mystream.binary_payload generated in the initialiastion into three parts
        # bits 0-7, bits 38-end and substitute the 30 bits that are the mmsi field

        header: str = '00010000'
        trailer: str = mystream.binary_payload[38:]

        for ssm in smmsi_list:
            sm: str = ssm
            mmsibits = '{:030b}'.format(int(sm))
            mypayload = Payloads.Payload(header + mmsibits + trailer)

            try:
                mypayload.payload = header + mmsibits + trailer
                mypayload.create_mmsi()
                ommsi: str = mypayload.create_mmsi()

                self.assertEqual(sm, ommsi, "Failed in create mmsi integer form")
            except:
                pass

    def test_extract_int(self):
        '''
               Produces random number in rage 0 to 999999999 and sets up fake binary_payload string
               then extracts that binary number from the string using AIS_Data.Binary_item
               effectively same test as for Binary_item
               '''
        # some necessary preconfig
        diction, mystream = self.initialise()

        mypayload = Payloads.Payload(mystream.binary_payload)

        print("Testing extract_int")
        # Create fake AIS payload with a random binary number in bits 8 to 37
        for i in range(10):
            fakestream: str = '00010000'
            faketail: str = '000000000000000000000000000000'

            testnumber: int = random.randint(0, 999999999)
            strnumber: str = "{:030b}".format(testnumber)
            # print('strnumber =                 ', strnumber)
            fakestream = fakestream + strnumber + faketail
            mypayload.payload = fakestream
            # print('fakestream          ', fakestream)
            intmmsi = mypayload.extract_int(8, 30)
            self.assertEqual(testnumber, intmmsi, "In Payload - Failed in test_extract_int")

    def test_extract_string(self):
        '''
                Create dummy binary payload including some test strings use Extract_String to recover text
        :return:
            string text to be compared
        '''
        print("Testing ExtractString")
        # some necessary preconfig
        diction, mystream = self.initialise()

        mypayload = Payloads.Payload(mystream.binary_payload)

        fakestream: str = '00010000'
        faketail: str = '11111111111111111111'

        testtext: str = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw01234567890:;<>=?@@AB'

        for _ in range(10):

            for ik in range(len(testtext)):
                fakestream = diction.makebinpayload(fakestream, testtext[ik])
            fakestream = fakestream + faketail

            # set this as "binary_payload" in AIS_Data and set its length as 6 times the text length plus
            # additional head/tail bits (28)
            mypayload.payload = fakestream

            # nominal start of text stream
            basepos: int = 8
            rndstrt = random.randint(0, len(testtext) - 1)
            # can pick out any random portion no more than 30chars size
            # then check if the combination of start posn plus length will not exceed binary_payload length
            rndlen = random.randint(1, 30)
            while rndstrt * 6 + rndlen * 6 > len(testtext) * 6:
                rndlen = random.randint(1, 30)
            # then extract the text segment we will be recovering from the binary_payload
            rndtext = testtext[rndstrt:rndstrt + rndlen]
            blklen = rndlen * 6

            logging.debug("DEBUG binary_payload from which string will be extracted\n",
                          mystream.binary_payload)
            outstr = mypayload.extract_string(rndstrt * 6 + 8, rndlen * 6)
            logging.debug('Extracted string ', outstr)

            self.assertEqual(rndtext, outstr, "In Payload - Failed in Extract_String")

    def test_binary_item(self):
        '''
        Produces random number in rage 0 to 999999999 and sets up fake binary_payload string
        then extracts that binary number from the string using AIS_Data.Binary_item
        '''
        print("Testing ExtractString")
        # some necessary preconfig
        diction, mystream = self.initialise()

        mypayload = Payloads.Payload(mystream.binary_payload)

        print("Testing Binary_item")
        # Create fake binary payload with a random binary number in bits 8 to 37
        for i in range(10):
            fakestream: str = '00010000'
            faketail: str = '000000000000000000000000000000'

            testnumber: int = random.randint(0, 999999999)
            strnumber: str = "{:030b}".format(testnumber)
            fakestream = fakestream + strnumber + faketail
            mypayload.payload = fakestream
            intmmsi = mypayload.binary_item(8, 30)
            self.assertEqual(testnumber, intmmsi, "FAiled in test_binary_item")

    def test_m_to_int(self):
        '''
        m_to_int takes in single armoured (encoded) character and returns a binary value

        :return:
            binary value as per Dictionaries.payload_armour
        '''

        print("Testing m_to_int")

        # some necessary preconfig
        diction, mystream = self.initialise()

        mypayload = Payloads.Payload(mystream.binary_payload)

        for char, str_val in diction.payload_armour.items():
            # print('character, string value', char, str_val )
            bin_val = int(str_val, 2)
            ret_val = mypayload.m_to_int(char)
            self.assertEqual(bin_val, ret_val, 'In Payload.m_to_int - returned binary does not match encoded char')

    def test_remove_at(self):
        '''
        remove_at strips trailing @ from string values

        :return:
            string without trailing @
        '''

        print("Testing remove_at")

        # some necessary preconfig
        diction, mystream = self.initialise()

        mypayload = Payloads.Payload(mystream.binary_payload)

        teststring = 'ABC'
        for i in range(1, 10):
            out_string = mypayload.remove_at(teststring)
            self.assertEqual('ABC', out_string,
                             "In Payload.remove_at - the returned string has not had trailing @ removed ")
            teststring = teststring + '@'

    def test_remove_space(self):
        '''
        remove_at strips trailing spaces from string values

        :return:
            string without trailing spaces
        '''

        print("Testing remove_space")

        # some necessary preconfig
        diction, mystream = self.initialise()
        mypayload = Payloads.Payload(mystream.binary_payload)

        teststring = 'ABC'
        for i in range(1, 10):
            out_string = mypayload.remove_space(teststring)
            self.assertEqual('ABC', out_string,
                             "In Payload.remove_at - the returned string has not had trailing spaces removed ")
            teststring = teststring + ' '

    def test_signd_bin_last_long(self):
        '''
           signed_binary_item takes in a set of parameters start position, number of bits (blength)
           and extracts string of bits from the binary_payload.
           if MSBit is 1 the negetive. Do twos complement arithmetic to return a signed integer

            :return:
                signed integer value which will need scaling if necessary
            '''

        print("Testing signed binary item")

        # some necessary preconfig
        diction, mystream = self.initialise()
        mypayload = Payloads.Payload(mystream.binary_payload)
        # zero degrees
        fakestream: str = '00010000'
        faketail: str = '000000000000000000000000000000'
        # testnumber: int = random.randint(0, 999999999)
        strnumber: str = "{:028b}".format(0)
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(0, intmmsi, "In Payload.signed_binary_int - Offered 0 but got non zero")
        # longitude
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(0.0, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for zero degrees got non zero back')
        # latitude
        strnumber: str = "{:027b}".format(0)
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(0.0, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for zero degrees got non zero back')

        # 1 degree
        strnumber: str = "{:028b}".format(1)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(1, intmmsi, "In Payload.signed_binary_int - Offered 1 but got not 1")
        # longitude
        strnumber: str = "{:028b}".format(1 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(1.0, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for one degrees one did not return')
        # latitude
        strnumber: str = "{:027b}".format(1 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(1.0, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for zero degrees one did not return')

        # minus 1 degree
        strnumber: str = "{:028b}".format(-1)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(-1, intmmsi, "In Payload.signed_binary_int - Offered -1 but got not -1")
        # longitude
        strnumber: str = "{:028b}".format(-1 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(-1.0, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for minus one did not return')
        # latitude
        strnumber: str = "{:027b}".format(-1 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(-1.0, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for minus one did not return')

        # 181 degrees - indicates not available
        mynumb = 181 * 600000
        strnumber: str = "{:028b}".format(mynumb)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(181 * 600000, intmmsi, "In Payload.signed_binary_int - Offered 181 but got not 181")
        # longitude
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(181.0, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for 181 did not return 181.0')
        # latitude
        # 91 degrees - indicates not available
        strnumber: str = "{:027b}".format(91 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(91.0, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for minus one did not return')

        # minus 180 degrees
        strnumber: str = "{:028b}".format(-180 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(-180 * 600000, intmmsi, "In Payload.signed_binary_int - Offered -180 but got not -180")
        # longitude
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(-180.0, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for -180 did not return -180.0')
        # latitude
        # 91 degrees - indicates not available
        strnumber: str = "{:027b}".format(91 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(91.0, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for -90 degrees did not return -90.0')

        # test for a non zero decimal degrees
        # longitude
        strnumber: str = "{:028b}".format(-45 * 600000 + 300000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.payload = fakestream
        mypayload.get_longitude(8, 28)
        self.assertEqual(-44.5, mypayload.longitude, "In Payload testing signed int, longitude\n" +
                         'Entered for -44.5 did not return -44.5')
        # latitude
        # 31.1 - indicates not available
        strnumber: str = "{:027b}".format(31 * 600000 + 60000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        mypayload.get_latitude(8, 27)
        self.assertEqual(31.1, mypayload.latitude, "In Payload testing signed int, latitude\n" +
                         'Entered for 31.1 degrees did not return 31.1')

        # for i in range(100):
        #     fakestream: str = '00010000'
        #     faketail: str = '000000000000000000000000000000'
        #
        #     #testnumber: int = random.randint(0, 999999999)
        #     strnumber: str = "{:030b}".format(testnumber)
        #     fakestream = fakestream + strnumber + faketail
        #     mypayload.payload = fakestream
        #     intmmsi = mypayload.binary_item(8, 30)

    def test_get_raimflag(self):
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

        # some necessary preconfig
        diction, mystream = self.initialise()
        mypayload = Payloads.Payload(mystream.binary_payload)
        print('Testing get_RAIMflag')

        fakestream: str = '00010000'
        faketail: str = '000000000000000000000000000000'

        teststring = fakestream + '1' + faketail
        mypayload.payload = teststring
        mypayload.getRAIMflag(8)
        self.assertEqual(True, mypayload.raim_flag, "In Payload.RAIMflag looking for True got other")

        teststring = fakestream + '0' + faketail
        mypayload.payload = teststring
        mypayload.getRAIMflag(8)
        self.assertEqual(False, mypayload.raim_flag, "In Payload.RAIMflag looking for False got other")

        mypayload.payload = teststring

    def test_get_fix(self):
        '''
        The position accuracy flag indicates the accuracy of the fix.
        A value of 1 indicates a DGPS-quality fix with an accuracy of < 10ms.
        0, the default, indicates an unaugmented GNSS fix with accuracy > 10m.

        :return:
        sets payload.fixquality
        '''

        # some necessary preconfig
        diction, mystream = self.initialise()
        mypayload = Payloads.Payload(mystream.binary_payload)
        print('Testing get_fixquality')

        fakestream: str = '00010000'
        faketail: str = '000000000000000000000000000000'

        teststring = fakestream + '1' + faketail
        mypayload.payload = teststring
        mypayload.getfix(8)
        self.assertEqual(True, mypayload.fix_quality, "In Payload.fixquality looking for True got other")

        teststring = fakestream + '0' + faketail
        mypayload.payload = teststring
        mypayload.getfix(8)
        self.assertEqual(False, mypayload.fix_quality, "In Payload.fixquality looking for False got other")

        mypayload.payload = teststring


class TestCNB(TestCase):

    def initialise(self):

        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        mystream = Payloads.AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05')
        # mystream = Payloads.AISStream('!AIVDM,1,1,,B,177Q0U0wBO:`jk5apbs2q2@>00SG,0*1F')
        mycnb = Payloads.CNB(mystream.binary_payload)
        return diction, mystream, mycnb

    def make_stream(self, preamlen: int, testbits: str):
        # creates a fake binary payload to allow testing
        # preamble is number number of bits needed to fill up to beginning of testbits
        # testbits is the binary stream representing the area of thge domain under test
        # a couple of 'constants'
        fakehead: str = '00010000'
        faketail: str = '000000000000000000000000000000'
        # prefill the preamble with message type 4
        preamble: str = fakehead
        # fillcount is number of required prefill with allowance for the 8 bit header
        fillcount = preamlen - 8

        while fillcount > 0:
            preamble = preamble + '1'
            fillcount -= 1

        # print('in make_stream nr bits needed, nr bits offered', preamlen, len(preamble))
        return preamble + testbits + faketail

    def test_get_nav_status(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_nav_status")

        for i in range(0, 15):
            testbits = '{:04b}'.format(i)

            diction.make_stream(38, testbits)
            mycnb.payload = diction.make_stream(38, testbits)

            mycnb.get_nav_status()
            self.assertEqual(i, mycnb.navigation_status, "In CNB.get_nav_status - value expected not returned")

    def test_get_rot(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_ROT")

        # int(round(4.733 * math.sqrt(708), 0)) gives 126
        # valid entries are -127 to 128
        fvalue: float = 0.0
        for fvalue in [0, 1.0, -1.0, 90.0, -90.0, 708.0, -708.0]:
            if fvalue >= 0:
                testbits = '{:08b}'.format(int(round(4.733 * math.sqrt(fvalue), 0)))
            else:
                testbits = '{:08b}'.format(-int(round(4.733 * math.sqrt(abs(fvalue)), 0)))
            mycnb.payload = diction.make_stream(42, testbits)
            mycnb.get_ROT()
            self.assertTrue(fvalue - 1 <= mycnb.rate_of_turn <= fvalue + 1,
                            "In CNB.get_rot value returned does not match value set " + '{:f}'.format(fvalue))

        # special cases
        testbits = "{:08b}".format(127)
        mycnb.payload = diction.make_stream(42, testbits)
        mycnb.get_ROT()
        self.assertEqual(1005.0, mycnb.rate_of_turn,
                         "In CNB.get_rot value returned does not match value set " + '{:f}'.format(1005.0))
        testbits = "{:08b}".format(-127)
        mycnb.payload = diction.make_stream(42, testbits)
        mycnb.get_ROT()
        self.assertEqual(-1005.0, mycnb.rate_of_turn,
                         "In CNB.get_rot value returned does not match value set " + '{:f}'.format(-1005.0))
        testbits = "{:08b}".format(128)
        mycnb.payload = diction.make_stream(42, testbits)
        mycnb.get_ROT()
        self.assertEqual(1000.0, mycnb.rate_of_turn,
                         "In CNB.get_rot value returned does not match value set " + '{:f}'.format(1000))

    def test_get_sog(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_SOG")

        # initially check for values 0, 0.5 1,102

        for i in [0, 0.5, 1, 102, 102.2]:
            i = int(i * 10)
        testbits = '{:010b}'.format(i)
        mycnb.payload = diction.make_stream(50, testbits)

        mycnb.getSOG()
        self.assertEqual(float(i) / 10.0, mycnb.speed_over_ground,
                         "In getSOG value returned does not match value offered")

        for _ in range(100):
            i = random.randint(0, 1022)
            testbits = '{:010b}'.format(i)
            mycnb.payload = diction.make_stream(50, testbits)
            mycnb.getSOG()
            self.assertEqual(float(i) / 10.0, mycnb.speed_over_ground,
                             "In getSOG value returned does not match value offered")

    def test_get_cog(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_COG")

        # initially check for values 0, 0.5 1,359, 360 and value outside valid range
        for i in [0, 0.5, 1, 90, 359, 360, 361]:
            i = i * 10
        testbits = '{:012b}'.format(i)
        mycnb.payload = diction.make_stream(116, testbits)
        try:
            mycnb.get_COG()
            self.assertEqual(float(i) / 10.0, mycnb.course_over_ground,
                             "In get_COG value returned does not offered value " + '{:d}'.format(i))
        except ValueError:
            self.assertFalse(mycnb.valid_item, "In get_COG module did not detect invalid parameter")

            # and for completeness a random set of values
        for _ in range(100):
            i = random.randint(0, 3600)
            testbits = '{:012b}'.format(i)
            mycnb.payload = diction.make_stream(116, testbits)
            try:
                mycnb.get_COG()
                self.assertEqual(float(i) / 10.0, mycnb.course_over_ground,
                                 "In get_COG value returned does not offered value " + '{:d}'.format(i))
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In get_COG module did not detect invalid parameter")

    def test_get_tru_head(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_truhead")

        # initially check for values 0, 1,359, 360 and value outside valid range

        for i in [0, 1, 90, 359, 511, 360]:

            testbits = '{:09b}'.format(i)
            mycnb.payload = diction.make_stream(128, testbits)
            try:
                mycnb.get_tru_head()
                self.assertEqual(i, mycnb.true_heading,
                                 "In get_tru_head value returned does not match value offered")
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In get_tru_head module did not detect invalid parameter")

        # and again a random selection
        for _ in range(100):
            i = random.randint(0, 3600)
            testbits = '{:09b}'.format(i)
            mycnb.payload = diction.make_stream(128, testbits)
            try:
                mycnb.get_tru_head()
                self.assertEqual(i, mycnb.true_heading,
                                 "In get_COG value returned does not match value offered")
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In CNB.get_tri_hed invalid value not flagged")

    def test_get_pos_accuracy(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_pos_accuracy")
        mycnb = Payloads.CNB(mystream.binary_payload)

        teststring = diction.make_stream(60, '1')
        mycnb.payload = teststring
        mycnb.get_pos_accuracy()
        self.assertEqual(True, mycnb.position_accuracy,
                         "In CNB.get_pos_accuracy looking for True got other")

        teststring = diction.make_stream(60, '0')
        mycnb.payload = teststring
        mycnb.get_pos_accuracy()
        self.assertEqual(False, mycnb.position_accuracy,
                         "In CNB.get_pos_accuracy looking for False got other")

    def test_get_timestamp(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_timestamp")
        # valid entries are 0-63, by virtue of only 6 bits cannot go outside range

        for i in [0, 1, 30, 59, 60, 61, 62, 63]:
            testbits = '{:06b}'.format(i)
            mycnb.payload = diction.make_stream(137, testbits)
            mycnb.get_timestamp()
            self.assertEqual(i, mycnb.time_stamp,
                             "In get_timestamp value returned does not match value offered" + '{:d}'.format(i))

    def test_get_man_indic(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_man_indic")
        # valid entries are 0-2 but can have an invalid 3 appear

        for i in [0, 1, 2, 3]:
            testbits = '{:02b}'.format(i)
            mycnb.payload = diction.make_stream(143, testbits)
            try:
                mycnb.get_man_indic()
                self.assertEqual(i, mycnb.maneouver_indicator,
                                 "In get_man_indic value returned does not offered value " + '{:d}'.format(i))
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In get_man_indic module did not detect invalid parameter")

    def test_repr(self):
        diction, mystream, mycnb = self.initialise()
        print('Testing CNB __repr__')

        print(mycnb)


class TestBasestation(TestCase):

    def initialise(self):

        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream = Payloads.AISStream(psuedo_AIS)
        mybase = Payloads.Basestation(mystream.binary_payload)
        return diction, mystream, mybase

    def test_get_year(self):
        print('Testing Base.get_year')
        # Bits 38-51  length 14  Year (UTC)  year  UTC, 1-9999, 0 = N/A (default)
        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 9999, 1, 2023, 11000]:
            mybase.payload = diction.make_stream(38, '{:014b}'.format(yval))
            try:
                mybase.get_year()
                self.assertEqual(yval, mybase.year, "In Base.get_year - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_year - module does not flag invalid value")

    def test_get_month(self):
        print('Testing Base.get_month')
        # Bits 52-55 length 4  Month (UTC) month  1-12; 0 = N/A (default)
        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 12, 1, 13]:
            mybase.payload = diction.make_stream(52, '{:04b}'.format(yval))
            try:
                mybase.get_month()
                self.assertEqual(yval, mybase.month, "In Base.get_month - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_month - module does not flag invalid value")

    def test_get_day(self):
        print('Testing Base.get_day')
        # Bits 56-60  length 5  Day (UTC) day  1-31; 0 = N/A (default)
        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 31, 1]:
            mybase.payload = diction.make_stream(56, '{:05b}'.format(yval))
            # put in dummy year 2023, dummy month 1
            dyear = '{:014b}'.format(2023)
            dmonth = '{:04b}'.format(1)
            mybase.payload = mybase.payload[0:38] + dyear + dmonth + mybase.payload[56:]
            try:
                mybase.get_day()
                self.assertEqual(yval, mybase.day, "In Base.get_day - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_day - module does not flag invalid value")

        # now setup some weird invalid conditions
        leap = '{:014b}'.format(2004)
        month = '{:04b}'.format(2)
        day = '{:05b}'.format(30)
        leap_year_stream = mybase.payload[0:38] + leap + month + day + mybase.payload[78:]
        mybase.payload = leap_year_stream
        try:
            mybase.get_day()
            self.fail("In Base.day - module does not flag invalid day for leap_year")
        except ValueError:
            self.assertFalse(mybase.valid_item,
                             "In Base.day - module does not flag invalid day for leap_year")

        nonleap = '{:014b}'.format(2003)
        month = '{:04b}'.format(2)
        day = '{:05b}'.format(29)
        nonleap_year_stream = mybase.payload[0:38] + nonleap + month + day + mybase.payload[78:]
        mybase.payload = leap_year_stream
        mybase.payload = nonleap_year_stream
        try:
            mybase.get_day()
            self.fail("In Base.day - module does not flag invalid day for nonleap_year")
        except ValueError:
            self.assertFalse(mybase.valid_item,
                             "In Base.day - module does not flag invalid day for nonleap_year")

        for imonth in [4, 6, 9, 11]:
            nonleap = '{:014b}'.format(2003)
            month = '{:04b}'.format(imonth)
            day = '{:05b}'.format(31)
            mybase.payload = diction.make_stream(56, '{:05b}'.format(31))
            nonleap_year_stream = mybase.payload[0:38] + nonleap + month + day + mybase.payload[78:]
            mybase.payload = nonleap_year_stream
            try:
                mybase.get_day()
                self.fail("In Base.day - module does not flag invalid day for 30 day months")
            except ValueError:
                self.assertFalse(mybase.valid_item,
                                 "In Base.day - module does not flag invalid day for 30 day months")

    def test_get_hour(self):
        print('Testing Base.get_hour')
        # Bits 61-65 length 5  Hour (UTC) hour  0-23; 24 = N/A (default)

        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 23, 1, 24, 25]:
            mybase.payload = diction.make_stream(61, '{:05b}'.format(yval))
            try:
                mybase.get_hour()
                self.assertEqual(yval, mybase.hour, "In Base.get_hour - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_hour - module does not flag invalid value")

    def test_get_minute(self):
        print('Testing Base.get_minute')
        # Bits 66-71 length 6  Minute (UTC) minute  0-59; 60 = N/A (default)
        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 59, 60, 61]:
            mybase.payload = diction.make_stream(66, '{:06b}'.format(yval))
            try:
                mybase.get_minute()
                self.assertEqual(yval, mybase.minute, "In Base.get_minute - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_minute - module does not flag invalid value")

    def test_get_second(self):
        print('Testing Base.get_second')
        # Bits 72-77 length 6  Second (UTC) second  0-59; 60 = N/A (default)
        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 59, 60, 61]:
            mybase.payload = diction.make_stream(72, '{:06b}'.format(yval))
            try:
                mybase.get_second()
                self.assertEqual(yval, mybase.second, "In Base.get_second - value returned does match value set")
            except ValueError:
                self.assertFalse(mybase.valid_item, "In Base.get_second - module does not flag invalid value")

    def test_get_epfd(self):
        print('Testing Base.get_EPFD')
        # Bits 134-137  length 4  Type of EPFD epfd  See "EPFD Fix Types" in Dictionary
        # valid 0-8 15 not uncommen, values 9-14 returned as 0 and object still validated

        diction, mystream, mybase = self.initialise()
        # first check for edge conditions, some normal values and a non=-valid
        for yval in [0, 8, 1, 15, 10]:
            mybase.payload = diction.make_stream(134, '{:04b}'.format(yval))
            try:
                mybase.get_EPFD()
                if 0 <= yval <= 8 or yval == 15:
                    self.assertEqual(yval, mybase.EPFD_type,
                                     "In Base.get_EPFD - value returned does match value set")
                else:
                    yval = 0
                    self.assertEqual(yval, mybase.EPFD_type,
                                     "In Base.get_EPFD - value returned does match default substitution 9-14")
            except:
                self.assertFalse(mybase.valid_item,
                                 "In Base.get_EPFD - somethings very wrong should not get here")

    def test_rerr(self):
        diction, mystream, mybase = self.initialise()
        print("testing  Base __repr__")

        print(mybase)


class TestAISStream(TestCase):
    mytestdata = [
        '!AIVDM,1,1,,A,404,0*05',
        '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05',
        '!AIVDM,2,1,7,A,57Oi`:021ssqHiL6221L4l8U8V2222222222220l1@F476Ik0;QA1C`88888,0*1E',
        '!AIVDM,2,2,7,A,88888888888,2*2B',
        '!AIVDM,1,1,,A,404k0WivNUSSNbKvjEag;4W00HB@,0*34',
        '!AIVDM,1,1,,B,177Q0U04BL:`kKQapd7RpB@v0HBB,0*6D',
        '!AIVDM,1,1,,A,15Rl8D002I:irnQc>`@hg0Vr08BL,0*65',
        '!AIVDM,1,1,,B,13loh<01Qm:jL<wcUG5p3nQ004J<,0*60',
        '!AIVDM,1,1,,B,404kS@P000Htt<tSF0l4Q@100pBr,0*10',
        '!AIVDM,1,1,,B,17Oosc0q2K:NrnOaf@Mobww200SB,0*28',
        '!AIVDM,1,1,,A,19NS6o002U:`fMQaqINBiBC20HCp,0*69'
    ]

    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid
        mystream = Payloads.AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05')
        return diction, mystream

    def test_split_string(self):
        diction, mystream = self.initialise()
        # this one should pass since input stream for the initialise is valid
        self.assertTrue(mystream.valid_message, "Failed in AISStream.split_stream")

        # now start testing the split varying parameters
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'

        mystream.split_string(teststream)
        self.assertEqual('!AIVDM', mystream.packet_id,
                         'In AISStreamn.split_string packet_id not correect')
        self.assertTrue(mystream.valid_message,
                        'In AISStream.split_string invalid status returned for valid packet_id')
        teststream = '!AIVDO,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertEqual('!AIVDO', mystream.packet_id,
                         'In AISStreamn.split_string packet_id not correect')
        self.assertTrue(mystream.valid_message,
                        'In AISStream.split_string invalid status returned for valid packet_id')
        teststream = '!AIVDX,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertFalse(mystream.valid_message,
                         'In AISStream.split_string invalid status returned for invalid packet_id')

        # next fragment count
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertEqual(1, mystream.fragment_count,
                         'In AISStreamn.split_string fragment_count not correect')
        self.assertTrue(mystream.valid_message,
                        'In AISStream.split_string invalid status returned for valid fragment_count')
        teststream = '!AIVDM,A,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertFalse(mystream.valid_message,
                         'In AISStream.split_string invalid status returned for valid fragment_count')

        # now fragment_number
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertEqual(1, mystream.fragment_number,
                         'In AISStreamn.split_string fragment_count not correect')
        self.assertTrue(mystream.valid_message,
                        'In AISStream.split_string invalid status returned for valid fragment_count')
        teststream = '!AIVDM,1,B,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertFalse(mystream.valid_message,
                         'In AISStream.split_string invalid status returned for valid fragment_count')
        # now fragment_number
        # null message_id
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertEqual(0, mystream.message_id,
                         'In AISStreamn.split_string message id not null as expected')
        # non_null message_id
        teststream = '!AIVDM,1,1,3,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertEqual(3, mystream.message_id,
                         'In AISStreamn.split_string fragment_count not correect')
        self.assertTrue(mystream.valid_message,
                        'In AISStream.split_string invalid status returned for valid fragment_count')
        # non_null message_id alphabetic
        teststream = '!AIVDM,1,1,C,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        self.assertFalse(mystream.valid_message,
                         'In AISStream.split_string invalid status returned for valid fragment_count')

        # now the channel
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream.split_string(teststream)
        for tchann in ['A', 'B', '1', '2', 'D', '3']:
            teststream = '!AIVDM,1,1,,' + tchann + ',404kS@P000Htt<tSF0l4Q@100pAg,0*05'
            mystream.split_string(teststream)
            if tchann not in ['D', '3']:
                self.assertEqual(tchann, mystream.channel,
                                 'In AISStreamn.split_string channel not correect')
                self.assertTrue(mystream.valid_message,
                                'In AISStream.split_string invalid status returned for valid channel')
            else:
                self.assertFalse(mystream.valid_message,
                                 'In AISStream.split_string invalid status returned for invalid channel')

        # now message type
        teststream = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'

        for i in range(1, 28):
            tmess = bytearray.fromhex('{:X}'.format(i + 0x30)).decode()
            teststream = '!AIVDM,1,1,,A,' + tmess + '04Sk@P000Htt<tSF0l4Q@100pAg,0*05'
            mystream.split_string(teststream)
            if i < 28:
                self.assertEqual(i, mystream.message_type,
                                 'In AISStreamn.split_string message_type not correct')
                self.assertTrue(mystream.valid_message,
                                'In AISStream.split_string invalid status returned for messager type')
            else:
                self.assertFalse(mystream.valid_message,
                                 'In AISStream.split_string invalid status returned for invalid message type')

    def test_create_binary_payload(self):
        dict, mystream = self.initialise()
        print('Testing create_binary_payload')
        for i in range(len(self.mytestdata) - 1):
            self.testpay: str = ''
            mystream.payload = self.mytestdata[i].split(',')[5]
            mystream.create_binary_payload()

            for char in mystream.payload:
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, char)

            # outstring = mydata.ExtractString(0, self.binlen+6)
            # print('outstring ', outstring)
            # print('instring  ', payload[5])
            #
            # if len(self.binpay) != len(self.testpay):
            #     print("lengths differ", len(self.binpay), len(self.testpay))
            #
            # for ii in range(len(self.testpay) -1):
            #     if self.testpay[ii] != self.binpay[ii]:
            #         print('differ at ', ii, "in string of length ", len(self.testpay),
            #               len(self.binpay), self.binlen, self.testpay[ii], self.binpay[ii])

            self.assertEqual(self.testpay, mystream.binary_payload, "Create binary payload failure")

    def test_create_bytearray_payload(self):
        dict, mystream = self.initialise()
        binpay: bytearray
        print('Testing create_bytearray_payload')
        for i in range(5):
            self.testpay: str = ''
            payload = self.mytestdata[i].split(',')[5]
            mystream.create_bytearray_payload()
            self.ostring = ''
            for i in range(len(mystream.byte_payload)):
                self.ostring = self.ostring + "{:08b}".format(mystream.byte_payload[i])

            testpay = mystream.payload
            for ij in range(len(mystream.payload)):
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, mystream.payload[ij])

            # the create bytearray by default pads with 0's to byte boundary.
            # to match the expected string needs to be padded as well
            while len(self.testpay) % 24 != 0:
                self.testpay = self.testpay + "0"

            self.assertEqual(self.testpay, self.ostring, "Create bytearray payload failure")

    def test_m_to_int(self):
        '''
        m_to_int takes an encoded (armoyed) string and returns an integer
        :return:
        '''
        print("Testing m_to_int")
        dict, mystream = self.initialise()

        for _ in range(20):
            # create a random length integer
            testlength: int = random.randint(1, 10)
            testnumb: int = random.randint(0, 9999999999)
            numstring: str = "{:010d}".format(testnumb)
            # extract required length string from the 10 character string
            numbstring = numstring[10 - testlength:]
            # #make encoded string using dictionary
            for ij in range(len(numbstring)):
                outint = mystream.m_to_int(numbstring[ij])
                self.assertEqual(int(numbstring[ij]), outint, "Failure in m_to_int")


class TestStaticData(TestCase):

    def initialise(self):

        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,2,1,5,A,577Q0U82<A0II9ACR20pT<th4V0l4E9<f222221?Bhh??6`A0EAR`4mE`88888888888880,0*3E'
        mystream = Payloads.AISStream(psuedo_AIS)
        mystatic = Payloads.StaticData(mystream.binary_payload)
        return diction, mystream, mystatic

    def make_stream(self, preamlen: int, testbits: str):
        # creates a fake binary payload to allow testing
        # preamble is number number of bits needed to fill up to beginning of testbits
        # testbits is the binary stream representing the area of thge domain under test
        # a couple of 'constants'
        fakehead: str = '00010000'
        faketail: str = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        # prefill the preamble with message type 4
        preamble: str = fakehead
        # fillcount is number of required prefill with allowance for the 8 bit header
        fillcount = preamlen - 8

        while fillcount > 0:
            preamble = preamble + '1'
            fillcount -= 1

        # print('in make_stream nr bits needed, nr bits offered', preamlen, len(preamble))
        return preamble + testbits + faketail

    def make_binary_stream(self, prteamleng: int, testval: int, bitcount: int):
        # returns a string of binary payload
        # incorporating a string of bit count length equivalent to integer value value presented
        #
        intstring: str = '{:0' + '{:d}'.format(bitcount) + 'b'.format(testval)
        return self.make_stream(preamlen=prteamleng, testbits=intstring)

    def test_get_ais_version(self):
        # given current specification little can be tested here
        # valid value is 0 per [ITU1371] but allow for 1-3 from future editions
        diction, mystream, mystatic = self.initialise()
        print("Testing Statc.get_ais_version")

        teststream = self.make_binary_stream(38, 0, 2)
        mystatic.payload = teststream
        try:
            self.assertEqual(0, mystatic.ais_version, "In Static.get_ais_version - value returned not equal 0")
        except RuntimeError:
            self.assertFalse(True, "Runtime Error in Static.get_ais_version")

    def test_get_imo_number(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_imo_number")

        # little can be tested here its only a 7 digit identifier and effectively free text
        # 30 bit field can returm greater than 7 digits check for this

        for i in [0, 11, 123, 1234, 12345, 123456, 1234567, 9999999, 12345678]:
            testbits = self.make_binary_stream(40, i, 30)
            mystatic.payload = testbits
            try:
                mystatic.get_imo_number()
                self.assertEqual(i, mystatic.imo_number,
                                 "In Static.get_imo_number value returned " + mystatic.imo_number +
                                 ' does not match value offered {:d}'.format(i))
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Static.get_imo_number")
            except ValueError:
                self.assertFalse(mystatic.valid_item, "In Static.get_imo_number invalid > 9999999' + "
                                                      " found and not flagged")

    def test_get_callsign(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_callsign")

        # again effectively free text

        for a in ['VH12345', 'ABVCDEF']:
            test_bits = ''
            # for x in a:
            #     test_bits = test_bits + diction.char_to_binary(x)
            #     print (x, test_bits)
            test_bits = diction.char_to_binary(a)
            test_bits = diction.make_stream(70, test_bits)
            mystatic.payload = test_bits
            try:
                mystatic.get_callsign()
                self.assertEqual(a, mystatic.callsign, "In Static.get_callsign, value returned "
                                 + mystatic.callsign + " not equal to value offered " + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Static.get_callsign")

    def test_get_vessel_name(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_vessel_name")

        # again effectively free text 20 char max

        try:
            mystatic.get_vessel_name()
        except RuntimeError:
            self.assertFalse(True, "Runtime Error in Static.get_vessel_name")

        for a in ['Spirit of Paynesvill',
                  'Australian Explorer',
                  '123456789012345678901234567890',
                  'ABCDEFGHIJKLMNOPQRSTUV',
                  'abcdefghijklmnopqrstuv'
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper())
            test_bits = diction.make_stream(112, test_bits)
            mystatic.payload = test_bits
            try:
                mystatic.get_vessel_name()
                self.assertEqual(a.upper()[0:20], mystatic.vessel_name, "In Static.get_destination, value returned "
                                 + mystatic.vessel_name + " not equal to value offered " + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Static.get_vessel_name")

    def test_get_ship_type(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_ship_type")

        # little can be checked here rubbish values are converted to 0
        # range is 0-99 as per AISDictionaries.Ship_Type dictionary
        # bits 232-239, 8 bits
        # can be rubbish field so errors cause type to be set to default 0, (Not Available)

        for i in [0, 1, 3, 7, 13, 99, 100]:

            testbits = '{:08b}'.format(i)
            mystatic.payload = self.make_stream(232, testbits)

            try:
                mystatic.get_ship_type()
                print('ín test ship type =', mystatic.ship_type, testbits)
                if i <= 99:
                    self.assertEqual(i, mystatic.ship_type, "In Static.get+_ship_type incorrect value retrieved")
                else:
                    self.assertEqual(0, mystatic.ship_type, "In Static.get+_ship_type incorrect value retrieved")
            except ValueError:
                self.assertFalse(mystatic.valid_item, "In Static.get_ship_type invalid type not flagged")

    def test_get_dim_to_bow(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 9 bits therefore range 0-511

        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_dom_to_bow")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            mystatic.payload = self.make_stream(240, testbits)

            try:
                mystatic.get_dim_to_bow()
                if i <= 511:
                    self.assertEqual(i, mystatic.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
                else:
                    self.assertEqual(511, mystatic.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
            except RuntimeError:
                logging.error("Runtime error in Static.dim_to_bow")

    def test_get_dim_to_stern(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_dim_to_stern")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            mystatic.payload = self.make_stream(249, testbits)

            try:
                mystatic.get_dim_to_stern()
                if i <= 511:
                    self.assertEqual(i, mystatic.dim_to_stern,
                                     "In Static.get_dim_to_stern value reurned incorrect")
                else:
                    self.assertEqual(511, mystatic.dim_to_stern,
                                     "In Static.get_dim_to_stern value reurned incorrect")
            except RuntimeError:
                logging.error("Runtime error in Static.dim_to_stern")

    def test_get_dim_to_port(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 6 bits range 0-63

        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_dim_to_port")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            mystatic.payload = self.make_stream(258, testbits)

            try:
                mystatic.get_dim_to_port()
                if i <= 511:
                    self.assertEqual(i, mystatic.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
                else:
                    self.assertEqual(511, mystatic.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
            except RuntimeError:
                logging.error("Runtime error in Static.dim_to_port")

    def test_get_dim_to_stbd(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_dim_to_stbd")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            mystatic.payload = self.make_stream(264, testbits)

        try:
            mystatic.get_dim_to_stbd()
            if i <= 511:
                self.assertEqual(i, mystatic.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
            else:
                self.assertEqual(511, mystatic.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
        except RuntimeError:
                logging.error("Runtime error in Static.dim_to_stbd")

    def test_get_eta_month(self):
        #
        # 4 bits range 0-15, at position 274
        # flsag error on 13-15, set to 0 (N/A) but dont invalidate
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_eta_month")

        for i in [0, 1, 2, 5, 11, 12, 13]:
            testbits = '{:04b}'.format(i)
            mystatic.payload = self.make_stream(274, testbits)

            try:
                mystatic.get_eta_month()
            except RuntimeError:
                logging.error("Runtime error in Static.get_eta_month")

            if i <= 12:
                self.assertEqual(i, mystatic.eta_month,
                                 "In Static.get_eta_month incorrect value returned")
            else:
                self.assertEqual(0, mystatic.eta_month,
                                 "In Static.get_eta_month incorrect value returned")





    def test_get_eta_day(self):
        # bits 278-282, 5 bits range 0-31, 0 == default == N/A
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_eta_day")
        for i in [0, 1, 2, 5, 11, 12, 13, 28, 29, 30,31]:
            testbits = '{:05b}'.format(i)
            mystatic.payload = self.make_stream(278, testbits)

            try:
                mystatic.get_eta_day()
            except RuntimeError:
                logging.error("Runtime error in Static.get_eta_day")

            self.assertEqual(i, mystatic.eta_day,
                                 "In Static.get_eta_day incorrect value returned")


    def test_get_eta_hour(self):
        # bits 283-287, 5 bits range 0-31, set to 24 (N/A) if outside range 0-23
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_eta_hour")
        for i in [0, 1, 2, 5, 11, 12, 13, 23, 24,28]:
            testbits = '{:05b}'.format(i)
            mystatic.payload = self.make_stream(283, testbits)

            try:
                mystatic.get_eta_hour()
            except RuntimeError:
                logging.error("Runtime error in Static.get_eta_hour")
            except ValueError:
                mystatic.eta_hour = 24

            if i <= 23:
                self.assertEqual(i, mystatic.eta_hour,
                             "In Static.get_eta_hour incorrect value returned")
            else:
                self.assertEqual(24, mystatic.eta_hour,
                                 "In Static.get_eta_hour incorrect value returned")


    def test_get_eta_minute(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_eta_minute")
        for i in [0, 1, 2, 5, 11, 12, 59, 60, 62]:
            testbits = '{:06b}'.format(i)
            mystatic.payload = self.make_stream(288, testbits)

            try:
                mystatic.get_eta_minute()
            except RuntimeError:
                logging.error("Runtime error in Static.get_eta_minute")
            except ValueError:
                # outside range 0-59 but dont invalidate
                mystatic.eta_minute = 60

            if mystatic.eta_minute <= 59:
                self.assertEqual(i,  mystatic.eta_minute,
                                 "In Static.get_eta_minute incorrect value returned")
            else:
                self.assertEqual(60, mystatic.eta_minute,
                                 "In Static.get_eta_minute incorrect value returned")


    def test_get_draught(self):
        # bits 294-301, 8 bits range 0-255 theerefore draught 0-25.5
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_draught")

        for i in [0, 1, 2, 5, 10, 20, 50, 100, 200, 255]:
            testbits = '{:08b}'.format(i)
            mystatic.payload = self.make_stream(294, testbits)

            try:
                mystatic.get_draught()
            except RuntimeError:
                logging.error("Runtime error in Static.get_draught")

            self.assertEqual(round(float(i)/10.0, 1), mystatic.draught,
                                 "In Static.get_draughte incorrect value returned")
    def test_get_destination(self):
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_destination")

        # again effectively free text - only upper case allowed

        for a in ['Melbourne',
                  'Australian Explorer',
                  '12345678901234567890',
                  'ABCDEFGHIJKLMNOPQRST',
                  'abcdefghijklmnopqrst',
                  '12345678901234567890'
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper())
            test_bits = diction.make_stream(302, test_bits)
            mystatic.payload = test_bits
            try:
                mystatic.get_destination()
                self.assertEqual(a.upper(), mystatic.destination, "In Static.get_destination, value returned "
                                 + mystatic.destination + " not equal to value offered " + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Static.get_destination")

    def test_repr(self):
        diction, mystream, mystatic = self.initialise()
        print("testing Static __repr__")
        print(mystatic)
        # should have a valid data set as a result of the initiaslise()



if __name__ == "main":
    pass
