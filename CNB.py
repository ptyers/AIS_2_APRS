import AISData
import MyPreConfigs
from GlobalDefinitions import Global
from AISData import AIS_Data


# CNB is Common Navigation Block


def do_CNB(AISObject):
    # AISObject is the encoded payload string received in message types 1,2,3 - 168 bits usually
    # it is an AISData object and passed from the main program through calls by reference
    # HOPEFULLY changes made to it here will be reflected in the original
    # TO BE CONFIRMED
    # contains both the payload ans a binary version of the payload
    # bit 0-5 message type
    # bits 6-7 Repeat Indicator
    # bits 8-37 MMSI
    # Types 1/2/3 and 18
    # bits 38-41 Navigation Status
    # bits 42-49 Rate of Turn
    # TYpe 9
    # bits 38-49 Altitude in metres
    # bits 50-59 Speed over ground
    # bits 60-60 Position Accuracy
    # bits 61-88 Longitude Minutes/10000
    # bits 89-115 Latitude Minutes/10000
    # bits 116-127 Course over ground (relative to True North)
    # Types 1/2/3/18
    # bits 128-136 True Heading
    # bits 137-142 Time Stamp
    # bits 143-144 Manouver Indicator
    # bits 145-147 SPARE
    # bits 148-148 RAIM Flag - Receiver Autonomous Integrity Monitoring
    # bits 149-167 Radio Status
    # Type 9
    # bits 128-133 Time Stamp
    # bits 134-141 Regional Reserved
    # bits 141-142 DTE 0 DTE ready, 1 DTE not ready
    # bits 143-145 SPARE
    # bits 146-146 Assigned
    # bits 147-147 RAIM Flag - Receiver Autonomous Integrity Monitoring
    # bits 148-167 Radio Status

    # get current diagnostic settings
    diagnostic = Global.diagnostic
    diagnostic2 = Global.diagnostic2
    diagnostic3 = Global.diagnostic3
    MyMap = Global.MyMap

    if diagnostic3:
        print("into CNB payload_id =   ", AISObject.AIS_Payload_ID)
        # print('entering CNB Binary payload = ' , bin(AISObject.AIS_Binary_Payload))
    # first the repeat indicator uper 2 bits of second 6 bit nibble

    AISObject.RepeatIndicator = AISObject.Binary_Item(6, 2)
    if diagnostic3:
        print("got repeat indicator = ", AISObject.RepeatIndicator)
        pass

    # now bits 8-37 the MMSI - character positions 1 to 6
    AISObject.get_string_MMSI(AISObject.Binary_Item(8, 30))

    if diagnostic3:
        print("got MMSI = ", AISObject.MMSI)
        pass
    # Console.WriteLine(" MMSI = " + p_mmsi)

    # dependent upon message type 1/2/3 or 18 bit references change or fields do not exist

    p_urot = 0
    p_ulong = 0

    # switch (AISObject.AIS_Payload_ID)
    # again use a function called via dictionary to replace the switch
    # switch(AISObject.AIS_Payload_ID)

    Dict123_9_18 = {1: do123, 2: do123, 3: do123, 9: do9, 18: do18}
    doswitch(AISObject.AIS_Payload_ID, AISObject, Dict123_9_18)


def doswitch(payload, AISObject, switchdict):
    # replaces a switch uses switchdict to determine which function to execute woth arguments payload and AISObject
    # print('payload ', payload, ' AISObject ',AISObject )
    if payload in switchdict:
        return switchdict[payload](AISObject)
    else:
        raise ValueError("Function to handle payload_ID unknown")
    pass


def do123(AISObject):
    AISObject.set_NavStatus(AISObject.Binary_Item(38, 4))
    # now rate of turn
    # the defproperty p_rot is kept as a signed integer32
    # this will require filling to the left for negative values given that the parameter is 8 bits long, bit 8 sign bit
    # extracted from  6 bits of char position 7 and upper 2  bits of char position 8

    # if bit 0 is 1 then we have a negative value (twos complement)
    p_urot = AISObject.Binary_Item(42, 8)
    if p_urot > 128:
        AISObject.set_int_ROT(int(p_urot - 256))
    else:
        AISObject.set_int_ROT(int(p_urot))
        #            Console.WriteLine(" Rate of Turn = ", + p_rot)
    AISObject.set_SOG(AISObject.Binary_Item(50, 10))
    #            Console.WriteLine("SOG = ", p_sog )

    # sometings are common between 123 and 9
    doCommon123_9(AISObject)

    AISObject.set_int_HDG(AISObject.Binary_Item(128, 9))

    AISObject.set_Timestamp(AISObject.Binary_Item(137, 6))
    #            Console.WriteLine("UTC Seconds = " + p_time)
    AISObject.set_MAN_Indicator(AISObject.Binary_Item(143, 2))
    #            Console.WriteLine("Manouvering  = " + p_man)

    # RAIM Flag bit 148 extract from character position 24 bit 4
    p_r = AISObject.Binary_Item(148, 1)
    if p_r > 0:
        AISObject.set_RAIM(True)
    else:
        AISObject.set_RAIM(False)
        #            Console.WriteLine("RAIM Flag  = " + p_raim)

        # lastly Radio Status bits 149-167 extracted from character positions 24 (bit 5), 25 (6 bits), 26 (6 bits), 27(6 bits)
        # we need to check here that theres enough characters to meet the need
        #
        if len(AISObject.AIS_Payload) >= 28:

            AISObject.AISObject.Binary_Item(149, 19)
            #          Console.WriteLine("RadioStatus  = " + p_rad_status)
        # else:
        #     AISObject.ra(0)

    pass


def doCommon123_9(AISObject):
    # things common to both 123 and 9

    # next position accuracy True/False indicated by 0/1 bit 60 character position 10 bit 0
    # p_pa True indicates augmented system
    if AISObject.Binary_Item(60, 1) > 0:
        AISObject.set_Pos_Accuracy(True, 1)
    else:
        AISObject.set_Pos_Accuracy(False, 1)

    # get longitude from binary
    p_ulong = AISObject.Binary_Item(61, 28)
    # have now got 28 bits check that the upper bit is zero or one
    #
    if (p_ulong & 0x8000000) > 0:
        print(p_ulong - 268435456)
        AISObject.set_int_longitude(int(p_ulong - 268435456))

    else:
        AISObject.set_int_longitude(int(p_ulong))

    # ditto for latitude extract from bit position 89 for 27 bits
    p_ulat = AISObject.Binary_Item(89, 27)
    # have now got 27 bits check that the upper bit is zero or one
    #
    if (p_ulat & 0x4000000) > 0:
        AISObject.set_int_latitude(int(p_ulat - 134217728))
    else:
        AISObject.set_int_latitude(int(p_ulat))

    AISObject.set_int_COG(AISObject.Binary_Item(116, 12))

    pass


def do9(AISObject):
    AISObject.set_NavStatus(15)
    AISObject.set_int_ROT(128)
    AISObject.set_Altitude = AISObject.Binary_Item(38, 12)
    AISObject.set_SOG(AISObject.Binary_Item(50, 10))
    AISObject.set_SOG(AISObject.SOG * 10)  # aircraft speed in knots not deciknots
    AISObject.set_Timestamp(AISObject.Binary_Item(128, 6))

    # next position accuracy True/False indicated by 0/1 bit 60 character position 10 bit 0
    # p_pa True indicates augmented system
    if AISObject.Binary_Item(60, 1) > 0:
        AISObject.set_Pos_Accuracy(True, 1)
    else:
        AISObject.set_Pos_Accuracy(False, 1)

    # some things lat/long/COG common to 123 and 9
    doCommon123_9(AISObject)

    if AISObject.Binary_Item(142, 1) == 0:
        AISObject.set_DTE(False)

    if AISObject.Binary_Item(146, 1) == 0:
        AISObject.set_Assigned(False)

    p_r = int(AISObject.Binary_Item(147, 1))
    if p_r > 0:
        AISObject.set_RAIM(True)
    else:
        AISObject.set_RAIM(False)
    #            Console.WriteLine("RAIM Flag  = " + p_raim)

    # lastly Radio Status bits 148-167 extracted from character positions 24 (bit 5), 25 (6 bits), 26 (6 bits), 27(6 bits)
    # we need to check here that theres enough characters to meet the need
    #
    if len(AISObject.AIS_Payload) >= 28:

        AISObject.AISObject.Binary_Item(148, 19)
        #          Console.WriteLine("RadioStatus  = " + p_rad_status)
    # else:
    #     AISObject.(0)

    pass


def do18(AISObject):
    AISObject.set_SOG(AISObject.Binary_Item(46, 10))
    if AISObject.Binary_Item(56, 1) > 0:
        AISObject.set_Pos_Accuracy(True, 1)
    else:
        AISObject.set_Pos_Accuracy(False, 1)

    p_ulong = AISObject.Binary_Item(57, 28)  # Longitude
    if (p_ulong & 0x8000000) > 0:
        AISObject.set_int_longitude(int(p_ulong - 268435456))
    else:
        AISObject.set_int_longitude(int(p_ulong))

    p_ulat = AISObject.Binary_Item(85, 27)  # Latitude
    if (p_ulat & 0x4000000) > 0:
        AISObject.set_int_latitude(int(p_ulat - 134217728))
    else:
        AISObject.set_int_latitude(int(p_ulat))

    AISObject.set_int_COG(AISObject.Binary_Item(112, 12))
    # True Heading bits 128 to 136 (9 bits) from character positions 21 (3 bits) and 22 (6 bits)
    AISObject.set_int_HDG(AISObject.Binary_Item(124, 9))
    # timestamp UTC second
    # bits 137-142 (6 bits) from character positions 23 (6 bits)
    AISObject.set_Timestamp(AISObject.Binary_Item(133, 6))
    AISObject.set_NavStatus(15)
    AISObject.set_int_ROT(128)

    if AISObject.Binary_Item(142, 1) == 0:
        AISObject.set_Display(False)
    else:
        AISObject.set_Display(True)

    if AISObject.Binary_Item(143, 1) == 0:
        AISObject.set_DSC(False)
    else:
        AISObject.set_DSC(True)

    if AISObject.Binary_Item(144, 1) == 0:
        AISObject.set_BAND(False)
    else:
        AISObject.set_BAND(True)

    if AISObject.Binary_Item(145, 1) == 0:
        AISObject.set_Message22(False)
    else:
        AISObject.set_Message22(True)

    if AISObject.Binary_Item(146, 1) == 0:
        AISObject.set_Assigned(False)
    else:
        AISObject.set_Assigned(True)

    p_r = int(AISObject.Binary_Item(147, 1))
    if p_r > 0:
        AISObject.set_RAIM(True)
    else:
        AISObject.set_RAIM(False)
    #            Console.WriteLine("RAIM Flag  = " + p_raim)

    # lastly Radio Status bits 148-167 extracted from character positions 24 (bit 5), 25 (6 bits), 26 (6 bits), 27(6 bits)
    # we need to check here that theres enough characters to meet the need
    #
    if len(AISObject.AIS_Payload) >= 28:

        AISObject.AISObject.Binary_Item(148, 19)
        #          Console.WriteLine("RadioStatus  = " + p_rad_status)
    # else:
    #     AISObject.(0)


def decode_char(self, in_char: str) -> int:
    my_int = int(0)
    mybyte = bytearray(in_char, "utf-8")

    my_int = mybyte[0]
    # need to mask off the upper 2 bits
    #                my_int = my_int & 0x3F
    if (my_int - 48) > 40:
        my_int = my_int - 56
    else:
        my_int = my_int - 48
    return my_int


def main(self):
    pass


if __name__ == 'main':
    main()
