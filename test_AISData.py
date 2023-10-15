from unittest import TestCase
from AISData import AIS_Data
from AISDictionary import AISDictionaries
import logging
import random


class TestAIS_Data(TestCase):
    # function used to initialise tests. sets up access to AIS_Data and Dictionary

    mytestdata = [
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
        mydata = AIS_Data(
            "!AIVDM", "1", "1", "", "A",
            "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n"
        )
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
        print("Succeeded")

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
            for char in payload[5]:
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, char)

            self.assertEqual(self.testpay, self.binpay, "Create binary payload failure")

        print('Succeeded')

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

            logging.debug("character version of bytearray\n", self.ostring)
            testpay = payload[5]
            for ij in range(len(testpay)):
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, testpay[ij])

            # the create bytearray by default pads with 0's to byte boundary.
            # to match the expected string needs to be padded as well
            while len(self.testpay) % 24 != 0:
                self.testpay = self.testpay + "0"

            self.assertEqual(self.testpay, self.ostring, "Create bytearray payload failure")

        print('Succeeded')

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

        print('succeeded')

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
        print("Succeeded")

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

        testtext: str = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvw01234567890:;<>=?@@'

        for _ in range(10):

            for ik in range(len(testtext) - 1):
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

            logging.debug("DEBUG binary_payload from which string will be extracted\n",
                          mydata.get_AIS_Binary_Payload())

            outstr = mydata.ExtractString(startpos, rndlen * 6)
            logging.debug('Extracted string ', outstr)

            self.assertEqual(rndtext, outstr, "Failed in Extract_String")

        ##### Error still exists last character in string if @ returns as w

        print("Succeeded")

    def test_print_ais(self):
        self.fail()

    def test_m_initialise(self):
        print("Testing m_initialise")
        self.fail()

    def test_m_setup(self):
        print("Testing m_setup")
        self.fail()

    def test_remove_at(self):
        self.fail()

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
        self.fail()

    def test_get_ais_frag_count(self):
        self.fail()

    def test_get_ais_frag_no(self):
        self.fail()

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

    def test_get_repeat_indicator(self):
        self.fail()

    def test_set_repeat_indicator(self):
        self.fail()

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
        self.assertEqual(ilat, mydata.get_int_latitude(), "Failed in set int latitude")
        self.assertEqual(10.0, mydata.get_Latitude, "Failed in getting floting point latitude")

    def test_get_int_latitude(self):
        self.fail()

    def test_set_int_longitude(self):
        print("Testing set int longitude")
        diction, mydata = self.initialise()
        print("Testing set int latitude")
        diction, mydata = self.initialise()
        ilat = 60000000
        mydata.set_int_longitude(ilat)
        self.assertEqual(ilat, mydata.get_int_latitude(), "Failed in set int longitude")
        self.assertEqual(10.0, mydata.get_Longitude(), "Failed in getting floting point longitude")

    def test_set_pos_accuracy(self):
        diction, mydata = self.initialise()
        print("Testing set/get Pos Accuracy")

        mydata.set_Pos_Accuracy(0)
        self.assertEqual(1, mydata.get_Pos_Accuracy, 'Failed in get/set pos accuyracy')
        mydata.set_Pos_Accuracy(0)
        self.assertEqual(0, mydata.get_Pos_Accuracy, 'Failed in get/set pos accuyracy')

    def test_get_cog(self):
        self.fail()

    def test_set_cog(self):
        self.fail()

    def test_set_int_cog(self):
        self.fail()

    def test_get_int_cog(self):
        self.fail()

    def test_get_hdg(self):
        self.fail()

    def test_set_hdg(self):
        self.fail()

    def test_get_timestamp(self):
        self.fail()

    def test_set_timestamp(self):
        self.fail()

    def test_get_man_indicator(self):
        self.fail()

    def test_set_man_indicator(self):
        self.fail()

    def test_get_raim(self):
        self.fail()

    def test_set_raim(self):
        self.fail()

    def test_get_name(self):
        self.fail()

    def test_set_name(self):
        self.fail()

    def test_get_callsign(self):
        self.fail()

    def test_set_callsign(self):
        self.fail()

    def test_get_imo(self):
        self.fail()

    def test_set_imo(self):
        self.fail()

    def test_get_version(self):
        self.fail()

    def test_set_version(self):
        self.fail()

    def test_get_destination(self):
        self.fail()

    def test_set_destination(self):
        self.fail()

    def test_get_display(self):
        self.fail()

    def test_set_display(self):
        self.fail()

    def test_get_dsc(self):
        self.fail()

    def test_set_dsc(self):
        self.fail()

    def test_get_band(self):
        self.fail()

    def test_set_band(self):
        self.fail()

    def test_get_message22(self):
        self.fail()

    def test_set_message22(self):
        self.fail()

    def test_get_assigned(self):
        self.fail()

    def test_set_assigned(self):
        self.fail()

    def test_get_ship_type(self):
        self.fail()

    def test_set_ship_type(self):
        self.fail()

    def test_get_dim2bow(self):
        self.fail()

    def test_set_dim2bow(self):
        self.fail()

    def test_get_dim2stern(self):
        self.fail()

    def test_set_dim2stern(self):
        self.fail()

    def test_get_dim2port(self):
        self.fail()

    def test_set_dim2port(self):
        self.fail()

    def test_get_dim2starboard(self):
        self.fail()

    def test_set_dim2starboard(self):
        self.fail()

    def test_get_fix_type(self):
        self.fail()

    def test_set_fix_type(self):
        self.fail()

    def test_get_eta_month(self):
        self.fail()

    def test_set_eta_month(self):
        self.fail()

    def test_get_eta_day(self):
        self.fail()

    def test_set_eta_day(self):
        self.fail()

    def test_get_eta_hour(self):
        self.fail()

    def test_set_eta_hour(self):
        self.fail()

    def test_get_eta_minute(self):
        self.fail()

    def test_set_eta_minute(self):
        self.fail()

    def test_get_draught(self):
        self.fail()

    def test_set_draught(self):
        self.fail()

    def test_get_dte(self):
        self.fail()

    def test_set_dte(self):
        self.fail()

    def test_radio_status(self):
        self.fail()

    def test_type24part_no(self):
        self.fail()

    def test_get_safety_text(self):
        self.fail()

    def test_set_safety_text(self):
        self.fail()

    def test_get_is_avcga(self):
        self.fail()

    def test_set_is_avcga(self):
        self.fail()

    def test_set_rad_status(self):
        self.fail()

    def test_get_rad_status(self):
        self.fail()

    def main(self):
        pass

    if __name__ == "main":
        main()
