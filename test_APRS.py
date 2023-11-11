from unittest import TestCase
from datetime import datetime
import os

import Payloads
from AISDictionary import AISDictionaries
from APRS import APRS, doposition, dobase, dosafety, datareport, define_server_address, do_log_aprs, do_print_server_address
from APRS import SendAPRS, QueueAPRS, TransmitAPRS
from Payloads import AISStream, Fragments, CNB, SAR_aircraft_position_report, ClassB_position_report
from Payloads import Extende_ClassB_position_report, Long_range_AIS_broadcast_message, Basestation
from Payloads import Aid_to_navigation_report, Safety_related_broadcast_message, StaticData, Static_data_report
from MyPreConfigs import MyPreConfigs
import GlobalDefinitions
from teststreams import TestStreams

from Map import Map, MapItem


class Test(TestCase):
    def initialise(self):
        diction = AISDictionaries()
        # the ais stream used here is only a place filler.
        mystream = AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100h3c,0*6B')

        return diction, mystream

    def test_send_aprs(self):
        # SendAPRS(p, mydata, kill: bool, Bulletin: int, test: bool = False):
        # pass a series of aisstreams of all types to sendAPRS with test boolean set
        # examine the returned statuses

        # create a series of tuples (ais_stream, expected response)
        print('Testing SendAPRS')

        teststream = TestStreams()

        # now the guts of it

        for type in [1,4,5,9,12,14,18,19,21,24, 27]:
            thestream = teststream.teststream[type]
            myais = AISStream(thestream[0])
            if myais.message_type == 1:
                mydata = CNB(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0,  True)
                self.assertEqual(teststream.teststream[1][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[1][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[1][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 4:
                mydata = Basestation(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[4][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[4][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[4][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 5:
                mydata = StaticData(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[5][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[5][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[5][1][38:-1] + teststream.teststream[5][1][-11:-2] +'\n'
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 9:
                mydata = SAR_aircraft_position_report(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[9][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[9][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[9][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 18:
                mydata = ClassB_position_report(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[18][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[18][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[18][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 19:
                mydata = Extende_ClassB_position_report(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[19][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[19][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[19][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 21:
                mydata = Aid_to_navigation_report(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[21][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[21][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[21][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 24:
                mydata = Static_data_report(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[24][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[24][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[24][1][38:-1] + teststream.teststream[5][1][-11:-2] +'\n'
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")
            if myais.message_type == 27:
                mydata = Long_range_AIS_broadcast_message(myais.binary_payload)
                xcallsign, tcpbytes = SendAPRS(mydata.message_type, mydata, False, 0, True)
                self.assertEqual(teststream.teststream[27][2], xcallsign,
                                 "failed in preparing to queue APRS byte stream")
                expected = teststream.teststream[27][1][0:30] + '*' \
                           + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                           + teststream.teststream[27][1][38:]
                self.assertEqual(expected, tcpbytes.decode(),
                                 "failed in preparing to queue APRS byte stream")

            pass



    def test_doposition(self):
        # crude test only
        # considered to work if can successfully call doposition and get back proper tcpbyte string
        print('Testing doposition')
        teststream = TestStreams()
        testais1 = teststream.teststream[1][0]

        myais = AISStream(testais1)
        mydata = CNB(myais.binary_payload)
        myaprs = APRS(mydata.mmsi, mydata.latitude, mydata.longitude, mydata.course_over_ground,
                      mydata.speed_over_ground, mydata.callsign + mydata.vessel_name, False)

        message = doposition(mydata, myaprs, 0, False).decode("utf-8")

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        # expected = (f'CG722>APU25N,TCPIP*:;503123456*{datetime.utcnow().strftime("%d%H%Mz")}'
        #             f'3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n')

        expected = teststream.teststream[1][1][0:30] + '*' \
        + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
        + teststream.teststream[1][1][38:]



        self.assertEqual(expected, message, f"Failed in do_position with message type "
                                            f"{myais.message_type}\n input string = {testais1}")



    def test_dobase(self):
        print('Testing dobase')
        teststream = TestStreams()
        testais = teststream.teststream[4][0]


        myais = AISStream(testais)
        mydata = Basestation(myais.binary_payload)
        myaprs = APRS(mydata.mmsi, mydata.latitude, mydata.longitude, mydata.course_over_ground,
                mydata.speed_over_ground, mydata.callsign + mydata.vessel_name, False)

        message = dobase(mydata, myaprs).decode("utf-8")

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        # expected = (f'CG722>APU25N,TCPIP*:;503123456*{datetime.utcnow().strftime("%d%H%Mz")}'
        #             f'3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n')
        expected = teststream.teststream[4][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[4][1][38:]

        self.assertEqual(expected, message, f"Failed in do_position with message type "
                                            f"{myais.message_type}\n input string = {testais}")

    def test_dosafety(self):
        print('Testing dosafety')
        teststream = TestStreams()
        testais = teststream.teststream[14][0]


        myais = AISStream(testais)
        mydata = Safety_related_broadcast_message(myais.binary_payload)
        myaprs =  APRS(mydata.mmsi, 0.0, 0.0, 0.0,
                             0.0, 'SAFETY', 0)

        message = dosafety(mydata, myaprs, 0 ).decode("utf-8")

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        # expected = (f'CG722>APU25N,TCPIP*:;503123456*{datetime.utcnow().strftime("%d%H%Mz")}'
        #             f'3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n')
        expected = teststream.teststream[14][1] + '\n'

        self.assertEqual(expected, message, f"Failed in do_position with message type "
                                            f"{myais.message_type}\n input string = {testais}")

    def test_datareport(self):
        '''
        Input Fragment Count = 1
        What is Message_ID default null =
        What channel ID = A
        Input Payload Type (Numeric 1-27 = 5
        Enter MMSI - 9 digits, default 503123456 =
        Enter AIS Version - default 0 1
        Enter IMO Number - up to 7 digits - Not Available1234567
        Enter Callsign 7 charactersVN456
        Enter Vessel Name 20 charactersTEST TYPE5 VESSEL
        Enter Ship Type - 0-99, default 0 37
        Enter Dimension to Bow - max 511, default 050
        Enter Dimension to Stern - max 511, default 047
        Enter Dimension to Port - max 511, default 012
        Enter Dimension to Starboard - max 511, default 013
        Enter EPFD Type range 0-8 default 0 (undefined) 1
        Enter ETA Month - default 0 - Not Available11
        Enter ETA Day - default 0 - Not Available10
        Enter ETA Hour - default 0 - Not Available12
        Enter ETA Minute - default 0 - Not Available20
        Input Draught - default = 0 10
        Enter Destination max 20 Chars - UPPER CASE MEL
        :return:
        '''
        print('Testing do_datareport')
        #testais = '!AIVDM,1,1,,A,57Ol>000Bm`MHsCGH01@E=B1AU0GF1HE=<Dh000U6@g<=2m<DI3AC000000000000000000,0*5'
        teststream = TestStreams()
        testais = teststream.teststream[5][0]

        myais = AISStream(testais)
        mydata = StaticData(myais.binary_payload)
        myaprs = APRS(mydata.mmsi, mydata.latitude, mydata.longitude, mydata.course_over_ground,
                      mydata.speed_over_ground, mydata.callsign + mydata.vessel_name, False)
        message = datareport(mydata, myaprs, True).decode("utf-8")
        # expected = (f'CG722>APU25N,TCPIP*:;503123456_{datetime.utcnow().strftime("%d%H%Mz")}'
        #             f'0000.00S\\00000.00Ws360.0/0.0 503123456 \n')
        expected = teststream.teststream[5][1][0:30] + '_' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[5][1][38:]
        self.assertEqual(expected, message, f"Failed in do_position with message type "
                                            f"{myais.message_type}\n input string = {testais}")

    def test_queue_aprs(self):
        print('Testing queue_aprs')
        teststream = TestStreams()
        serverqueue = GlobalDefinitions.Global.ServerQueue

        testdata = [
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
                'CG722>APU25N,TCPIP*:;503123654*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
                'CG722>APU25N,TCPIP*:;503654321*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
                'CG722>APU25N,TCPIP*:;503123456*XXXXXXX3823.99S\\14730.00WL\n'
                    ]

        # first with no entries in queue
        tcpbytes = testdata[0]
        tcparray = bytearray(testdata[0], "utf-8")
        mmsi = tcpbytes[21:30]
        self.assertFalse('503123456' in serverqueue, 'Found entry where no entry sholuld be in server queue')
        QueueAPRS(mmsi, tcparray)
        self.assertTrue('503123456' in serverqueue, 'Found no entry when one expectedin server queue')
        self.assertEqual(testdata[0], serverqueue['503123456'],
                         'Incorrect entry retrieved from server queue with supposedly only one entry')

        # then load some other entries into the queue
        for i in range(1, 3):
            tcpbytes = testdata[i]
            tcparray = bytearray(testdata[i], "utf-8")
            mmsi = tcpbytes[21:30]
            QueueAPRS(mmsi, tcparray)

        # and then load a newer entry into the queue data field should reflect new value
        tcpbytes = testdata[3]
        tcparray = bytearray(testdata[3], "utf-8")
        mmsi = tcpbytes[21:30]
        QueueAPRS(mmsi, tcparray)
        self.assertTrue('503123456' in serverqueue, 'Found no entry when one expected in server queue')
        self.assertEqual(testdata[3], serverqueue['503123456'],
                         'Incorrect entry retrieved from server queue with supposedly only one entry')


    def test_transmit_aprs(self):
        print('Testing transmit_aprs')

        testdata = [
            'CG722>APU25N,TCPIP*:;503123456*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
            'CG722>APU25N,TCPIP*:;503123654*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
            'CG722>APU25N,TCPIP*:;503654321*XXXXXXX3823.99S\\14730.00Ws122.0/30.0 503123456 503123456\n',
            'CG722>APU25N,TCPIP*:;503123456*XXXXXXX3823.99S\\14730.00WL\n'
        ]

        GlobalDefinitions.Global.UseRemote = False
        UseRemote = GlobalDefinitions.Global.UseRemote
        GlobalDefinitions.Global.LogAPRS = True
        LogAPRS = GlobalDefinitions.Global.LogAPRS
        GlobalDefinitions.Global.APRSFileName = './aprstestlog.txt'
        APRSLogFile = GlobalDefinitions.Global.APRSFileName

        LastTransmit = GlobalDefinitions.Global.LastTransmit
        ServerQueue = GlobalDefinitions.Global.ServerQueue
        NoConnect = GlobalDefinitions.Global.NoConnect

        # Flush the server squeue in case
        delete_list = []
        for key in ServerQueue:
            delete_list.append(key)

        for _ in delete_list:
            del ServerQueue[_]

        # first load a single item into queue and flush the APRSlogfile by deleting it will be regenerated during test
        tcpbytes = testdata[0]
        tcparray = bytearray(testdata[0], "utf-8")
        mmsi = tcpbytes[21:30]
        QueueAPRS(mmsi, tcparray)

        if os.path.exists('./aprstestlog.txt'):
            os.remove('./aprstestlog.txt')

        # force a transmit - boolean test overrides the timeout value

        TransmitAPRS(True)

        with open('./aprstestlog.txt', "r") as f:
            bytes = f.readlines()

        self.assertEqual(testdata[0], bytes[0],'Failed to properly log outgoing packet')

        for i in range(0,4):
            tcpbytes = testdata[i]
            tcparray = bytearray(testdata[i], "utf-8")
            mmsi = tcpbytes[21:30]
            QueueAPRS(mmsi, tcparray)

        # should now have a server queue of 4 items
        TransmitAPRS(True)

        # need to check whats in logfile against what we expected to havebeen sent

        valid = True

        with open('./aprstestlog.txt', "r") as f:
            bytes = f.readlines()
            for k in range(0,len(bytes)):
                found = False
                for i in range(0, 4):
                    if bytes[k] == testdata[i]:
                        found = True

                if not found:
                    valid = False
                found = False

        self.assertTrue(valid,"data which was queued did not gret logged as transmitted")













    def test_define_server_address(self):
        print('Testing define_server_address')
        #@ define_server_address(useremote: bool):

        initialise = MyPreConfigs()

        address = define_server_address(False)
        expected = GlobalDefinitions.Global.ServerAddress, int(GlobalDefinitions.Global.APRSPort)
        self.assertEqual(expected[0], address[0], 'Failed in defining remote server address')
        self.assertEqual(expected[1], address[1], 'Failed in defining remote server address')

        address = define_server_address(True)
        expected = GlobalDefinitions.Global.remoteEnd, int(GlobalDefinitions.Global.APRSPort),
        self.assertEqual(expected[0], address[0], 'Failed in defining remote server address')
        self.assertEqual(expected[1], address[1], 'Failed in defining remote server address')

    def test_do_print_server_address(self):
        print('Testing print_server_address')
        do_print_server_address(False)
        response = input('Did local server addresses print? (y/Y/n/N) ')
        self.assertEqual('Y', response.upper(), "Should have printed local server addresses")
        print('\n')

        do_print_server_address(True)
        response = input('Did remote server addresses print? (y/Y/n/N) ')
        self.assertEqual('Y', response.upper(), "Should have printed remote server addresses")
        print('\n')

    def test_do_log_aprs(self):
        print('Testing do_log_aprs')
        #do_log_aprs(logaprs: bool, aprslogfile, tcpbytes):

        # ensure we start with a clean slate
        if os.path.exists('./aprstestlog.txt'):
            os.remove('./aprstestlog.txt')

        do_log_aprs(True, './aprstestlog.txt', bytearray('This is a test write to logfile', "utf-8"))

        with open('./aprstestlog.txt', "r") as f:
            bytes = f.read()
        self.assertEqual('This is a test write to logfile', bytes,
                         'Failed to write to logfile')

        if os.path.exists('./aprstestlog.txt'):
            os.remove('./aprstestlog.txt')

        # now the opposite no write

        do_log_aprs(False, './aprstestlog.txt', bytearray('This is a test write to logfile', "utf-8"))

        self.assertFalse(os.path.exists('./aprstestlog.txt'),
                         'Failed - should not have opened and written to file')




class TestAPRS(TestCase):

    def initialise(self):
        diction = AISDictionaries()
        # the ais stream used here is only a place filler.
        mystream = AISStream('!AIVDM,1,1,,A,404kS@P000Htt<tSF0l4Q@100h3c,0*6B')

        return diction, mystream

    def test_set_course(self):
        print('Testing set_course')

        for course in [(0, '000'), (10, '010'), (100, '100'), (359, '359')]:
            myaprs = APRS('503123456', 90.0, 147, course[0],
                          30, 'TEST', False)
            myaprs.set_Course(f'{course[0]:03}')
            self.assertEqual(course[1], myaprs._course, 'Failure in APRS.set_course')

    def test_set_speed(self):
        print('Testing set_speed')
        for speed in [(0, '000'), (10, '010'), (100, '100')]:
            myaprs = APRS('503123456', 90.0, 147, 122,
                          speed[0], 'TEST', False)
            myaprs.set_Speed(f'{speed[0]:03}')
            self.assertEqual(speed[1], myaprs._speed, 'Failure in APRS.set_speed')

    def test_set_name(self):
        print('Testing set_name')
        for test in ['FREDDO', 'SPIRIT OF PAYNESVILLE']:
            myaprs = APRS(test, 90.0, 147, 122,
                          30, 'TEST', False)

            testlong: str = myaprs.set_Name(test)
            self.assertEqual(test, myaprs._name, 'Failure in APRS.Set_callsign')

    def test_set_callsign(self):
        print('Testing set_callsign')
        for test in ['VN12345', 'ABC98765']:
            myaprs = APRS(test, 90.0, 147, 122,
                          30, 'TEST', False)

            testlong: str = myaprs.set_Callsign(test)
            self.assertEqual(test, myaprs._callsign, 'Failure in APRS.Set_callsign')

    def test_set_mmsi(self):
        print('Testing set_mmsi')
        for test in ['503123456', '005034321']:
            myaprs = APRS(test, 90.0, 147, 122,
                          30, 'TEST', False)

            testlong: str = myaprs.set_MMSI(test)
            self.assertEqual(test, myaprs._mmsi, 'Failure in APRS.Set_mmsi')

    def test_convert_longitude(self):
        print('Testing convert_longitude')
        # def ConvertLongitude(self, longitude: float) -> str:
        diction, mystream = self.initialise()

        for test in [(0.0, '00000.00W'), (90.0, '09000.00E'), (-90.0, '09000.00W'),
                     (147.5, '14730.00E'), (-147.5, '14730.00W'), (147.5632, '14733.79E')]:
            myaprs = APRS('503123456', 90.0, test[0], 122,
                          30, 'TEST', False)

            testlong: str = myaprs.ConvertLongitude(test[0])
            self.assertEqual(test[1], testlong, 'Failure in APRS.ConvertLongitude')

    def test_convert_latitude(self):
        print('Testing convert_latitude')
        # def ConvertLatitude(self, longitude: float) -> str:

        diction, mystream = self.initialise()

        for test in [(0.0, '0000.00S'), (90.0, '9000.00N'), (-90.0, '9000.00S'),
                     (47.5, '4730.00N'), (-43.5, '4330.00S'), (47.5632, '4733.79N')]:
            myaprs = APRS('503123456', test[0], 147, 122,
                          30, 'TEST', False)

            testlong: str = myaprs.ConvertLatitude(test[0])
            self.assertEqual(test[1], testlong, 'Failure in APRS.ConvertLatitude')

    def test_convert_speed(self):
        print('Testing convert_speed')
        diction, mystream = self.initialise()

        for speed in [(0, '000'), (1, '001'), (10, '010'), (100, '100'), (257, '257')]:
            myaprs = myaprs = APRS('503123456', 38, 147, 122,
                                   speed[0], 'TEST', False)
            myaprs.ConvertSpeed(speed[0])
            self.assertEqual(speed[1], myaprs._speed, "Failure in APRS.ConvertSpeed")

    def test_create_object_position(self):
        '''
        Types 1, 2, 3, 4, 9, 18, 19, 21, 27 all use this routine
        set up dummy aisstring for each type and pass to create_object_position


        :return:
        '''
        print('Testing create_object_position')
        diction, mystream = self.initialise()
        teststream = TestStreams()

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
        testais1 = teststream.teststream[1][0]

        '''
        Enter UTC Year 4 digits - default 0 - Not Available2023
        Enter UTC Month 2 digits - default 0 - Not Available11
        Enter UTC Day 2 digits - default 0 - Not Available08
        Enter UTC Hour 2 digits - default 24 - Not Available17
        Enter UTC Minute 2 digits - default 60 - Not Available58
        Enter UTC Second 2 digits - default 60 - Not Available0
        Input Fix Quality 0/1 - default = 0 
        '''
        testais4 = teststream.teststream[4][0]
        '''
        Enter Altitude - max 4095 1045
        Enter Speed Over Ground max 1022 300
        Enter Assigned Flag 0/1 0
        '''
        testais9 = teststream.teststream[9][0]
        testais18 = teststream.teststream[18][0]
        '''
        Enter Vessel Name 20 chars upper caseTEST VESSEL
        Enter Ship Type - 0-99, default 0 37
        Enter Dimension to Bow - max 511, default 0 50
        Enter Dimension to Stern - max 511, default 047
        Enter Dimension to Port - max 511, default 012
        Enter Dimension to Starboard - max 511, default 013
        Enter EPFD Type range 0-8 default 0 (undefined) 3
        '''
        testais19 = teststream.teststream[19][0]
        '''
        Enter Aid Type 0-31 numeric 6
        Enter Vessel Name 20 chars upper caseTEST AID
        Enter Extended Vessel Name 15 chars upper caseNO EXTENSION
        '''
        testais21 = teststream.teststream[21][0]
        '''
        Enter Navigation Status range 0-15 default 15 2
        '''
        testais27 = teststream.teststream[27][0]

        # now the guts of the tests
        # use function prepare_position to avoid duplicated effort
        myais = AISStream(testais1)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[1][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[1][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais1}")
        # and a kill position report message - Kill boolean passed to prepare position
        # only difference should be an _ in position 10 of information field rather than a *
        message = self.prepare_position(myais, True)
        expected = teststream.teststream[1][1][0:30] + '_' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[1][1][38:-10] + '\n'
        self.assertEqual(expected, message, f"Failed in kill APRS.Create_Object_position with message type "
                                            f"{myais.message_type}\n input string = {testais1}")

        myais = AISStream(testais9)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[9][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[9][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais9}")

        myais = AISStream(testais18)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[18][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[18][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais18}")

        myais = AISStream(testais19)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[19][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[19][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais19}")

        myais = AISStream(testais21)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[21][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[21][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais21}")

        myais = AISStream(testais27)
        message = self.prepare_position(myais)

        # for expected strings if expected contains a backslash it needs be escaped by another backslash
        expected = teststream.teststream[27][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[27][1][38:]

        self.assertEqual(expected, message, f"Failed in APRS.Create_Object+position with message type "
                                            f"{myais.message_type}\n input string = {testais27}")

    def prepare_position(self, mystream: AISStream, kill: bool = False):
        # allows setting up of conditions to pass data to create_position
        if mystream.message_type in [1, 2, 3]:
            mydata = CNB(mystream.binary_payload)
        elif mystream.message_type == 9:
            mydata = SAR_aircraft_position_report(mystream.binary_payload)
        elif mystream.message_type == 18:
            mydata = ClassB_position_report(mystream.binary_payload)
        elif mystream.message_type == 19:
            mydata = Extende_ClassB_position_report(mystream.binary_payload)
        elif mystream.message_type == 21:
            mydata = Aid_to_navigation_report(mystream.binary_payload)
        elif mystream.message_type == 27:
            mydata = Long_range_AIS_broadcast_message(mystream.binary_payload)
        else:
            raise Exception('Invalid message type presented in preparing test APRS position')

        myaprs = APRS(mydata.mmsi, mydata.latitude, mydata.longitude, mydata.course_over_ground,
                      mydata.speed_over_ground, mydata.callsign + mydata.vessel_name, False)

        return myaprs.CreateObjectPosition(kill, mydata)

    def test_create_base_position(self):
        '''
        Set up position reportr for a base station (Type 4)


        :return:
        '''
        diction, mystream = self.initialise()
        '''
        Input Fragment Count = 1
        What is Message_ID default null = 
        What channel ID = A
        Input Payload Type (Numeric 1-27 = 4
        Enter MMSI - 9 digits, default 503123456 = 
        Enter UTC Year 4 digits - default 0 - Not Available2023
        Enter UTC Month 2 digits - default 0 - Not Available11
        Enter UTC Day 2 digits - default 0 - Not Available09
        Enter UTC Hour 2 digits - default 24 - Not Available18
        Enter UTC Minute 2 digits - default 60 - Not Available42
        Enter UTC Second 2 digits - default 60 - Not Available0
        Input Fix Quality 0/1 - default = 0 
        Enter longitude decimal +ve West, -ve East = -147.5
        longitude  -147.5
        intlongitude -88500000
        Enter latitude decimal +ve North, -ve South = -38.4
        intllattitude -23040000
        Enter EPFD Type range 0-8 default 0 (undefined) 4
        '''
        print('Testing create_base_position')
        teststream = TestStreams()

        testais = teststream.teststream[4][0]
        myais = AISStream(testais)
        mydata = Basestation(myais.binary_payload)

        myaprs = APRS(mydata.mmsi, mydata.latitude, mydata.longitude, mydata.course_over_ground,
                      mydata.speed_over_ground, mydata.callsign + mydata.vessel_name, False)

        message = myaprs.CreateBasePosition(False, mydata)
        expected = teststream.teststream[4][1][0:30] + '*' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[4][1][38:]
        self.assertEqual(expected, message, 'Failed in establishing AQPRS.base position report')
        # and a kill
        message = myaprs.CreateBasePosition(True, mydata)
        expected = teststream.teststream[4][1][0:30] + '_' \
                   + f'{datetime.utcnow().strftime("%d%H%Mz")}' \
                   + teststream.teststream[4][1][38:]
        self.assertEqual(expected, message, 'Failed in establishing AQPRS.base kill position report')

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
        print('Testing create_safety_message')
        diction, mystream = self.initialise()
        teststream = TestStreams()


        # first a Type 14 broadcast message with less than 67 chrs
        print('short type 14')
        testais = teststream.teststream[14][0]
        message = self.prepare_safety(14, testais)
        expected = teststream.teststream[14][1][0:30] + ':' \
                   + teststream.teststream[14][1][31:] + '\n'
        self.assertEqual(expected, message, "In testing APRS.create short type14 safety message fail")

        # now a longer thgan 67 char safety message
        print('long type 14')
        testais = ('!AIVDM,1,1,,A,>7Ol>01@PU>0U>060htpN1<4HEAV0lE=<4LF0tJ05B0hD5=B37320<P585'
                   '<=@E9>337;?CGKOSW37;?CGKOSW37;?CGKOSW37;?CGKOSW337;?CGKOST,0*5')
        message = self.prepare_safety(14, testais)
        expected = ('CG722>APU25N,TCPIP*::BLN0     :THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS '
                    '01234567\nCG722>APU25N,TCPIP*::BLN1     :8901234567890123456789012345678900123456789\n')
        self.assertEqual(expected, message, "In testing APRS.create long type14 safety message fail")

        # now for Type 12 Addressed Safety Message
        # first a short message
        print('short type 12')
        testais = teststream.teststream[12][0]
        message = message = self.prepare_safety(12, testais)
        expected = teststream.teststream[12][1]
        self.assertEqual(expected, message, "In testing APRS.create short type12 addressed safety message fail")
        print('long type 12')
        # now a long (to be split) message
        # 'THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS 012345678901234567890123456789012345678900123456789')'
        testais = ('!AIVDM,1,1,,A,<7Ol>01ou3P0D89CP9CP1P<?>7PC165DIP=5CC175P?6P1DP<51CDPihh'
                   'P381B1C3D5BCPhijklmnopqhijklmnopqhijklmnopqhijklmnopqhhijklmnopq,0*5')
        message = message = self.prepare_safety(12, testais)
        expected = ('CG722>APU25N,TCPIP*:503123456:THIS IS A LONG SAFETY MESSAGE OF AT LEAST 100 CHARASCTERS 01234567\n'
                    'CG722>APU25N,TCPIP*:503123456:8901234567890123456789012345678900123456789\n')
        self.assertEqual(expected, message, "In testing APRS.create long type12 addressed safety message fail")

    def prepare_safety(self, message_type: int, testais: str):
        mystream = AISStream(testais)
        if message_type == 14:
            mydata = Payloads.Safety_related_broadcast_message(mystream.binary_payload)
        elif message_type == 12:
            mydata = Payloads.Addressed_safety_related_message(mystream.binary_payload)

        myaprs = APRS(mydata.mmsi, 0.0, 0.0, 0.0, 0.0, 'SAFETY', 0)

        message = myaprs.CreateSafetyMessage(0, mydata)

        return message
