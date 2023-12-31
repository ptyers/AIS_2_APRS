from unittest import TestCase
from AISDictionary import AISDictionaries
import Payloads
import random
import logging
import math
from GlobalDefinitions import Global


class TestBinary_addressed_message(TestCase):
    pass


class TestBinary_acknowledge(TestCase):
    pass


class TestBinary_broadcast_message(TestCase):
    pass


class TestUTC_date_enquiry(TestCase):
    pass


class TestUTC_date_response(TestCase):
    pass


class TestSafety_related_acknowledgement(TestCase):
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


class TestSingle_slot_binary_message(TestCase):
    pass


class TestMultiple_slot_binary_message(TestCase):
    pass


class TestFragments(TestCase):

    def test_put_frag_in_dict(self):
        # __init__(self, binary_payload: str, fragment_count: int, fragment_number: int, message_id: int):
        # we need to define at least two fragments
        # the first with frag count = 2, frag_number = 1, message_id = 0
        # thge second with frag_count = 2, frag_number = 2, message_id= 0
        # and try and put both of these in dictionary
        # print('**********************************************************************************************')
        # print("entering test put frag in dict")
        # print('8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888')

        fragcnt = random.randint(1, 4)
        messid = []
        message_memory = []
        # produce a list of tuples (message_id, Number of Fragments)
        # create random number of fragments with varied message ids and varied number of fragments
        # if you can put them into the Fragdict and then recover them to match with a local fragment memory
        # we have success

        for i in range(0, 10):
            messid.append((random.randint(0, 999), random.randint(1, 4)))

        # print(messid)
        current = 0
        maxno = 10
        for j in range(0, maxno):
            # print(messid[j])
            current += 1

            for k in range(0, maxno):
                if messid[k][1] > j:
                    # create a random payload
                    payload = '{:20b}'.format(random.randint(0, 999999))
                    message_memory.append((messid[k][0], current, payload))
                    # print(messid[k][0], current, payload)
                    m = Payloads.Fragments(payload, messid[k][1], current, messid[k][0])
                    m.put_frag_in_dict()

        for data in message_memory:
            # print(data[0], data[1], data[2], Global.FragDict[str(data[0]) + ',' + str(data[1])][2])
            self.assertEqual(data[2], Payloads.Fragments.FragDict[str(data[0]) + ',' + str(data[1])][2], "Failed")

    def test_match_fragments(self):

        # first a simple test - produce two fragments with same message id, fragment counts 1 and 2
        # possibly extend to three fragments once proven with two
        print("Testing match fragments")

        fragements = [(3, 1, '000000111111000000111111000000'),
                      (3, 2, '111111000000111111000000111111'),
                      (3, 3, '1011010101000000111111000000111111')]
        expected = fragements[0][2] + fragements[1][2] + fragements[2][2]

        m = Payloads.Fragments(fragements[0][2], 3, 1, 4)
        m.put_frag_in_dict(False)
        m = Payloads.Fragments(fragements[1][2], 3, 2, 4)
        m.put_frag_in_dict(False)
        m = Payloads.Fragments(fragements[2][2], 3, 3, 4)
        m.put_frag_in_dict(False)

        # now try merging - this normally would come out of put_frag_in_dict but for testing will do it seperately
        # there is little validation done in the fragments object

        success, newpayload = m.match_fragments('4,3')
        # print('After merge ', success)
        if success:
            # print(expected)
            # print(newpayload)
            self.assertEqual(expected, newpayload,
                             'Failed in matching fragments test sequence does not match sequence retrurned')

        # set of fragments produced in testing put_frag_in_dict as test data
        messid = []
        message_memory = []
        for i in range(0, 10):
            messid.append((random.randint(0, 999), random.randint(1, 4)))

        # print(messid)
        current = 0
        maxno = 10
        for j in range(0, maxno):
            # print(messid[j])
            current += 1

            for k in range(0, maxno):
                if messid[k][1] > j:
                    # create a random payload
                    payload = '{:20b}'.format(random.randint(0, 999999))
                    message_memory.append((messid[k][0], current, payload))
                    # print(messid[k][0], current, payload)
                    m = Payloads.Fragments(payload, messid[k][1], current, messid[k][0])
                    m.put_frag_in_dict(False)  # dont attempt to invoke match_fragments as would be normal
        # print(Global.FragDict)
        # now take message_id from list messid and see if we can do matches
        # yje list of tuples in message memory contains the message_id, the number of fragments and the portions of
        # "fragmented"payload. Now work down the list presenting message id ,  when success flag is returned TRUE
        # aggregate the fragmented payloads tresented and compare to the aggregate payload returned
        #

        for m_id, fc in messid:
            # collect the presented payloads on a per message_id basis

            expected = ''
            for mm_id, fn, pload in message_memory:
                if m_id == mm_id:
                    expected = expected + pload

            # now have an expected payload to compare
            # call match_fragements with a key ['m_id,fc']
            key = str(m_id) + ',' + str(fc)
            # print('calling match frags key = ', key)
            success, newpayload = m.match_fragments(key)
            # print('returned {}\n{}\n{}'.format(success,expected, newpayload))
            if success:
                self.assertEqual(expected, newpayload,
                                 "Failed in random fragment matching\n {} \n {}vs".format(expected, newpayload))
            else:
                print("Failed matching fragments for {}\n ".format(m_id))


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

            logging.debug("DEBUG binary_payload from which string will be extracted\n{}"
            .format(mystream.binary_payload))
            outstr = mypayload.extract_string(rndstrt * 6 + 8, rndlen * 6)
            logging.debug('Extracted string {}'.format( outstr))

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

    def test_signd_bin_lat_long(self):
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

            mycnb.get_CNB_nav_status()
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

        mycnb.getCNB_SOG()
        self.assertEqual(float(i) / 10.0, mycnb.speed_over_ground,
                         "In getSOG value returned does not match value offered")

        for _ in range(100):
            i = random.randint(0, 1022)
            testbits = '{:010b}'.format(i)
            mycnb.payload = diction.make_stream(50, testbits)
            mycnb.getCNB_SOG()
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
            mycnb.getCNB_COG()
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
                mycnb.getCNB_COG()
                self.assertEqual(float(i) / 10.0, mycnb.course_over_ground,
                                 "In get_COG value returned does not offered value " + '{:d}'.format(i))
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In get_COG module did not detect invalid parameter")

    def test_get_CNBtru_head(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_truhead")

        # initially check for values 0, 1,359, 360 and value outside valid range

        for i in [0, 1, 90, 259, 359, 511, 360]:

            testbits = '{:09b}'.format(i)
            mycnb.payload = diction.make_stream(128, testbits)
            try:
                mycnb.getCNB_tru_head()
                self.assertEqual(i, mycnb.true_heading,
                                 "In get_CNBtru_head value returned does not match value offered")
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In get_CNBtru_head module did not detect invalid parameter")

        # and again a random selection
        for _ in range(100):
            i = random.randint(0, 360)
            testbits = '{:09b}'.format(i)
            mycnb.payload = diction.make_stream(128, testbits)
            try:
                mycnb.getCNB_tru_head()
                self.assertEqual(i, mycnb.true_heading,
                                 "In get_COG value returned does not match value offered")
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In CNB.get_tru_hed invalid value not flagged")

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
            mycnb.getCNB_timestamp()
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
                mybase.get_second(72)
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
                mybase.get_Base_EPFD()
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

    def test_repr(self):
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
        formatter = "'{:0" + '{:d}'.format(bitcount) + "b}'"
        intstring: str = formatter.format(testval)
        return self.make_stream(preamlen=prteamleng, testbits=intstring.strip("'"))

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

        for i in [0, 11, 123, 1234, 12345, 123456, 1234567, 9999999, 10000000]:
            testbits = self.make_binary_stream(40, i, 30)
            mystatic.payload = testbits
            try:
                mystatic.get_imo_number()
                self.assertEqual('{:07d}'.format(i), mystatic.imo_number,
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
            mystatic.get_Static_vessel_name()
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
                mystatic.get_Static_vessel_name()
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
                mystatic.get_Static_ship_type()
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
                mystatic.get_Static_dim_to_bow()
                if i <= 511:
                    self.assertEqual(i, mystatic.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
                else:
                    self.assertEqual(511, mystatic.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_bow")
                pass

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
                mystatic.get_Static_dim_to_stern()
                if i <= 511:
                    self.assertEqual(i, mystatic.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
                else:
                    self.assertEqual(511, mystatic.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_stern")
                pass

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
                mystatic.get_Static_dim_to_port()
                if i <= 62:
                    self.assertEqual(i, mystatic.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
                else:
                    self.assertEqual(63, mystatic.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_port")
                pass

    def test_get_dim_to_stbd(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_dim_to_stbd")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            mystatic.payload = self.make_stream(264, testbits)

        try:
            mystatic.get_Static_dim_to_stbd()
            if i <= 62:
                self.assertEqual(i, mystatic.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
            else:
                self.assertEqual(63, mystatic.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
        except RuntimeError:
            # logging.error("Runtime error in Static.dim_to_stbd")
            pass

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
                # logging.error("Runtime error in Static.get_eta_month")
                pass

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
        for i in [0, 1, 2, 5, 11, 12, 13, 28, 29, 30, 31]:
            testbits = '{:05b}'.format(i)
            mystatic.payload = self.make_stream(278, testbits)

            try:
                mystatic.get_eta_day()
            except RuntimeError:
                # logging.error("Runtime error in Static.get_eta_day")
                pass

            self.assertEqual(i, mystatic.eta_day,
                             "In Static.get_eta_day incorrect value returned")

    def test_get_eta_hour(self):
        # bits 283-287, 5 bits range 0-31, set to 24 (N/A) if outside range 0-23
        diction, mystream, mystatic = self.initialise()
        print("Testing Static.get_eta_hour")
        for i in [0, 1, 2, 5, 11, 12, 13, 23, 24, 28]:
            testbits = '{:05b}'.format(i)
            mystatic.payload = self.make_stream(283, testbits)

            try:
                mystatic.get_eta_hour()
            except RuntimeError:
                # logging.error("Runtime error in Static.get_eta_hour")
                pass
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
                # logging.error("Runtime error in Static.get_eta_minute")
                pass
            except ValueError:
                # outside range 0-59 but dont invalidate
                mystatic.eta_minute = 60

            if mystatic.eta_minute <= 59:
                self.assertEqual(i, mystatic.eta_minute,
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
                # logging.error("Runtime error in Static.get_draught")
                pass

            self.assertEqual(round(float(i) / 10.0, 1), mystatic.draught,
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


class TestSAR_aircraft_position_report(TestCase):

    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100pAg,0*05'
        mystream = Payloads.AISStream(psuedo_AIS)
        mysar = Payloads.SAR_aircraft_position_report(mystream.binary_payload)
        return diction, mystream, mysar

    def test_get_altitude(self):
        diction, mystream, mysar = self.initialise()

        for i in [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 4094, 4095]:
            testbits = '{:012b}'.format(i)
            mysar.payload = diction.make_stream(38, testbits)
            mysar.get_altitude()
            self.assertEqual(i, mysar.altitude,
                             "in SAR.get_altitude value returned {} "
                             "does match value expected {}".format(mysar.altitude, i))

    def test_get_speed_over_ground(self):
        diction, mystream, mysar = self.initialise()

        for i in [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 1022, 1023]:
            testbits = '{:010b}'.format(i)
            mysar.payload = diction.make_stream(50, testbits)
            mysar.get_speed_over_ground()
            self.assertEqual(i, mysar.speed_over_ground,
                             "In SAR.get_SOG value returned {} "
                             "does match value expected {}".format(mysar.speed_over_ground, i))

    def test_get_cog(self):
        diction, mystream, mycnb = self.initialise()
        print("Testing get_COG")

        # initially check for values 0, 0.5 1,359, 360 and value outside valid range
        for i in [0, 0.5, 1, 90, 359, 360, 361]:
            i = i * 10
        testbits = '{:012b}'.format(i)
        mycnb.payload = diction.make_stream(116, testbits)
        try:
            mycnb.get_course_over_ground()
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
                mycnb.get_course_over_ground()
                self.assertEqual(float(i) / 10.0, mycnb.course_over_ground,
                                 "In get_COG value returned does not offered value " + '{:d}'.format(i))
            except ValueError:
                self.assertFalse(mycnb.valid_item, "In SAR.get_COG module did not detect invalid parameter")

    def test_get_time_stamp(self):
        diction, mystream, mysar = self.initialise()

        for i in [0, 1, 2, 5, 10, 20, 50, 59, 60, 63]:
            testbits = '{:06b}'.format(i)
            mysar.payload = diction.make_stream(128, testbits)
            mysar.get_time_stamp()
            self.assertEqual(i, mysar.time_stamp,
                             "In SAR.get_timestamp value returned {} "
                             "does match value expected {}".format(mysar.time_stamp, i))

    def test_get_dte(self):
        diction, mystream, mysar = self.initialise()

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            mysar.payload = diction.make_stream(142, testbits)
            mysar.get_dte()
            if i == 1:
                self.assertTrue(mysar.dte,
                                "In SAR.get_dte value returned {} "
                                "does match value expected True".format(mysar.dte))
            else:
                self.assertFalse(mysar.dte,
                                 "In SAR.get_dte value returned {} "
                                 "does match value expected True".format(mysar.dte))

    def test_get_assigned(self):
        diction, mystream, mysar = self.initialise()

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            mysar.payload = diction.make_stream(146, testbits)
            mysar.get_assigned()
            if i == 1:
                self.assertTrue(mysar.assigned,
                                "In SAR.get_dte value returned {} "
                                "does match value expected True".format(mysar.assigned))
            else:
                self.assertFalse(mysar.assigned,
                                 "In SAR.get_dte value returned {} "
                                 "does match value expected True".format(mysar.assigned))

    def test_repr(self):
        diction, mystream, mysar = self.initialise()

        print(mysar)


class TestAddressed_safety_related_message(TestCase):
    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,<7Ol>01ou3P09>F1<94PD5HD00000000000000000000000000000000000000,0*5'
        mystream = Payloads.AISStream(psuedo_AIS)
        mysafety = Payloads.Addressed_safety_related_message(mystream.binary_payload)
        return diction, mystream, mysafety

    def test_get_repeat_indicator(self):
        diction, mystream, mysafety = self.initialise()

        # 2 bits, 6-7 unsigned integer 0-3, no other values exist
        for i in [0, 1, 2, 3]:
            testbits = '{:02b}'.format(i)
            testbits = diction.make_stream(4, testbits)

            mysafety.payload = testbits
            mysafety.get_repeat_indicator()
            self.assertEqual(i, mysafety.repeat_indicator,
                             "In Addressed Safety.sequence returned value does not match expected value")

    def test_get_sequence_number(self):
        diction, mystream, mysafety = self.initialise()

        # 2 bits, 38-39 unsigned integer 0-3, no other values exist
        for i in [0, 1, 2, 3]:
            testbits = '{:02b}'.format(i)
            testbits = diction.make_stream(38, testbits)

            mysafety.payload = testbits
            mysafety.get_sequence_number()
            self.assertEqual(i, mysafety.sequence_number,
                             "In Addressed Safety.sequence returned value does not match expected value")

    def test_get_destination_mmsi(self):
        diction, mystream, mysafety = self.initialise()

        print('Testing Addressed Safety get Destination mmsi')

        smmsi_list: list = [
            '850312345', '503543210', '050398765', '005037651', '111504678',
            '998761234', '984135432', '970654987', '972654321', '974765432',
            '999999999'
        ]

        # the mmsi field is bits 40-69 of the binary payload string

        for ssm in smmsi_list:
            sm: str = ssm
            mmsibits = '{:030b}'.format(int(sm))
            mmsibits = diction.make_stream(40, mmsibits)
            mysafety.payload = mmsibits

            try:
                mysafety.get_destination_mmsi()

                self.assertEqual(sm, mysafety.destination_mmsi,
                                 "Failed in Addressed Safety get destination mmsi ")
            except RuntimeError:
                # logging.error("Runtime Error in testing Addressed SAfety get destination mmsi")
                pass

    def test_get_retransmit_flag(self):
        diction, mystream, mysafety = self.initialise()

        print('Testing Addressed Safety get Retransmit flag')

        for i in [0, 1]:
            testbits = "{:01b}".format(i)
            testbits = diction.make_stream(70, testbits)

            mysafety.payload = testbits
            mysafety.get_retransmit_flag()
            if i == 0:
                self.assertFalse(mysafety.retransmit_flag,
                                 "In Addressed SAfety get retrandsmit flag incorrectr bool returned")
            else:
                self.assertTrue(mysafety.retransmit_flag,
                                "In Addressed SAfety get retrandsmit flag incorrectr bool returned")

    def test_get_safety_text(self):
        diction, mystream, mysafety = self.initialise()
        print('Testing Addressed Safety get Safety Text')

        # again effectively free text - only upper case allowed

        for a in ['Melbourne',
                  'Australian Explorer',
                  '12345678901234567890',
                  'ABCDEFGHIJKLMNOPQRST',
                  'abcdefghijklmnopqrst',
                  '12345678901234567890',
                  '01234567890123456789012345678901234567890123456789012345678900987654321'
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper())
            test_bits = diction.make_stream(72, test_bits)
            mysafety.payload = test_bits
            try:
                mysafety.get_safety_text()
                self.assertTrue(a.upper() == mysafety.safety_text,
                                "In Addressed Safety.get_safety text, value returned\n "
                                + mysafety.safety_text + "\nnot equal to value offered \n" + a.upper())

            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Addressed Safety.get_safety text")

    def test_repr(self):
        diction, mystream, mysafety = self.initialise()
        print("testing Addressed Safety \n __repr__")
        print(mysafety)
        # should have a valid data set as a result of the initiaslise()


class TestSafety_related_broadcast_message(TestCase):
    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,>7Ol>009>F1<94PD5HD00000000000000000000000000000000000000,0*5'
        mystream = Payloads.AISStream(psuedo_AIS)
        mysafety = Payloads.Safety_related_broadcast_message(mystream.binary_payload)

        return diction, mystream, mysafety

    def test_get_safety_text(self):
        diction, mystream, mysafety = self.initialise()
        print('Testing Addressed Safety get Safety Text')

        # again effectively free text - only upper case allowed

        for a in ['Melbourne',
                  'Australian Explorer',
                  '12345678901234567890',
                  'ABCDEFGHIJKLMNOPQRST',
                  'abcdefghijklmnopqrst',
                  '12345678901234567890',
                  '01234567890123456789012345678901234567890123456789012345678900987654321'
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper())
            test_bits = diction.make_stream(40, test_bits)
            mysafety.payload = test_bits
            try:
                mysafety.get_safety_text()
                self.assertEqual(a.upper(), mysafety.safety_text,
                                 "In Addressed Safety.get_safety text, value returned\n "
                                 + mysafety.safety_text + "\nnot equal to value offered \n" + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Addressed Safety.get_safety text")

    def test_repr(self):
        diction, mystream, mysafety = self.initialise()
        print("testing Broadcast Safety __repr__")
        print(mysafety)
        # should have a valid data set as a result of the initiaslise()


class TestAid_to_navigation_report(TestCase):
    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,E7Ol>004W;0V4R@:2d:000000005@M=0:ok@0000000001F53`51F50000000,0*5'
        mystream = Payloads.AISStream(psuedo_AIS)
        myaid = Payloads.Aid_to_navigation_report(mystream.binary_payload)

        return diction, mystream, myaid

    def test_get_aid_type(self):
        # 5 bits range 0-31, no range validation needed
        diction, mystream, myaid = self.initialise()
        print('Testing NAV Aid.get_aid_type')

        for i in [0, 1, 2, 5, 10, 20, 30, 31]:
            testbits = '{:05b}'.format(i)
            myaid.payload = diction.make_stream(38, testbits)
            myaid.get_aid_type()
            self.assertEqual(i, myaid.aid_type, "In Aid to Navigation.aid_type value returned {} "
                                                "not equal to value expected {} ".format(i, myaid.aid_type))

    def test_get_nav_name(self):
        diction, mystream, myaid = self.initialise()
        for a in ['Melbourne',
                  'Australian Explorer',
                  '12345678901234567890',
                  'ABCDEFGHIJKLMNOPQRST',
                  'abcdefghijklmnopqrst',
                  '12345678901234567890',
                  '01234567890123456789012345678901234567890123456789012345678900987654321'
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper()[0:20])
            test_bits = diction.make_stream(43, test_bits)
            myaid.payload = test_bits
            try:
                myaid.get_NAV_name()
                self.assertTrue(a.upper()[0:20] == myaid.vessel_name,
                                "In Addressed Safety.get_safety text, value returned\n "
                                + myaid.vessel_name + "\nnot equal to value offered \n" + a.upper())
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Aid to Navigation - get aid name")

    def test_get_nav_longitude(self):
        # assumed OK if tests in class Payload are OK
        pass

    def test_get_nav_latitude(self):
        # assumed OK if tests in class Payload are OK
        pass

    def test_get_nav_dim_to_bow(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 9 bits therefore range 0-511

        diction, mystream, myaid = self.initialise()
        print("Testing Nav Aid.get_dom_to_bow")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            myaid.payload = diction.make_stream(219, testbits)

            try:
                myaid.get_NAV_dim_to_bow()
                if i <= 511:
                    self.assertEqual(i, myaid.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
                else:
                    self.assertEqual(511, myaid.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_bow")
                pass

    def test_get_nav_dim_to_stern(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, myaid = self.initialise()
        print("Testing Nav Aid.get_dim_to_stern")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            myaid.payload = diction.make_stream(228, testbits)

            try:
                myaid.get_NAV_dim_to_stern()
                if i <= 511:
                    self.assertEqual(i, myaid.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
                else:
                    self.assertEqual(511, myaid.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_stern")
                pass

    def test_get_nav_dim_to_port(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 6 bits range 0-63

        diction, mystream, myaid = self.initialise()
        print("Testing Nav Aid.get_dim_to_port")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            myaid.payload = diction.make_stream(237, testbits)

            try:
                myaid.get_NAV_dim_to_port()
                if i <= 62:
                    self.assertEqual(i, myaid.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
                else:
                    self.assertEqual(63, myaid.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_port")
                pass

    def test_get_nav_dim_to_stbd(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, myaid = self.initialise()
        print("Testing Nav Aid.get_dim_to_stbd")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            myaid.payload = diction.make_stream(243, testbits)

        try:
            myaid.get_NAV_dim_to_stbd()
            if i <= 62:
                self.assertEqual(i, myaid.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
            else:
                self.assertEqual(63, myaid.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
        except RuntimeError:
            # logging.error("Runtime error in Static.dim_to_stbd")
            pass

    def test_get_nav_epfd(self):
        # 4 bits range 0-`15`, no range validation needed
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.get_epfd')

        for i in [0, 1, 2, 5, 8, 15]:
            testbits = '{:04b}'.format(i)
            myaid.payload = diction.make_stream(249, testbits)
            myaid.get_NAV_EPFD()
            self.assertEqual(i, myaid.EPFD_type, "In Aid to Navigation.epfd value returned {} "
                                                 "not equal to value expected {} ".format(i, myaid.EPFD_type))

    def test_get_nav_utc_second(self):
        diction, mystream, myaid = self.initialise()

        myaid.utc_second = myaid.binary_item(253, 6)

    def test_get_nav_off_position_indicator(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.get_off_position_flag')

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            myaid.payload = diction.make_stream(259, testbits)
            myaid.get_NAV_off_position_indicator()
            if i == 1:
                self.assertTrue(myaid.off_position_indicator,
                                "In NavAid get off posn value returned {} "
                                "does match value expected True".format(myaid.off_position_indicator))
            else:
                self.assertFalse(myaid.off_position_indicator,
                                 "In NavAid get off posn value returned {} "
                                 "does match value expected True".format(myaid.off_position_indicator))

    def test_get_nav_raim_flag(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.get_raim_flag')

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            myaid.payload = diction.make_stream(268, testbits)
            myaid.get_NAV_raim_flag()
            if i == 1:
                self.assertTrue(myaid.raim_flag,
                                "In NavAid get raim value returned {} "
                                "does match value expected True".format(myaid.raim_flag))
            else:
                self.assertFalse(myaid.off_position_indicator,
                                 "In NavAid get rfaim value returned {} "
                                 "does match value expected True".format(myaid.raim_flag))

    def test_get_nav_virtual_aid_flag(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.get_virtual_aid_flag')

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            myaid.payload = diction.make_stream(269, testbits)
            myaid.get_NAV_virtual_aid_flag()
            if i == 1:
                self.assertTrue(myaid.virtual_aid_flag,
                                "In NavAid get virt aid value returned {} "
                                "does match value expected True".format(myaid.virtual_aid_flag))
            else:
                self.assertFalse(myaid.virtual_aid_flag,
                                 "In NavAid get virt aid value returned {} "
                                 "does match value expected True".format(myaid.virtual_aid_flag))

    def test_get_nav_assigned_flag(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.get_assigned_flag')

        for i in [0, 1]:
            testbits = '{:01b}'.format(i)
            myaid.payload = diction.make_stream(270, testbits)
            myaid.get_NAV_assigned_flag()
            if i == 1:
                self.assertTrue(myaid.assigned_mode,
                                "In NavAid get assoigned value returned {} "
                                "does match value expected True".format(myaid.assigned_mode))
            else:
                self.assertFalse(myaid.assigned_mode,
                                 "In NavAid get assoigned value returned {} "
                                 "does match value expected True".format(myaid.assigned_mode))

    def test_get_nav_name_extension(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.name_extension')

        # should check for null name as well

        for a in ['Melbourne',
                  'Aust. Exp',
                  '12345678901234',
                  'ABCDEFGHIJKLMN',
                  'abcdefghijklmn',
                  ''
                  ]:
            test_bits = ''
            test_bits = diction.char_to_binary(a.upper())
            test_bits = diction.make_stream(272, test_bits)
            myaid.payload = test_bits
            try:
                myaid.get_NAV_name_extension()
                self.assertEqual(a.upper(), myaid.name_extension,
                                 "In Addressed Safety.get_name extension, value returned\n "
                                 + myaid.name_extension + "\nnot equal to value offered \n" + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in Aid to Navigation - get name extension")

    def test_repr(self):
        diction, mystream, myaid = self.initialise()
        print('Testing Nav_aid.__repr__')
        myaid.payload = '01010100'

        myaid.payload = (myaid.payload + '{:030b}'.format(5031234) + '01010'
                         + diction.char_to_binary('AID NAME@@@@@@@@@@@@')
                         + '0'
                         + '{:028b}'.format(2300000)
                         + '{:027b}'.format(23000)
                         + '{:09b}'.format(100)
                         + '{:09b}'.format(105)
                         + '{:06b}'.format(10)
                         + '{:06b}'.format(15)
                         + '{:04b}'.format(5)
                         + '{:06b}'.format(47)
                         + '1'
                         + '000000001110'
                         + diction.char_to_binary('EXTENSION')
                         )

        myaid.create_mmsi()
        myaid.get_aid_type()
        myaid.get_NAV_name()
        myaid.get_NAV_longitude()
        myaid.get_NAV_latitude()
        myaid.get_NAV_dim_to_bow()
        myaid.get_NAV_dim_to_stern()
        myaid.get_NAV_dim_to_port()
        myaid.get_NAV_dim_to_stbd()
        myaid.get_NAV_EPFD()
        myaid.get_NAV_UTC_second()
        myaid.get_NAV_off_position_indicator()
        myaid.get_NAV_raim_flag()
        myaid.get_NAV_virtual_aid_flag()
        myaid.get_NAV_assigned_flag()
        myaid.get_NAV_name_extension()

        print(myaid)


class TestStatic_data_report(TestCase):
    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,H7Ol>00TqH4hTB1@EQ@00000000,0*5'
        mystream = Payloads.AISStream(psuedo_AIS)
        mybase24 = Payloads.Static_data_report(mystream.binary_payload)
        return diction, mystream, mybase24

    def test_get_part_number(self):
        # 2 bits at 38-39
        # values 0 or 1

        diction, mystream, mybase24 = self.initialise()
        print('Testing 24.get_part_number of type 24')

        for i in [0, 1, 2, 3]:

            testbits = '{:02b}'.format(i)
            mybase24.payload = diction.make_stream(38, testbits)

            try:
                mybase24.get_part_number()
                self.assertEqual(i, mybase24.part_number,
                                 "In Type24 base, part number returned does not match part number expoected")
            except ValueError:
                self.assertFalse(mybase24.valid_item, "In type 24 base, invalid part number not flagged")

    def test_get_24_vessel_name(self):
        diction, mystream, mybase24 = self.initialise()
        print('Testing 24.get_vessel_name')

        testbits = diction.char_to_binary('TEST SHIP NAME@@@@@@')
        mybase24.payload = diction.make_stream(40, testbits)

        try:
            mybase24.get_24_vessel_name()
            self.assertEqual('TEST SHIP NAME', mybase24.vessel_name,
                             "Incorrect data returned in TYpe 24 Part A vessel name")
        except ValueError:
            self.assertFalse(mybase24.valid_item,
                             "Incorrect value in type 24 get vessel name not flagged ")


    def test_get_24_ship_type(self):
        # validation for ship type done in class BasicPosition
        # need to check here that when presented with a valid ship type the same value is returned
        diction, mystream, mybase24 = self.initialise()
        print('Testing 24.get_ship_type')

        testbits = "{:08b}".format(30)
        mybase24.payload = diction.make_stream(40, testbits)

        try:
            mybase24.get_24_ship_type()
            self.assertEqual(30, mybase24.ship_type, 'Incorrect value returned in Type24B ship type')
        except ValueError:
            self.assertFalse(mybase24.valid_item, "Incorrect value in TYpe24B ship type not flagged correctly")

    def test_get_vendor_id(self):
        # this one is peculiar to TYpe24B so needs more testing
        # 18 bits comprising 3 six bit characters or alternatively 7 characters (pre1371_4)
        # all that can be testewd is that data presented is returned OK

        diction, mystream, mybase24 = self.initialise()
        print('Testing 24.get_vendor_id both pre and post 1371_4')
        # test posdt 1371_4 version first
        testbits = diction.char_to_binary('ABC')
        mybase24.payload = diction.make_stream(48, testbits)
        try:
            mybase24.get_vendor_id()
            self.assertEqual('ABC', mybase24.vendor_id, "In Type24B vendor ID incorrectly returned")
        except ValueError:
            self.assertFalse(mybase24.valid_item, "In Type24B incorrect Vendor ID not correctly Flagged")

        # now for pre1371_4
        testbits = diction.char_to_binary('ABC0109')
        mybase24.payload = diction.make_stream(48, testbits)
        try:
            mybase24.get_vendor_id()
            self.assertEqual('ABC0109', mybase24.pre1371_4_vendor_id,
                             "In Type24B pre1371_4 vendor ID incorrectly returned")
        except ValueError:
            self.assertFalse(mybase24.valid_item,
                             "In Type24B pre1371_4 incorrect Vendor ID not correctly Flagged")

    def test_get_unit_model_code(self):
        # post 1371_4 4 bits 66-69 integer
        # again can only check that correct value returned
        diction, mystream, mybase24 = self.initialise()

        testbits = '{:04b}'.format(12)
        mybase24.payload = diction.make_stream(66, testbits)
        print('Testing 24.get_sunit_model_code')

        try:
            mybase24.get_unit_model_code()
            self.assertEqual(12, mybase24.unit_model_code,
                             "In Type24B post1371_4 unit model incorrectly returned")
        except ValueError:
            self.assertFalse(mybase24.valid_item,
                             "In Type24B post1371_4 incorrect unit model code not correctly Flagged")

    def test_get_serial_number(self):
        # bits 70-89 20- bit integer max value 1048575 (7 digits)
        # all that can be done here is to check that value returned matches value set
        diction, mystream, mybase24 = self.initialise()
        print('Testing 24.get_serial_number')

        testbits = '{:020b}'.format(1038575)
        mybase24.payload = diction.make_stream(70, testbits)

        try:
            mybase24.get_serial_number()
            self.assertEqual(1038575, mybase24.serial_number,
                             "In Type24B post1371_4 serial number {} incorrectly returned".format(
                                 mybase24.serial_number))
        except ValueError:
            self.assertFalse(mybase24.valid_item,
                             "In Type24B post1371_4 incorrect serial number not correctly flagged")

    def test_get_callsign(self):
        diction, mystream, mybase24 = self.initialise()
        print("Testing 24.get_callsign")

        # again effectively free text

        for a in ['VH12345', 'ABVCDEF']:
            test_bits = ''
            # for x in a:
            #     test_bits = test_bits + diction.char_to_binary(x)
            #     print (x, test_bits)
            test_bits = diction.char_to_binary(a)
            test_bits = diction.make_stream(90, test_bits)
            mybase24.payload = test_bits
            try:
                mybase24.get_callsign()
                self.assertEqual(a, mybase24.callsign, "In 24B.get_callsign, value returned "
                                 + mybase24.callsign + " not equal to value offered " + a)
            except RuntimeError:
                self.assertFalse(True, "Runtime Error in 24B.get_callsign")

    def test_get_dim_to_bow(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 9 bits therefore range 0-511

        diction, mystream, mybase24 = self.initialise()
        print("Testing 24.get_dom_to_bow")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            mybase24.payload = diction.make_stream(132, testbits)

            try:
                mybase24.get_24_dim_to_bow()
                if i <= 511:
                    self.assertEqual(i, mybase24.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
                else:
                    self.assertEqual(511, mybase24.dim_to_bow,
                                     "In Static.get_dim_to_bow value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_bow")
                pass

    def test_get_dim_to_stern(self):
        # Ship  dimensions will be 0 if not available.
        # For the dimensions to bow and stern, the special value  511 indicates 511 meters or greater;
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, mybase24 = self.initialise()
        print("Testing 24.get_dim_to_stern")

        for i in [0, 10, 100, 500, 511]:
            testbits = '{:09b}'.format(i)
            mybase24.payload = diction.make_stream(141, testbits)

            try:
                mybase24.get_24_dim_to_stern()
                if i <= 511:
                    self.assertEqual(i, mybase24.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
                else:
                    self.assertEqual(511, mybase24.dim_to_stern,
                                     "In Static.get_dim_to_stern value returned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_stern")
                pass

    def test_get_dim_to_port(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.
        # 6 bits range 0-63

        diction, mystream, mybase24 = self.initialise()
        print("Testing 24.get_dim_to_port")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            mybase24.payload = diction.make_stream(150, testbits)

            try:
                mybase24.get_24_dim_to_port()
                if i <= 62:
                    self.assertEqual(i, mybase24.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
                else:
                    self.assertEqual(63, mybase24.dim_to_port,
                                     "In Static.get_dim_to_stern value reurned incorrect")
            except RuntimeError:
                # logging.error("Runtime error in Static.dim_to_port")
                pass

    def test_get_dim_to_stbd(self):
        # Ship  dimensions will be 0 if not available.
        # for the dimensions to port and starboard, the special value 63 indicates 63 meters or greater.

        diction, mystream, mybase24 = self.initialise()
        print("Testing 24.get_dim_to_stbd")
        for i in [0, 10, 62, 63]:
            testbits = '{:06b}'.format(i)
            mybase24.payload = diction.make_stream(156, testbits)

        try:
            mybase24.get_24_dim_to_stbd()
            if i <= 62:
                self.assertEqual(i, mybase24.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
            else:
                self.assertEqual(63, mybase24.dim_to_stbd,
                                 "In Static.get_dim_to_stbd value returned incorrect")
        except RuntimeError:
            # logging.error("Runtime error in Static.dim_to_stbd")
            pass

    def test_get_mothership_mmsi(self):
        # again not much that can be done here
        # check if value returnred matched value set

        diction, mystream, mybase24 = self.initialise()
        print("Testing 24B get mother ship MMSI")

        smmsi_list: list = [
            '850312345', '503543210', '050398765', '005037651', '111504678',
            '998761234', '984135432', '970654987', '972654321', '974765432',
            '999999999'
        ]

        # the mmsi field is bits 40-69 of the binary payload string

        for ssm in smmsi_list:
            sm: str = ssm
            mmsibits = '{:030b}'.format(int(sm))
            mmsibits = diction.make_stream(132, mmsibits)
            mybase24.payload = mmsibits

            try:
                mybase24.get_mothership_mmsi()

                self.assertEqual(sm, mybase24.mothership_mmsi,
                                 "Failed in Type24B (auxiliary) get mothership mmsi ")
            except RuntimeError:
                # logging.error("Runtime Error in testing Type24B (auxiliary) get mothership mmsi")
                pass


class TestLong_range_AIS_broadcast_message(TestCase):
    def initialise(self):
        logging.basicConfig(level=logging.CRITICAL, filename='logfile.log')
        diction = AISDictionaries()
        # the stream offered here is valid but the mystream.payload , mypayload.payload
        #  and/or mystream.binary_payload will be overwritten during testing
        psuedo_AIS = '!AIVDM,1,1,,A,H7Ol>040F5>wwwwEg1F19<Mw@p00,0*5,0*5'
        mystream = Payloads.AISStream(psuedo_AIS)
        mytype27 = Payloads.Long_range_AIS_broadcast_message(mystream.binary_payload)
        return diction, mystream, mytype27

    def test_get_longitude(self):
        # since weknow that the BasicPosition algorithm for Longitude and Latitude works
        # albeit with a scaling factor of 600000
        # can do some tests here with the changed scling factor of 600.
        # range -180 to 180 , 181 indicates not available

        diction, mystream, mytype27 = self.initialise()

        for i in {-180.0, 180.0, 0.0, 90.0, 181.0, 182.0}:
            testbits = '{:018b}'.format(int(i * 600.0))
            mytype27.payload = diction.make_stream(44, testbits)
            try:
                mytype27.get_27longitude(44, 18)
                self.assertEqual(i, mytype27.longitude,
                                 'In TYpe27 get Longitude incorrect value returned')
            except ValueError:
                self.assertFalse(mytype27.valid_item,
                                 ' In TYpe27 get Longitude incorrect value not flagged')

    def test_get_latitude(self):
        # since we know that the BasicPosition algorithm for Longitude and Latitude works
        # albeit with a scaling factor of 600000
        # can do some tests here with the changed scling factor of 600.
        # range -90 to 90, 91 indicates not available

        diction, mystream, mytype27 = self.initialise()

        for i in {-90.0, 90.0, 0.0, 91.0, 92.0}:

            testbits = '{:017b}'.format(int(i * 600.0))
            mytype27.payload = diction.make_stream(62, testbits)
            try:
                mytype27.get_27latitude(62, 17)
                self.assertEqual(i, mytype27.latitude,
                                 'In TYpe27 get Latitude incorrect value returned')
            except ValueError:
                self.assertFalse(mytype27.valid_item,
                                 ' In TYpe27 get Latitude incorrect value not flagged')
