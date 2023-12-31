from unittest import TestCase

import AISData
from AISData import AIS_Data
from AISDictionary import AISDictionaries
import logging
import random


class TestAIS_Data(TestCase):
    # function used to initialise tests. sets up access to AIS_Data and Dictionary

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

    # generic initiale to allow testing - I know the stream offered to the initialise is valid
    def initialise(self):
        diction = AISDictionaries()
        mydata = AISData.AIS_Data(
            "!AIVDM", "1", "1", "", "A",
            "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n")
        return diction, mydata

    def test_binary_item(self):
        '''
        Produces random number in rage 0 to 999999999 and sets up fake binary_payload string
        then extracts that binary number from the string using AIS_Data.Binary_item
        '''
        # some necessary preconfig
        # dict = AISDictionaries()
        # mydata = AIS_Data(
        #     "!AIVDM", "1", "1", "", "A",
        #     "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n"
        # )
        dict, mydata = self.initialise()
        print("Testing Binary_item")
        # Create fake AIS payload with a random binary number in bits 8 to 37
        for i in range(10):
            fakestream: str = '00010000'
            faketail: str = '000000000000000000000000000000'

            testnumber: int = random.randint(0, 999999999)
            strnumber: str = "{:030b}".format(testnumber)
            fakestream = fakestream + strnumber + faketail
            mydata.set_AIS_Binary_Payload(fakestream)
            intmmsi = mydata.Binary_Item(8, 30)
            self.assertEqual(testnumber, intmmsi, "FAiled in test_binary_item")

    '''
    block of strings to get test data
    '''

    def test_create_binary_payload(self):
        dict, mydata = self.initialise()
        print('Testing create_binary_payload')
        for i in range(len(self.mytestdata) - 1):
            self.testpay: str = ''
            payload = self.mytestdata[i].split(',')
            self.binpay, self.binlen = mydata.create_binary_payload(payload[5])
            mydata.set_AIS_Binary_Payload(self.binpay)
            mydata.set_AIS_Binary_Payload_length(self.binlen)
            for char in payload[5]:
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



            self.assertEqual(self.testpay, self.binpay, "Create binary payload failure")

    def test_create_bytearray_payload(self):
        dict = AISDictionaries()
        binpay: bytearray
        print('Testing create_bytearray_payload')
        for i in range(5):
            self.testpay: str = ''
            payload = self.mytestdata[i].split(',')
            self.binpay, self.binlength = AIS_Data.create_bytearray_payload(payload[5])
            self.ostring = ''
            for i in range(len(self.binpay)):
                self.ostring = self.ostring + "{:08b}".format(self.binpay[i])

            logging.debug("character version of bytearray\n{}".format( self.ostring))
            testpay = payload[5]
            for ij in range(len(testpay)):
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, testpay[ij])

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
        diction = AISDictionaries()
        mydata = AIS_Data(
            "!AIVDM", "1", "1", "", "A",
            "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n")

        for _ in range(20):
            # create a random length integer
            testlength: int = random.randint(1, 10)
            testnumb: int = random.randint(0, 9999999999)
            numstring: str = "{:010d}".format(testnumb)
            # extract required length string from the 10 character string
            numbstring = numstring[10 - testlength:]
            # #make encoded string using dictionary
            outint = mydata.m_to_int2(numbstring)
            self.assertEqual(int(numbstring), outint, "Failure in m_to_int")

    def test_ExtractInt(self):
        '''
               Produces random number in rage 0 to 999999999 and sets up fake binary_payload string
               then extracts that binary number from the string using AIS_Data.Binary_item
               effectively same test as for Binary_item
               '''
        # some necessary preconfig
        dict = AISDictionaries()
        mydata = AIS_Data(
            "!AIVDM", "1", "1", "", "A",
            "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n")

        print("Testing extract_int")
        # Create fake AIS payload with a random binary number in bits 8 to 37
        for i in range(10):
            fakestream: str = '00010000'
            faketail: str = '000000000000000000000000000000'

            testnumber: int = random.randint(0, 999999999)
            strnumber: str = "{:030b}".format(testnumber)
            fakestream = fakestream + strnumber + faketail
            mydata.set_AIS_Binary_Payload(fakestream)
            intmmsi = mydata.ExtractInt(8, 30)
            self.assertEqual(testnumber, intmmsi, "FAiled in test_binary_item")

    def test_extract_string(self):
        '''
                Create dummy binary payload including some test strings use Extract_String to recover text
        :return:
            string text to be compared
        '''
        print("Testing ExtractString")
        diction, mydata = self.initialise()

        fakestream: str = '00010000'
        faketail: str = '11111111111111111111'

        testtext: str = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw01234567890:;<>=?@@AB'

        for _ in range(10):

            for ik in range(len(testtext)):
                fakestream = diction.makebinpayload(fakestream, testtext[ik])
            fakestream = fakestream + faketail

            # set this as "binary_payload" in AIS_Data and set its length as 6 times the text length plus
            # additional head/tail bits (28)
            mydata.set_AIS_Binary_Payload(fakestream)
            mydata.set_AIS_Binary_Payload_length((len(testtext) * 6) + 28)

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

            startpos: int = 8 + rndstrt * 6
            blklen = rndlen * 6

            logging.debug("DEBUG binary_payload from which string will be extracted\n{}"
            .format(mydata.get_AIS_Binary_Payload()))

            outstr = mydata.ExtractString(startpos, rndlen * 6)
            logging.debug('Extracted string {}'.format( outstr))

            self.assertEqual(rndtext, outstr, "Failed in Extract_String")

        ##### Error still exists last character in string if @ returns as w

    def test_extract_random_mmsi(self):
        # takes in a variety of MMSIs as per the dictionary
        # sets upo dummy binary sequence and extracts them
        # tests for both integer MMSI and String MMSI

        print("Testing extract_random MMSI")
        diction, mydata = self.initialise()

        smmsi_list: list = [
            '850312345', '503543210', '050398765', '005037651', '111504678',
            '998761234', '984135432', '970654987', '972654321', '974765432'
        ]

        for im in smmsi_list:
            binstring = "{:030b}".format(int(im))
            # setup fake header  type 4 repeat  indicator = 1, then the 30 bit MMSI and a fake tail (using fake header
            fakehead = '00100000'
            binary_stream = fakehead + binstring + fakehead
            mydata.set_AIS_Binary_Payload(binary_stream)
            ommsi, osmmsi = mydata.extract_random_mmsi(8, 30)
            self.assertEqual(int(im), ommsi, "Failed in get random mmsi integer form")
            self.assertEqual(im, osmmsi, "Failed in get random mmsi string form")

    def test_set_mmsi(self):
        print('Testing set mmsi')
        diction, mydata = self.initialise()
        smmsi_list: list = [
            '850312345', '503543210', '050398765', '005037651', '111504678',
            '998761234', '984135432', '970654987', '972654321', '974765432',
            '9999999999', 'A99999999'
                            ]
        for sm in smmsi_list:
            if sm[0] != "A":
                try:
                    mydata.set_mmsi(int(sm))
                    ommsi = mydata.get_mmsi()
                    self.assertEqual(int(sm), ommsi, "Failed in get/set random mmsi integer form")
                    osmmsi = mydata.get_smmsi()
                    self.assertEqual(sm, osmmsi, "Failed in get/set random mmsi in string form")
                except ValueError:
                    pass
            if sm[0] == 'Á':
                try:
                    mydata.set_mmsi(int(sm))
                    self.assertNotEquals(1,1,"Failed allowed alphabetic MMSI to be offewred")
                except ValueError:
                    pass

    def test_print_ais(self):
        self.assertEqual(1, 1, "Print_ais not tested")

    def test_m_initialise(self):
        self.assertEqual(1, 1, "m_initialise not tested")

    def test_m_setup(self):
        self.assertEqual(1, 1, "m_setup not tested")

    def test_remove_at(self):
        print('Testing remove @')
        diction, mydata = self.initialise()
        for cs in ['cg22', 'CG22', 'ABCDE765@@', 'ABC765 @']:
            result = ''
            try:
                out = mydata.Remove_at(cs)

                for i in cs:
                    if not (i == '@'):
                        result = result + i
                self.assertEqual(result, out, "Failed in remove at")
            except ValueError:
                pass

    def test_remove_space(self):
        print('Testing remove space')
        diction, mydata = self.initialise()
        for cs in ['cg22', 'CG22', 'ABCDE765@@', 'ABC765 @']:
            result = ''
            try:
                out = mydata.Remove_space(cs)

                for i in cs:
                    if not (i == ' '):
                        result = result + i
                self.assertEqual(result, out, "Failed in remove at")
            except ValueError:
                pass

    def test_set_Encoded_String(self):
        print("Testing set_EncodedString")
        diction, mydata = self.initialise()
        mydata.set_Encoded_String(self.mytestdata[0].split(',')[5])
        out = mydata.get_Encoded_String()
        self.assertEqual(self.mytestdata[0].split(',')[5], out)

    def test_get_Encoded_String(self):
        print("Testing getEncodedString")
        diction, mydata = self.initialise()
        mydata.set_Encoded_String(self.mytestdata[0].split(',')[5])
        out = mydata.get_Encoded_String()
        self.assertEqual(self.mytestdata[0].split(',')[5], out)

    def test_set_Fragment(self):
        print("Testing set_Fragment Count")
        diction, mydata = self.initialise()
        for intid in range(0, 10):
            try:
                mydata.set_fragment(intid)
                intout = mydata.get_fragment()
                self.assertEqual(intid, intout, "Failed in test get/set Fragment Count")
            except ValueError:
                pass

    def test_set_Fragmentno(self):
        print("Testing set_Fragment count to Complete")
        diction, mydata = self.initialise()
        for intid in range(0, 10):
            try:
                mydata.set_fragnumber(value=intid)
                intout = mydata.get_fragno()
                self.assertEqual(intid, intout, "Failed in test get/set Fragment Count to complete")
            except ValueError:
                pass

    def test_get_message_id(self):
        diction, mydata = self.initialise()
        print("Testing get_Message_ID")

        # use first item in the list of AIS streams to get a message id, field
        mydata.set_Message_ID(self.mytestdata[0].split(',')[3])
        out = mydata.get_Message_ID()
        self.assertEqual(self.mytestdata[0].split(',')[3], out)

    def test_get_AIS_channel(self):
        print("Testing getAIUS Channel")
        diction, mydata = self.initialise()

        mydata.set_ais_Channel('A')
        out = mydata.get_AIS_Channel()
        self.assertEqual("A", out, "Failed in test get_AIS_Channel")

    def test_get_AIS_payload(self):
        print("Testing get_AIS_Payload")
        diction, mydata = self.initialise()

        mydata.set_AIS_Payload(self.mytestdata[0].split(',')[5])
        out = mydata.get_AIS_Payload()
        self.assertEqual(self.mytestdata[0].split(',')[5], out, "Failed in test get_AIS_Payload")

    def test_set_AIS_payload(self):
        print("Testing set AIS_Payload")
        diction, mydata = self.initialise()

        mydata.set_AIS_Payload(self.mytestdata[0].split(',')[5])
        out = mydata.get_AIS_Payload()
        self.assertEqual(self.mytestdata[0].split(',')[5], out, "Failed in test set_AIS_Payload")

    def test_set_AIS_Binary_Payload(self):
        print("Testing set AIS_Binary_Payload")
        diction, mydata = self.initialise()
        fakestream: str = '00010000'
        faketail: str = '11111111111111111111'
        fakebinary = ''
        fakebinary = '00010000'
        # print('sending ', fakebinary)
        mydata.set_AIS_Binary_Payload(fakebinary)
        out = mydata.get_AIS_Binary_Payload()
        self.assertEqual(fakebinary, out, "Failed in test set_AIS_Binary_Payload")

    def test_get_AIS_Binary_Payload(self):
        print("Testing get_AIS_Binary_Payload")
        diction, mydata = self.initialise()
        fakestream: str = '00010000'
        faketail: str = '11111111111111111111'
        thefake = '00010000' + '11111111111111111111' + '00010000'

        # print('sending ', thefake)

        mydata.set_AIS_Binary_Payload(thefake)
        mydata.set_AIS_Binary_Payload_length(len(thefake))
        out = mydata.get_AIS_Binary_Payload()
        self.assertEqual(thefake, out, "Failed in test get_AIS_Binary_Payload")

    def test_get_AIS_Binary_Payload_length(self):
        print("Testing get_AIS_Binary_Payload_Length")
        diction, mydata = self.initialise()
        mydata.set_AIS_Binary_Payload_length(160)
        out = mydata.get_AIS_Binary_Payload_length()
        self.assertEqual(160, out, "Failed in test get_AIS_Binary_Payload")

    def test_set_AIS_Binary_Payload_length(self):
        print("Testing set_AIS_Binary_Payload_length")
        diction, mydata = self.initialise()
        mydata.set_AIS_Binary_Payload_length(160)
        out = mydata.get_AIS_Binary_Payload_length()
        self.assertEqual(160, out, "Failed in test get_AIS_Binary_Payload")

    def test_set_AIS_Payload_ID(self):
        print("Testing set_AIS_Payload_ID")
        diction, mydata = self.initialise()
        for intid in range(0, 28):
            try:
                mydata.set_AIS_Payload_ID(intid)
                intout = mydata.get_AIS_Payload_ID()
                self.assertEqual(intid, intout, "Failed in test get_AIS_Binary_ID")
            except ValueError:
                pass

    def test_get_AIS_Payload_ID(self):
        print("Testing get_AIS_Payload_ID")
        diction, mydata = self.initialise()
        mydata.set_AIS_Payload_ID(1)
        intout = mydata.get_AIS_Payload_ID()
        self.assertEqual(1, intout, "Failed in test get_AIS_Payload_ID")

    def test_set_fragment(self):
        print("Testing set_fragment")
        diction, mydata = self.initialise()
        mydata.set_fragment(2)
        intout = mydata.get_fragment()
        self.assertEqual(2, intout, "Failed in test set_fragment")

    def test_set_fragno(self):
        # work to be done strange unexpected argument when defding set_fragno in AIS_Data
        pass

    def test_set_channel(self):
        diction, mydata = self.initialise()
        print('Testing set channel')

        for char in ['A', 'B', '1', '2', '3']:
            try:
                mydata.set_channel(char)
                out = mydata.get_channel()
                if char == '1':
                    char = 'A'
                elif char == '2':
                    char = 'B'
                self.assertEqual(char, out, "Failed in set channel")
            except ValueError:
                # if channel nuber == 3 invalid
                pass

    def test_get_channel(self):
        diction, mydata = self.initialise()
        print('Testing get channel')
        mydata.set_channel("A")
        out = mydata.get_channel()
        self.assertEqual("A", out, "Failed in set channel")

    def test_do_function(self):
        pass

    def test_set_repeat_indicator(self):
        print('Testing set assigned')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_RepeatIndicator(tpl)
                out = mydata.get_Assigned()
                self.assertEqual(tpl, out, "Failedc in get/set assigned")
            except ValueError:
                pass

    def test_get_sog(self):
        print("Testing get SOG")
        diction, mydata = self.initialise()
        mydata.set_SOG(100)
        out: float = mydata.get_SOG()
        self.assertEqual(10.0, out, "Failed in get_SOG")

    def test_set_sog(self):
        print("Testing get SOG")
        diction, mydata = self.initialise()
        for _ in range(10):
            ispd = random.randint(0, 1000)
            mydata.set_SOG(ispd)
            out: float = mydata.get_SOG()
            self.assertEqual(float(ispd / 10), out, "Failed in set_SOG")

    def test_get_int_hdg(self):
        print("Testing set int_hdg")
        diction, mydata = self.initialise()
        ispd = random.randint(0, 359)
        mydata.set_int_HDG(ispd)
        out: float = mydata.get_int_HDG()
        self.assertEqual(ispd, out, "Failed in set_SOG")

    def test_set_int_hdg(self):
        print("Testing set int_hdg")
        diction, mydata = self.initialise()
        for _ in range(10):
            ispd = random.randint(0, 359)
            mydata.set_int_HDG(ispd)
            out: float = mydata.get_int_HDG()
            self.assertEqual(ispd, out, "Failed in set_SOG")

    def test_rot(self):
        # WIP not certain where the actual ROT is calculated yet
        pass

    def test_get_altitude(self):
        print("Testing get altitude")
        diction, mydata = self.initialise()
        ispd = 1000
        mydata.set_Altitude(ispd)
        out: float = mydata.get_Altitude()
        self.assertEqual(ispd, out, "Failed in set_altitude")

    def test_set_altitude(self):
        print("Testing set altitude")
        diction, mydata = self.initialise()
        for _ in range(10):
            ispd = random.randint(0, 4095)
            mydata.set_Altitude(ispd)
            out: float = mydata.get_Altitude()
            self.assertEqual(ispd, out, "Failed in set_altitude")

    def test_get_int_rot(self):
        # WIP not certain where the actual ROT is calculated yet
        pass

    def test_set_int_rot(self):
        # WIP not certain where the actual ROT is calculated yet
        pass

    def test_get_nav_status(self):
        print("Testing get nav status")
        diction, mydata = self.initialise()

        mydata.set_NavStatus(10)
        out: float = mydata.get_NavStatus()
        self.assertEqual(10, out, "Failed in set_Navstatus")

    def test_set_nav_status(self):
        print("Testing set nav status")
        diction, mydata = self.initialise()
        for ispd in range(1, 16):
            try:
                mydata.set_NavStatus(ispd)
                out: float = mydata.get_NavStatus()
                self.assertEqual(ispd, out, "Failed in set_Navstatus")
            except ValueError:
                pass

    def test_set_int_latitude(self):
        print("Testing set int latitude")
        diction, mydata = self.initialise()
        ilat = 60000000
        mydata.set_int_latitude(ilat)
        outi = mydata.get_int_latitude()
        outf = mydata.get_Latitude()
        self.assertEqual(ilat, outi, "Failed in set int latitude")
        self.assertEqual(10.0, outf, "Failed in getting floting point latitude")

    def test_set_int_longitude(self):
        print("Testing set int longitude")
        diction, mydata = self.initialise()
        print("Testing set int latitude")
        diction, mydata = self.initialise()
        ilat = 60000000
        mydata.set_int_longitude(ilat)
        outi = mydata.get_int_longitude()
        outf = mydata.get_Longitude()
        self.assertEqual(ilat, outi, "Failed in set int longitude")
        self.assertEqual(10.0, outf, "Failed in getting floating point longitude")

    def test_set_pos_accuracy(self):
        diction, mydata = self.initialise()
        print("Testing set/get Pos Accuracy")

        mydata.set_Pos_Accuracy(value=1)
        self.assertEqual(1, mydata.get_Pos_Accuracy(), 'Failed in get/set pos accuracy')
        mydata.set_Pos_Accuracy(value=0)
        self.assertEqual(0, mydata.get_Pos_Accuracy(), 'Failed in get/set pos accuracy')

    def test_set_cog(self):
        diction, mydata = self.initialise()
        print("Test set COG")
        for _ in range(100):
            ispd = random.randint(0, 3600)
            mydata.set_COG(ispd)
            out: float = mydata.get_COG()
            self.assertEqual(float(ispd / 10), out, "Failed in set_COG")
            self.assertEqual(int(ispd / 10), mydata.get_int_COG(), "Failed in get_int_COG")

    def test_set_hdg(self):
        diction, mydata = self.initialise()
        print("Test set HDG")
        for _ in range(100):
            ispd = random.randint(0, 359)
            mydata.set_HDG(ispd)
            out: int = mydata.get_HDG()
            self.assertEqual(ispd, out, "Failed in set_HDG")

    def test_set_timestamp(self):
        print('Testing set timestamp')
        diction, mydata = self.initialise()
        for _ in range(100):
            utc = random.randint(0, 64)
            try:
                mydata.set_Timestamp(utc)
                self.assertEqual(utc, mydata.get_Timestamp(), "Failed in get/set timestamp")
            except ValueError:
                pass

    def test_set_man_indicator(self):
        print('Testing set manouver indicator')
        diction, mydata = self.initialise()
        for i in range(0, 3):
            try:
                mydata.set_MAN_Indicator(i)
                self.assertEqual(i, mydata.get_MAN_Indicator(), "Failed in get/set manouver indicator")
            except ValueError:
                pass

    def test_set_raim(self):
        print('Testing set RAIM')
        diction, mydata = self.initialise()
        for i in range(0, 2):
            try:
                mydata.set_RAIM(i)
                self.assertEqual(i, mydata.get_RAIM(), "Failed in get/set manouver indicator")
            except ValueError:
                pass

    def test_set_name(self):
        print('Testing set Vessel Name')
        diction, mydata = self.initialise()
        for cs in ['cg22', 'CG22', 'ABCDE765@@', 'ABC765 @']:
            result = ''
            try:
                mydata.set_Name(cs)

                for i in cs:
                    if not (i == '@' or i == ' '):
                        result = result + i
                self.assertEqual(result, mydata.get_Name(), "Failed in get/set Vessel Name")
            except ValueError:
                pass

    def test_set_callsign(self):
        print('Testing set callsign')
        diction, mydata = self.initialise()
        for cs in ['cg22', 'CG22', 'ABCDE765@@', 'ABC765 @']:
            result = ''
            try:
                mydata.set_Callsign(cs)

                for i in cs:
                    if not (i == '@' or i == ' '):
                        result = result + i
                self.assertEqual(result, mydata.get_Callsign(), "Failed in get/set Callsign")
            except ValueError:
                pass

    def test_set_imo(self):
        print('Testing set IMO')
        diction, mydata = self.initialise()
        for _ in range(1000):
            i = random.randint(0, 9999999)
            try:
                mydata.set_IMO(i)
                self.assertEqual(i, mydata.get_IMO(), "Failed in get/set manouver indicator")
            except ValueError:
                pass
        try:
            mydata.set_IMO(11111111)
            self.fail()
        except ValueError:
            pass

    def test_set_version(self):
        print('Testing set AIS Vesion')
        diction, mydata = self.initialise()
        for i in range(0, 4):
            try:
                mydata.set_Version(i)
                self.assertEqual(i, mydata.get_Version(), "Failed in get/set AIS Version")
            except ValueError:
                pass

    def test_set_destination(self):
        print('Testing set Desination')
        diction, mydata = self.initialise()
        for cs in ['cg22', 'CG22', 'ABCDE765@@', 'ABC765 @']:
            result = ''
            try:
                mydata.set_Name(cs)

                for i in cs:
                    if not (i == '@' or i == ' '):
                        result = result + i
                self.assertEqual(result, mydata.get_Name(), "Failed in get/set Destination")
            except ValueError:
                pass

    def test_set_display(self):
        print('Testing setdisplay')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_Display(tpl)
                out = mydata.get_Display()
                self.assertEqual(tpl, out, "Failedc in get/set Display")
            except ValueError:
                pass

    def test_set_dsc(self):
        print('Testing set DSC')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_DSC(tpl)
                out = mydata.get_DSC()
                self.assertEqual(tpl, out, "Failedc in get/set DSC")
            except ValueError:
                pass

    def test_set_band(self) -> None:
        print('Testing set band flag')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_BAND(tpl)
                out = mydata.get_BAND()
                self.assertEqual(tpl, out, "Failedc in get/set Band Flag")
            except ValueError:
                pass

    def test_set_message22(self):
        print('Testing set bmessage22 flag')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_Message22(tpl)
                out = mydata.get_Message22()
                self.assertEqual(tpl, out, "Failedc in get/set Message22 Flag")
            except ValueError:
                pass

    def test_set_assigned(self):
        print('Testing set assigned')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_Assigned(tpl)
                out = mydata.get_Assigned()
                self.assertEqual(tpl, out, "Failedc in get/set assigned")
            except ValueError:
                pass

    def test_set_ship_type(self):
        print('Testing set Ship Type')
        diction, mydata = self.initialise()
        for _ in range(100):
            i = random.randint(0, 101)
            try:
                mydata.set_ShipType(i)
                if i > 99:
                    i = 0
                self.assertEqual(i, mydata.get_ShipType(), "Failed in get/set Ship Type")
            except ValueError:
                pass

    def test_set_dim2bow(self):
        print('Testing set Dim to Bow')
        diction, mydata = self.initialise()
        for _ in range(100):
            i = random.randint(1, 1023)
            try:
                mydata.set_Dim2Bow(i)
                self.assertEqual(i, mydata.get_Dim2Bow(), "Failed in get/set Dimm to Bow")
            except ValueError:
                pass

    def test_set_dim2stern(self):
        print('Testing set Dim to Stern')
        diction, mydata = self.initialise()
        for _ in range(100):
            i = random.randint(1, 1023)
            try:
                mydata.set_Dim2Stern(i)
                self.assertEqual(i, mydata.get_Dim2Stern(), "Failed in get/set Dim to Stern")
            except ValueError:
                pass

    def test_set_dim2port(self):
        print('Testing set Dim to Portr')
        diction, mydata = self.initialise()
        for _ in range(100):
            i = random.randint(1, 63)
            try:
                mydata.set_Dim2Port(i)
                self.assertEqual(i, mydata.get_Dim2Port(), "Failed in get/set Dim to Port")
            except ValueError:
                pass

    def test_set_dim2starboard(self):
        print('Testing set Dim to Starboard')
        diction, mydata = self.initialise()
        for _ in range(100):
            i = random.randint(1, 63)
            try:
                mydata.set_Dim2Starboard(i)
                self.assertEqual(i, mydata.get_Dim2Starboard(), "Failed in get/set Dim to Starboard")
            except ValueError:
                pass

    def test_set_fix_type(self):
        print('Testing set EPFD Fix Type')
        # range 0-8 valid, 15 often appears as undefined, 9-14 shouldn't happen
        diction, mydata = self.initialise()
        for _ in range(20):
            i = random.randint(0, 15)

            try:
                mydata.set_FixType(i)
                if 9 <= i <= 14:
                    i = 15
                self.assertEqual(i, mydata.get_FixType(), "Failed in get/set fix type")
            except ValueError:
                pass

    def test_set_eta_month(self):
        print('Testing set ETA Month')
        diction, mydata = self.initialise()
        for _ in range(20):
            i = random.randint(0, 12)
            try:
                mydata.set_ETA_Month(i)
                self.assertEqual(i, mydata.get_ETA_Month(), "Failed in get/set ETA Month")
            except ValueError:
                pass

    def test_set_eta_day(self):
        print('Testing set ETA Day')
        diction, mydata = self.initialise()
        for _ in range(50):
            i = random.randint(0, 31)
            try:
                mydata.set_ETA_Day(i)
                self.assertEqual(i, mydata.get_ETA_Day(), "Failed in get/set ETA Dasy")
            except ValueError:
                pass

    def test_set_eta_hour(self):
        print('Testing set ETA Hour')
        diction, mydata = self.initialise()
        for _ in range(50):
            i = random.randint(0, 24)
            try:
                mydata.set_ETA_Hour(i)
                self.assertEqual(i, mydata.get_ETA_Hour(), "Failed in get/set ETA Hour")
            except ValueError:
                pass

    def test_set_eta_minute(self):
        print('Testing set ETA Minute')
        diction, mydata = self.initialise()
        for _ in range(50):
            i = random.randint(0, 60)
            try:
                mydata.set_ETA_Minute(i)
                self.assertEqual(i, mydata.get_ETA_Minute(), "Failed in get/set ETA Minute")
            except ValueError:
                pass

    def test_set_draught(self):
        print('Testing set Draught')
        diction, mydata = self.initialise()
        for _ in range(50):
            i = random.randint(0, 512)
            try:
                mydata.set_Draught(i)
                self.assertEqual(i, mydata.get_Draught(), "Failed in get/set Draughjt")
            except ValueError:
                pass

    def test_set_dte(self):
        print('Testing set DTE')
        diction, mydata = self.initialise()
        testitems = [0, 1, 3]
        for tpl in testitems:
            try:
                mydata.set_DTE(tpl)
                out = mydata.get_DTE()
                self.assertEqual(tpl, out, "Failedc in get/set DTE")
            except ValueError:
                pass

    def test_get_radio_status(self):
        diction, mydata = self.initialise()
        self.assertEqual("Radio Status Unavailable", mydata.get_Radio_Status(), "Failed in get Radio Status")

    def test_Radio_status(self):
        diction, mydata = self.initialise()
        try:
            mydata.Radio_Status()
            self.assertEqual(1, 2, "Radio Status does not raise an error")
        except NameError:
            pass

    def test_type24part_no(self):
        # if p_payload_ID is 24 then extract bits 38-39 and return integer value
        # valid values are 0 or 1, if called with non-valid payload type returns -1
        # throws exception if data stream returns 2 or 3
        print('Testing Type24parttno')
        diction, mydata = self.initialise()
        falsehead = '00000000000000000000000000000000000000'

        # test for 0, 1 2, 3
        testitems = [('00', 0), ('01', 1), ('10', 2), ('11', 3)]
        for tpl in testitems:
            teststream = falsehead + tpl[0] + falsehead
            mydata.set_AIS_Binary_Payload_length(len(teststream))
            mydata.set_AIS_Binary_Payload(teststream)
            mydata.set_AIS_Payload_ID(24)
            try:
                out = mydata.Type24PartNo()
                self.assertEqual(tpl[1], out, "Failedc in Type24PartNo")
            except ValueError:
                pass

        try:
            mydata.set_isAVCGA(3)
        except ValueError:
            pass

    def test_set_safety_text(self):
        print('Testing set Safety Text')
        diction, mydata = self.initialise()
        mydata.set_SafetyText('asdfghjkl')
        self.assertEqual('asdfghjkl', mydata.get_SafetyText(), "Failed in get/set Safety Text")
        try:
            mydata.set_SafetyText(1)
            self.assertEqual(1, 0, "Failed in get set Safety text accepted non string")
        except TypeError:
            pass

    def test_set_is_avcga(self):
        print('Testing set isAVCGA')
        diction, mydata = self.initialise()
        mydata.set_isAVCGA(1)
        self.assertEqual(1, mydata.get_isAVCGA(), "Failed in get/set isAVCGA")
        mydata.set_isAVCGA(0)
        self.assertEqual(0, mydata.get_isAVCGA(), "Failed in get/set isAVCGA")
        try:
            mydata.set_isAVCGA(3)
        except ValueError:
            pass

    def main(self):
        pass

    if __name__ == "main":
        main()
