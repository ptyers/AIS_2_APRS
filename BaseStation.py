import MyPreConfigs
import GlobalDefinitions


class BASESTATION:
    # Implements the various parameters required for Base Station Reporting
    # Message Type 4
    #
    # Bits 0-5 Message type
    # Bits 6-7 Repeat Indicator
    # Bits 8-37 MMSI
    # Bits 38-51 Year (UTC)
    # Bits 52-55 Month (UTC)
    # Bits 56-60 Day (UTC)
    # Bits 61-65 Hour (UTC)
    # Bits 66-71 Minute (UTC)
    # Bits 72-77 Second (UTC)
    # Bits 78-78 Fix Quality
    # Bits 79-106 Longitude
    # Bits 107-133 Latitude
    # Bits 134-137 Type of EPFDF
    # Bits 138-147 SPARE
    # Bits 148-148 RAIM Flag
    # Bits 149-167 SOTDMA State

    def __init__(self, aisdata):  # input is of type AUSData
        diagnostic = GlobalDefinitions.Global.diagnostic
        diagnostic2 = GlobalDefinitions.Global.diagnostic2
        diagnostic3 = GlobalDefinitions.Global.diagnostic3

        # first the repeat indicator uper 2 bits of second 6 bit nibble
        aisdata.RepeatIndicator = aisdata.Binary_Item(6, 2)  #
        # now bits 8-37 the MMSI - character positions 1 to 6
        aisdata.MMSI = aisdata.Binary_Item(8, 37)  #
        #            Console.WriteLine(" MMSI = " + p_mmsi)#
        # next longitude signed integer 28 bits. Starting Position 79
        # if upper bit is 1 signed integer needs twos complement negation
        #
        p_ulong = int(0)  #
        p_ulong = aisdata.Binary_Item(79, 28)  #

        # have now got 28 bits check that the upper bit is zero or one
        #
        if (p_ulong & 0x8000000) > 0:
            aisdata.int_longitude = int(p_ulong - 268435456)  #
        else:
            aisdata.int_longitude = int(p_ulong)  #

        # ditto for latitude extract from bit position 107 for 27 bits

        p_ulat = int(0)  #
        p_ulat = aisdata.Binary_Item(107, 27)  #

        # have now got 27 bits check that the upper bit is zero or one
        #
        if (p_ulat & 0x4000000) > 0:
            aisdata.int_latitude = int(p_ulat - 134217728)  #
        else:
            aisdata.int_latitude = int(p_ulat)  #

        # RAIM Flag bit 148 extract from character position 24 bit 4
        p_r = aisdata.Binary_Item(148, 1)  #
        if p_r > 0:
            aisdata.RAIM = True  #
        else:
            aisdata.RAIM = False  #
        #            Console.WriteLine("RAIM Flag  = " + p_raim)#

        # need to dummy up a speed and heading settings for Base stations - which are stationary
        aisdata.SOG = 0
        aisdata.COG = 0

        if diagnostic3:
            print(
                " in Base Station init aisdata.SOG, aisdata.HDG ",
                aisdata.SOG,
                " ",
                aisdata.HDG,
            )
