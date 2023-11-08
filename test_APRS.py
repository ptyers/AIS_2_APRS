from unittest import TestCase

import Payloads
from AISDictionary import AISDictionaries
from APRS import APRS
from Payloads import AISStream, Fragments

class Test(TestCase):
    def test_send_aprs(self):
        self.fail()

    def test_doposition(self):
        self.fail()

    def test_do4(self):
        self.fail()

    def test_do14(self):
        self.fail()

    def test_do5_24(self):
        self.fail()

    def test_queue_aprs(self):
        self.fail()

    def test_do_diag_print(self):
        self.fail()

    def test_transmit_aprs(self):
        self.fail()

    def test_define_server_address(self):
        self.fail()

    def test_do_print_server_address(self):
        self.fail()

    def test_do_log_aprs(self):
        self.fail()


class TestAPRS(TestCase):

    def initialise(self):
        diction = AISDictionaries()
        # the ais stream used here is only a place filler.
        mystream = AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100h3c,0*6B')

        return diction, mystream

    def test_get_course(self):
        self.fail()

    def test_set_course(self):
        self.fail()

    def test_get_speed(self):
        self.fail()

    def test_set_speed(self):
        self.fail()

    def test_get_name(self):
        self.fail()

    def test_set_name(self):
        self.fail()

    def test_get_callsign(self):
        self.fail()

    def test_set_callsign(self):
        self.fail()

    def test_get_mmsi(self):
        self.fail()

    def test_set_mmsi(self):
        self.fail()

    def test_convert_longitude(self):
        self.fail()

    def test_split_longitude(self):
        self.fail()

    def test_convert_latitude(self):
        self.fail()

    def test_split_latitude(self):
        self.fail()

    def test_convert_speed(self):
        self.fail()

    def test_create_object_position(self):
        '''
        Types 1, 2, 3, 4, 9, 18, 19, 21, 27 all use this routine
        set up dummy aisstring for each type and pass to create_object_position


        :return:
        '''
        diction, mystream = self.initialise()
        # one for each type
        # generic parameters
        '''
        Input Fragment Count = 1
        What is Message_ID default null = 
        What channel ID = A
        Input Payload Type (Numeric 1-27 = will change
        Enter MMSI - 9 digits, default 503123456 = 
        Enter Navigatiobn Status range 0-15 default 15 7
        Enter Rate Of Turn 0-128, 128 default = 63
        Enter Speed over ground range 0-102 knots default 102.2 = 30.0
        Enter longitude decimal +ve West, -ve East = -147.5
        longitude  -147.5
        Enter latitude decimal +ve North, -ve South = -38.4
        Enter course over ground range 0-359 default 360 = 122
        True heading range 0-259 default 360 = 127
        '''
        testais1 = '!AIVDM,1,1,,A,17Ol>07?ldELk71b1h04i3v00000,0*5'
        testais2 = '!AIVDM,1,1,,A,27Ol>07?ldELk71b1h04i3v00000,0*5'
        testais3 = '!AIVDM,1,1,,A,37Ol>07?ldELk71b1h04i3v00000,0*5'
        '''
        Enter UTC Year 4 digits - default 0 - Not Available2023
        Enter UTC Month 2 digits - default 0 - Not Available11
        Enter UTC Day 2 digits - default 0 - Not Available08
        Enter UTC Hour 2 digits - default 24 - Not Available17
        Enter UTC Minute 2 digits - default 60 - Not Available58
        Enter UTC Second 2 digits - default 60 - Not Available0
        Input Fix Quality 0/1 - default = 0 
        '''
        testais4 = '!AIVDM,1,1,,A,47Ol>01vNl8rtELk71b1h0000000,0*5'
        '''
        Enter Altitude - max 4095 1045
        Enter Speed Over Ground max 1022 300
        Enter Assigned Flag 0/1 0
        '''
        testais9 = '!AIVDM,1,1,,A,97Ol>045DdELk71b1h00NP000000,0*5'
        testais18 = '!AIVDM,1,1,,A,B7Ol>001;5G<ihJPL01<@wP00000,0*5'
        '''
        Enter Vessel Name 20 chars upper caseTEST VESSEL
        Enter Ship Type - 0-99, default 0 37
        Enter Dimension to Bow - max 511, default 0 50
        Enter Dimension to Stern - max 511, default 047
        Enter Dimension to Port - max 511, default 012
        Enter Dimension to Starboard - max 511, default 013
        Enter EPFD Type range 0-8 default 0 (undefined) 3
        '''
        testais19 = '!AIVDM,1,1,,A,C7Ol>001;5G<ihJPL01<@wP0`:Va0d:VV:H000000000BS8GV6P0,0*5'
        '''
        Enter Aid Type 0-31 numeric 6
        Enter Vessel Name 20 chars upper caseTEST AID
        Enter Extended Vessel Name 15 chars upper caseNO EXTENSION
        '''
        testais21 = '!AIVDM,1,1,,A,E7Ol>03:2ab@0TR000000000000:fISPm0p00j5qQ`0003Sp1F51CTjCkP000,0*5'
        '''
        Enter Navigation Status range 0-15 default 15 2
        '''
        testais27 = '!AIVDM,1,1,,A,K7Ol>00bVC=<0?7`,0*5'

        # now the guts of the tests






        self.fail('Not fully implemented')

    def prepare_position(self):
        # allows setting up of conditions to pass data to create_position
        pass
    def test_create_base_position(self):
        self.fail()

    def test_create_safety_message(self):
        '''
        Test will involve setting up test aisstreams of type 12 and 14 and passing to the function
        Validation will be if message generated has the correct format

        correct format will be of form for TYpe 12
            {APRS._relay_station}>APU25N,TCPIP*:{self.destination_mmsi}:{self.safetytext}\n')
            where
                {APRS._relay_station} is the identity of this system - 9 characters
                {self.destination_mmsi)} is the destination mmsi pecified in Type 12 Addressed message
                    max 9 char filled to the right
                {self.safetytext} is the safety text passed in from the AIS interpretation system as an attribute
                    of type 12 AIS packet blocked if necessary into 67 byte chunks


        correct format will be of form for TYpe 14
            {APRS._relay_station}>APU25N,TCPIP*::BLN{str(Bulletin)}_____:{self.safetytext}\n')
            where
                {APRS._relay_station} is the identity of this system - 9 characters
                {str(Bulletin)} is a single digit modulo 10
                {self.safetytext} is the safety text passed in from the AIS interpretation system as an attribute
                    of type 14 AIS packet blocked if necessary into 67 byte chunks
                _____ are mandatory spaces


        :return:
        '''
        diction, mystream = self.initialise()

        # first a Type 14 broadcast message with less than 67 chrs
        testais = '!AIVDM,1,1,,A,>7Ol>01@PU>0U>061@E=B1<4HEAV0lE=<4LD000000000000000000000,0*5'
        message = self.prepare_safety(14,testais)
        expected = 'CG722>APU25N,TCPIP*::BLN0     :THIS IS A TEST SAFETY MESSAGE\n'.upper()
        self.assertEqual(expected, message,"In testing APRS.create short type14 safety message fail")

        # now a longer thgan 67 char safety message
        testais = ('!AIVDM,1,1,,A,>7Ol>01@PU>0U>060htpN1<4HEAV0lE=<4LF0tJ05B0hD5=B37320<P585'
                   '<=@E9>337;?CGKOSW37;?CGKOSW37;?CGKOSW37;?CGKOSW337;?CGKOST,0*5')
        message = self.prepare_safety( 14, testais)
        expected = ('CG722>APU25N,TCPIP*::BLN0     :THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS '
                    '01234567\nCG722>APU25N,TCPIP*::BLN1     :8901234567890123456789012345678900123456789\n')
        self.assertEqual(expected, message, "In testing APRS.create long type14 safety message fail")


        # now for Type 12 Addressed Safety Message
        # first a short message

        testais = '!AIVDM,1,1,,A,<7Ol>01ou3P0D89CP9CP1PC8?BDP144B5CC54PC165DIPD5HD0000000000000,0*5'
        message= message = self.prepare_safety(12, testais)
        expected = 'CG722>APU25N,TCPIP*:503123456:THIS IS A SHORT ADDRESSED SAFETY TEXT\n'
        self.assertEqual(expected, message, "In testing APRS.create short type12 addressed safety message fail")
        # now a long (to be split) message
        # 'THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS 012345678901234567890123456789012345678900123456789')'
        testais = ('!AIVDM,1,1,,A,<7Ol>01ou3P0D89CP9CP1P<?>7PC165DIP=5CC175P?6P1DP<51CDPihh'
                   'P381B1C3D5BCPhijklmnopqhijklmnopqhijklmnopqhijklmnopqhhijklmnopq,0*5')
        message = message = self.prepare_safety(12, testais)
        expected = ('CG722>APU25N,TCPIP*:503123456:THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS 01234567\n'
                    'CG722>APU25N,TCPIP*:503123456:8901234567890123456789012345678900123456789\n')
        self.assertEqual(expected, message, "In testing APRS.create long type12 addressed safety message fail")


    def prepare_safety(self,message_type: int, testais: str):
        mystream = AISStream(testais)
        if message_type == 14:
            mydata = Payloads.Safety_related_broadcast_message(mystream.binary_payload)
        elif message_type == 12:
            mydata = Payloads.Addressed_safety_related_message(mystream.binary_payload)

        myaprs = APRS(mydata.mmsi, 0.0, 0.0, 0.0, 0.0, 'SAFETY', 0)

        message = myaprs.CreateSafetyMessage(0, mydata)

        return message




