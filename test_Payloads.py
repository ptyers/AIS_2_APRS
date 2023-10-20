from unittest import TestCase
from AISDictionary import AISDictionaries
import Payloads
import random
import logging


class TestPayload(TestCase):
    pass


class TestCNB(TestCase):
    pass


class TestBasestation(TestCase):
    pass


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
    def test_extract_mmsi(self):
        self.fail()

    def test_binary_item(self):
        self.fail()

    def test_put_frag_in_dict(self):
        self.fail()

    def test_match_fragments(self):
        self.fail()


class TestPayload(TestCase):

    def initialise(self):
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
            '9999999999'
        ]

        # the mmsi field is bits 8-37 of the binary payload string
        # so split the mystream.binary_payload generated in the initialiastion into three parts
        # bits 0-7, bits 38-end and substitute the 30 bits that are the mmsi field

        header: str = mystream.binary_payload[0:7]
        trailer: str = mystream.binary_payload[38:]

        for sm in smmsi_list:
            mmsibits = '{:09b}'.format(int(sm))
            mystream.binary_payload = header + mmsibits + trailer

            try:
                mypayload = Payloads.Payload(mystream.binary_payload)
                mypayload.create_mmsi()
                ommsi: str = mypayload.mmsi
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
            #print('character, string value', char, str_val )
            bin_val = int(str_val,2)
            ret_val = mypayload.m_to_int(char)
            self.assertEqual(bin_val, ret_val,'In Payload.m_to_int - returned binary does not match encoded char')

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
        for i in range(1,10):
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


    def test_get_longitude(self):
        self.fail()

    def test_get_latitude(self):
        self.fail()

    def test_signed_binary_item(self):
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

        fakestream: str = '00010000'
        faketail: str = '000000000000000000000000000000'
        #testnumber: int = random.randint(0, 999999999)
        strnumber: str = "{:028b}".format(0)
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(0, intmmsi,"In Payload.signed_binary_int - Offered 0 but got non zero")
        strnumber: str = "{:028b}".format(1)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(1, intmmsi, "In Payload.signed_binary_int - Offered 1 but got not 1")
        strnumber: str = "{:028b}".format(-1)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(-1, intmmsi, "In Payload.signed_binary_int - Offered -1 but got not -1")
        mynumb = 181*600000
        strnumber: str = "{:028b}".format(mynumb)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(181*600000, intmmsi, "In Payload.signed_binary_int - Offered 1 but got not 1")
        strnumber: str = "{:028b}".format(-180 * 600000)
        fakestream: str = '00010000'
        fakestream = fakestream + strnumber + faketail
        mypayload.payload = fakestream
        intmmsi = mypayload.signed_binary_item(8, 28)
        self.assertEqual(-180 * 600000, intmmsi, "In Payload.signed_binary_int - Offered 1 but got not 1")

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
        self.fail()


class TestCNB(TestCase):
    def test_get_nav_status(self):
        self.fail()

    def test_get_rot(self):
        self.fail()

    def test_get_sog(self):
        self.fail()

    def test_get_cog(self):
        self.fail()

    def test_get_tru_head(self):
        self.fail()

    def test_get_pos_accuracy(self):
        self.fail()

    def test_get_timestamp(self):
        self.fail()

    def test_get_man_indic(self):
        self.fail()


class TestBasestation(TestCase):
    def test_get_year(self):
        self.fail()

    def test_get_month(self):
        self.fail()

    def test_get_day(self):
        self.fail()

    def test_get_hour(self):
        self.fail()

    def test_get_minute(self):
        self.fail()

    def test_get_second(self):
        self.fail()

    def test_get_epfd(self):
        self.fail()


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



