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
        dict = AISDictionaries()
        print('Testing create_binary_payload')
        for i in range(len(self.mytestdata) - 1):
            self.testpay: str = ''
            payload = self.mytestdata[i].split(',')
            self.binpay, self.binlen = AIS_Data.create_binary_payload(payload[5])
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
        diction, mydata = self.initialise()
        mydata.set_Encoded_String(self.mytestdata[0].split(',')[5])
        out = mydata.get_Encoded_String()
        self.assertEqual(self.mytestdata[0].split(',')[5], out)

    def test_get_Encoded_String(self):
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
        self.fail()

    def test_get_ais_channel(self):
        self.fail()

    def test_get_ais_payload(self):
        self.fail()

    def test_set_ais_binary_payload(self):
        self.fail()

    def test_get_ais_binary_payload_length(self):
        self.fail()

    def test_set_ais_binary_payload_length(self):
        self.fail()

    def test_set_ais_payload_id(self):
        self.fail()

    def test_get_ais_payload_id(self):
        self.fail()

    def test_set_fragment(self):
        self.fail()

    def test_set_fragno(self):
        self.fail()

    def test_set_messid(self):
        self.fail()

    def test_set_channel(self):
        self.fail()

    def test_set_payload(self):
        self.fail()

    def test_set_trailer(self):
        self.fail()

    def test_get_mmsi(self):
        self.fail()

    def test_set_mmsi(self):
        self.fail()

    def test_get_string_mmsi(self):
        self.fail()

    def test_set_talker(self):
        self.fail()

    def test_do_function(self):
        pass

    def test_get_repeat_indicator(self):
        self.fail()

    def test_set_repeat_indicator(self):
        self.fail()

    def test_get_sog(self):
        self.fail()

    def test_set_sog(self):
        self.fail()

    def test_get_int_hdg(self):
        self.fail()

    def test_set_int_hdg(self):
        self.fail()

    def test_rot(self):
        self.fail()

    def test_get_altitude(self):
        self.fail()

    def test_set_altitude(self):
        self.fail()

    def test_get_int_rot(self):
        self.fail()

    def test_set_int_rot(self):
        self.fail()

    def test_get_nav_status(self):
        self.fail()

    def test_set_nav_status(self):
        self.fail()

    def test_set_int_latitude(self):
        self.fail()

    def test_get_int_latitude(self):
        self.fail()

    def test_set_int_longitude(self):
        self.fail()

    def test_get_int_longitude(self):
        self.fail()

    def test_get_latitude(self):
        self.fail()

    def test_get_longitude(self):
        self.fail()

    def test_get_pos_accuracy(self):
        self.fail()

    def test_set_pos_accuracy(self):
        self.fail()

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
    self.test_create_binary_payload()
    self.test_create_bytearray_payload()
    pass


if __name__ == "main":
    main()
