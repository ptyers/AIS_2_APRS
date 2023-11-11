from datetime import datetime, timezone
import logging
from GlobalDefinitions import Global
import struct
import sys
from AISDictionary import AISDictionaries

'''
utility to allow creation of AIS Streams

'''
# dummy mmsi may be overwritten later
mmsi = '503123456'
header = '!AIVDM,'
fragment_count: str
fragment_number: str
message_id: str
channel_id: str
Checksum: str = ',0*5'  # dummy checksum field NOT CALCULATED

AISString: str  # string returned after creation


def do_encode(input_payload: str, fragmentcount: str, fragmentnumber: str, messageid: str, channelid: str):
    diction = AISDictionaries()
    # takes payload six bits at a time and armoured encodes them
    payload = input_payload

    while len(payload) % 6 != 0:
        payload = payload + '0'

    encstring = do_header(fragmentcount, fragmentnumber, messageid, channelid)
    endex = 6
    while endex < len(payload)+ 1:
        encstring = encstring + diction.nibble_to_armour(payload[endex - 6:endex])
        endex += 6

    # print(encstring)

    return encstring


def do_header(fragmentcount: str, fragmentnumber: str, messageid: str, channel_id: str) -> str:
    hheader = header
    return hheader + fragmentcount + ',' + fragmentnumber + ',' + messageid + ',' + channel_id + ','


def do_123() -> str:
    # now create a binary payload for CNB, this will be encoded as a last step

    binary_payload = '00000100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    nav_status = input('Enter Navigatiobn Status range 0-15 default 15 ')
    if len(nav_status) == 0:
        nav_status = '15'
    binary_payload = binary_payload + '{:04b}'.format(int(nav_status))  # Navigation Status

    rate_of_turn = input('Enter Rate Of Turn 0-128, 128 default = ')
    if len(rate_of_turn) == 0:
        rate_of_turn = 128
    binary_payload = binary_payload + '{:08b}'.format(int(rate_of_turn))

    speed_over_ground = input('Enter Speed over ground range 0-102 knots default 102.2 = ')
    if len(speed_over_ground) == 0:
        speed_over_ground = '5'
    int_speedoverground = int(float(speed_over_ground) * 10)
    binary_payload = binary_payload + '{:010b}'.format(int_speedoverground)
    # going to assume a default 0 for position accuracy bit -
    binary_payload = binary_payload + '0'

    longitude, latitude = longlat()

    binary_payload = binary_payload + longitude + latitude

    course_over_ground = input("Enter course over ground range 0-359 default 360 = ")
    if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
        course_over_ground = '360'
    binary_payload = binary_payload + '{:012b}'.format(int(course_over_ground) * 10)

    true_heading = input("True heading range 0-259 default 360 = ")
    if len(true_heading) == 0 or not (0 <= int(true_heading) <= 359):
        true_heading = '360'
    binary_payload = binary_payload + '{:09b}'.format(int(true_heading))

    # setting timestamp to 0
    binary_payload = binary_payload + '000000'
    # setting Maneouver Indicator to 0
    binary_payload = binary_payload + '00'
    # setting RAIM Flag to 0, prefiling spare bit
    binary_payload = binary_payload + '0000'
    # setting Radio Status to all zero
    binary_payload = binary_payload + '0000000000000000000'

    # veracity check print out payload length
    print("Having created Type 123 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def longlat() -> tuple:
    longitude = input('Enter longitude decimal +ve West, -ve East = ')
    if len(longitude) == 0:
        longitude = '147'
    print("longitude ", longitude)
    if not (-180 <= float(longitude) <= 180):
        print("Error longitude must be between -180 and 180 set to 147.0")
        longitude = '147.0'

    intlongitude = int(float(longitude) * 600000)
    print(f'intlongitude {intlongitude}')
    if intlongitude < 0:
        binlong = '{:028b}'.format(abs(intlongitude))
        binlong = twos_comp_negation(binlong, 28)
    else:
        binlat = '{:028b}'.format(intlongitude)

    latitude = input('Enter latitude decimal +ve North, -ve South = ')
    if len(latitude) == 0:
        latitude = '38'
    if not (-90 <= float(latitude) <= 90):
        print("Error longitude must be between -180 and 180 set to -38.5")
        lattitude = '-38.5'
    intlatitude = int(float(latitude) * 600000)
    print(f'intllattitude {intlatitude}')
    if intlatitude < 0:
        binlat = '{:027b}'.format(abs(intlatitude))
        binlat = twos_comp_negation(binlat, 27)
    else:
        binlat = '{:027b}'.format(intlatitude)


    return binlong, binlat

def twos_comp_negation(binstring: str, length: int) -> str:
    # exor the incoming positive representation on a bit by bit basis
    #
    outstring = ''
    for i in range(0,length):
        if binstring[i] == '1':
            outstring = outstring + '0'
        else:
            outstring = outstring + '1'
    # now have inverted string need to add 1
    binstring = ''
    carry = '1'
    for i in range(0, length):
        char = outstring[(length-i-1):][0]
        if outstring[(length-i-1):][0] == '1' and carry == '1':
            # we need to reset bit and carry
            binstring = '0' + binstring
            carry = '1'
        elif outstring[(length-i-1):][0] == '0' and carry == '1':
            # found a zero bit can just put the carry in it
            binstring = '1' + binstring
            carry = '0'
        else:
            binstring = outstring[(length-i-1):][0] + binstring

    return binstring

def do_4() -> str:
    # now create a binary payload for Base Station, this will be encoded as a last step

    binary_payload = '00010000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    utc_year = input('Enter UTC Year 4 digits - default 0 - Not Available')
    if len(utc_year) == 0:
        utc_year = '0'
    binary_payload = binary_payload + '{:014b}'.format(int(utc_year))

    utc_month = input('Enter UTC Month 2 digits - default 0 - Not Available')
    if len(utc_month) == 0 or not (1 <= int(utc_month) <= 12):
        utc_month = '0'
    binary_payload = binary_payload + '{:04b}'.format(int(utc_month))

    utc_day = input('Enter UTC Day 2 digits - default 0 - Not Available')
    if len(utc_day) == 0 or not (1 <= int(utc_day) <= 31):
        utc_day = '0'
    binary_payload = binary_payload + '{:05b}'.format(int(utc_day))

    utc_hour = input('Enter UTC Hour 2 digits - default 24 - Not Available')
    if len(utc_hour) == 0 or not (1 <= int(utc_hour) <= 23):
        utc_hour = '24'
    binary_payload = binary_payload + '{:05b}'.format(int(utc_day))

    utc_minute = input('Enter UTC Minute 2 digits - default 60 - Not Available')
    if len(utc_minute) == 0 or not (1 <= int(utc_minute) <= 59):
        utc_minute = '60'
    binary_payload = binary_payload + '{:06b}'.format(int(utc_minute))

    utc_second = input('Enter UTC Second 2 digits - default 60 - Not Available')
    if len(utc_second) == 0 or not (1 <= int(utc_second) <= 59):
        utc_second = '60'
    binary_payload = binary_payload + '{:06b}'.format(int(utc_second))

    fix_quality = input("Input Fix Quality 0/1 - default = 0 ")
    if len(fix_quality) == 0 or not (fix_quality in [0, 1]):
        fix_quality = '0'

    binary_payload = binary_payload + '{:01b}'.format(int(fix_quality))

    longitude, latitude = longlat()

    binary_payload = binary_payload + longitude + latitude

    epfd_type = input("Enter EPFD Type range 0-8 default 0 (undefined) ")
    if len(epfd_type) == 0 or not (epfd_type in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
        epfd_type = '0'

    binary_payload = binary_payload + '{:04b}'.format(int(epfd_type))

    # 10 bits spare + raim flag 0 + SOTDMA (Radio) Status
    binary_payload = binary_payload + '0000000000' + '0' + '0000000000000000000'

    # veracity check print out payload length
    print("Having created Type 4 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def do_5() -> str:
    diction = AISDictionaries()

    # now create a binary payload for Base Station, this will be encoded as a last step

    binary_payload = '00010100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    ais_version = input('Enter AIS Version - default 0 ')
    if len(ais_version) == 0 or not (ais_version in [0, 1, 2, 3]):
        ais_version = '0'
    binary_payload = binary_payload + '{:02b}'.format(int(ais_version))

    imo_number = input('Enter IMO Number - up to 7 digits - Not Available')
    if len(imo_number) == 0:
        imo_number = '9999999'
    binary_payload = binary_payload + '{:030b}'.format(int(imo_number))

    callsign = input('Enter Callsign 7 characters')
    if len(callsign) == 0 or len(callsign) > 7:
        callsign = 'U/AVAIL'
        print('len callsign bits = ', len(diction.char_to_binary(callsign)))
    while len(callsign) < 7:
        callsign = callsign + '@'
    binary_payload = binary_payload + diction.char_to_binary(callsign)

    vessel_name = input('Enter Vessel Name 20 characters')
    if len(vessel_name) == 0 or len(vessel_name) > 20:
        vessel_name = 'NOT SPECIFIED@@@@@@@'
    while len(vessel_name) < 20:
        vessel_name = vessel_name + '@'
    print('len vessel name bits = ', len(diction.char_to_binary(vessel_name)))
    binary_payload = binary_payload + diction.char_to_binary(vessel_name)

    ship_type = input('Enter Ship Type - 0-99, default 0 ')
    if len(ship_type) == 0 or not (1 <= int(ship_type) <= 99):
        ship_type = '0'
    binary_payload = binary_payload + '{:08b}'.format(int(ship_type))

    dim_to_bow = input('Enter Dimension to Bow - max 511, default 0')
    if len(dim_to_bow) == 0 or not (1 <= int(dim_to_bow) <= 511):
        dim_to_bow = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_bow))

    dim_to_stern = input('Enter Dimension to Stern - max 511, default 0')
    if len(dim_to_stern) == 0 or not (1 <= int(dim_to_stern) <= 511):
        dim_to_stern = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_stern))

    dim_to_port = input('Enter Dimension to Port - max 511, default 0')
    if len(dim_to_port) == 0 or not (1 <= int(dim_to_port) <= 63):
        dim_to_port = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_port))

    dim_to_stbd = input('Enter Dimension to Starboard - max 511, default 0')
    if len(dim_to_stbd) == 0 or not (1 <= int(dim_to_stbd) <= 63):
        dim_to_stbd = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_stbd))

    epfd_type = input("Enter EPFD Type range 0-8 default 0 (undefined) ")
    if len(epfd_type) == 0 or not (epfd_type in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
        epfd_type = '0'

    binary_payload = binary_payload + '{:04b}'.format(int(epfd_type))

    eta_month = input('Enter ETA Month - default 0 - Not Available')
    if len(eta_month) == 0 or not (1 <= int(eta_month) <= 12):
        eta_month = '0'
    binary_payload = binary_payload + '{:04b}'.format(int(eta_month))

    eta_day = input('Enter ETA Day - default 0 - Not Available')
    if len(eta_day) == 0 or not (1 <= int(eta_day) <= 31):
        eta_day = '0'
    binary_payload = binary_payload + '{:05b}'.format(int(eta_day))

    eta_hour = input('Enter ETA Hour - default 0 - Not Available')
    if len(eta_hour) == 0 or not (1 <= int(eta_hour) <= 23):
        eta_hour = '24'
    binary_payload = binary_payload + '{:05b}'.format(int(eta_hour))

    eta_minute = input('Enter ETA Minute - default 0 - Not Available')
    if len(eta_minute) == 0 or not (1 <= int(eta_minute) <= 59):
        eta_minute = '60'
    binary_payload = binary_payload + '{:06b}'.format(int(eta_minute))

    draught = input("Input Draught - default = 0 ")
    if len(draught) == 0:
        draught = '0'

    binary_payload = binary_payload + '{:08b}'.format(int(draught) * 10)

    destination = input("Enter Destination max 20 Chars - UPPER CASE ")

    if len(destination) == 0 or len(destination) > 20:
        destination = 'UNKNOWN DESTiNATION@@'

    destination = destination.upper()[0:20]
    print('len destination bits = ', len(diction.char_to_binary(destination)))
    while len(destination) < 20:
        destination = destination + '@'
    binary_payload = binary_payload + diction.char_to_binary(destination)


    # set DTE bit to 0 and add a spare bit
    binary_payload = binary_payload + '00'

    # veracity check print out payload length
    print("Having created Type 4 fields payload length expected 424 got ", len(binary_payload))
    if len(binary_payload) != 424:
        print("ERROR wrong length")

    return binary_payload


def do_9() -> str:
    diction = AISDictionaries()

    # now create a binary payload for SAR Aircraft, this will be encoded as a last step

    binary_payload = '00100100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    altitude = input('Enter Altitude - max 4095 ')
    if len(altitude) == 0 or not (0 <= int(altitude) <= 4095):
        altitude = '1000'
    binary_payload = binary_payload + '{:012b}'.format(int(altitude))

    speed_over_ground = input('Enter Speed Over Ground max 1022')
    if len(speed_over_ground) == 0 or not (0 <= int(speed_over_ground) <= 1022):
        speed_over_ground = '1023'
    binary_payload = binary_payload + '{:010b}'.format(int(speed_over_ground))

    # set position accuracy bit to 0
    binary_payload = binary_payload + '0'

    binlong, binlat = longlat()

    binary_payload = binary_payload + binlong + binlat

    # course_over_ground = input('Enter Course Over Ground 0-359 ')
    # if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
    #     course_over_ground = '0'
    # binary_payload = binary_payload + '{:012b}'.format(int(course_over_ground*10))

    course_over_ground = input("Enter course over ground range 0-359 default 360 = ")
    if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
        course_over_ground = '360'
    binary_payload = binary_payload + '{:012b}'.format(int(course_over_ground) * 10)

    # set timestamp to 0 , regional reserved to 0 , DTE to 0 plus 3 spare
    binary_payload = binary_payload + '000000' + '00000000' + '0' + '000'

    assigned = input('Enter Assigned Flag 0/1 ')
    if len(assigned) == 0 or not (assigned in [0, 1]):
        assigned = '0'
    binary_payload = binary_payload + '{:01b}'.format(int(assigned))

    # set RAIM bit to 0 and add radio bits
    binary_payload = binary_payload + '0' + '00000000000000000000'

    # veracity check print out payload length
    print("Having created Type 4 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def do_12() -> str:
    diction = AISDictionaries()

    # now create a binary payload for Addressed Safety, this will be encoded as a last step

    binary_payload = '00110000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set sequence number to 0
    binary_payload = binary_payload + '00'

    destmmsi = input('Enter Destination MMSI - 9 digits, default 503123456 = ')
    if len(destmmsi) == 0:
        destmmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(destmmsi[0:9]))

    # set retransmit flag to 0 and add spare bit
    binary_payload = binary_payload + '0' + '0'

    text = input("Enter Safety Text - max 156 chars upper case")
    if len(text) == 0:
        text = 'INVALID TEXT'
    elif len(text) > 156:
        text = text[0:156]

    while len(text) < 50:
        text = text + '@'

    text = text.upper()[0:]
    binary_payload = binary_payload + diction.char_to_binary(text)

    # veracity check print out payload length
    print(f'Having created Type 4 fields payload length expected {(72 + len(text)*6)} got {len(binary_payload)}')
    if len(binary_payload) != (72 + len(text)*6):
        print("ERROR wrong length")

    return binary_payload


def do_14() -> str:
    diction = AISDictionaries()

    # now create a binary payload for Broadcast Safety, this will be encoded as a last step

    binary_payload = '00111000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set  spare bits
    binary_payload = binary_payload + '00'

    text = input("Enter Safety Text - max 156 chars upper case\n")
    if len(text) == 0 :
        text = 'INVALID TEXT'
    elif len(text) > 161:
        print('Truncating text to limit of 161 chars')
        text = text[0:161]

    while len(text) < 50:
        text = text + '@'

    text = text.upper()[0:]
    print(f'text input = {text}')
    binary_payload = binary_payload + diction.char_to_binary(text)

    # veracity check print out payload length
    print(f"Having created Type 14 fields payload length expected {41+len(text)*6} got {len(binary_payload)}" )
    if len(binary_payload) != (41+len(text)*6):
        print("ERROR wrong length")

    return binary_payload


def do_18() -> str:

    # now create a binary payload for Class B Posn, this will be encoded as a last step

    binary_payload = '01001000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set regional reserved bits to 0
    binary_payload = binary_payload + '00000000'

    speed_over_ground = input('Enter Speed over ground range 0-102 knots default 102.2 = ')
    if len(speed_over_ground) == 0:
        speed_over_ground = '5'
    int_speedoverground = int(float(speed_over_ground) * 10)
    binary_payload = binary_payload + '{:010b}'.format(int_speedoverground)

    # set position accuracy bit to 0
    binary_payload = binary_payload + '0'

    binlong, binlat = longlat()
    binary_payload = binary_payload + binlong + binlat

    course_over_ground = input("Enter course over ground range 0-359 default 360 = ")
    if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
        course_over_ground = '360'
    binary_payload = binary_payload + '{:012b}'.format(int(course_over_ground) * 10)

    true_heading = input("True heading range 0-259 default 360 = ")
    if len(true_heading) == 0 or not (0 <= int(true_heading) <= 359):
        true_heading = '360'
    binary_payload = binary_payload + '{:09b}'.format(int(true_heading))

    # setr timnestamp to 0 and regional reserved bits + CS Unit Flag + Display Flag
    binary_payload = binary_payload + '000000' + '00' + '0' + '0'

    # set DSC Flag to 0, Band Flag to 0, MEssage22 Flag to 0, Assigned Flag to 0, RAIM Flag to 0
    binary_payload = binary_payload + '0' + '0' + '0' + '0' + '0'

    # add Radio Bits
    binary_payload = binary_payload + '00000000000000000000'
    print(binary_payload)

    # veracity check print out payload length
    print("Having created Type 123 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def do_19() -> str:

    # now create a binary payload for Class B Extended, this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01001100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set regional reserved bits to 0
    binary_payload = binary_payload + '00000000'

    speed_over_ground = input('Enter Speed over ground range 0-102 knots default 102.2 = ')
    if len(speed_over_ground) == 0:
        speed_over_ground = '5'
    int_speedoverground = int(float(speed_over_ground) * 10)
    binary_payload = binary_payload + '{:010b}'.format(int_speedoverground)

    # set position accuracy bit to 0
    binary_payload = binary_payload + '0'

    binlong, binlat = longlat()
    binary_payload = binary_payload + binlong + binlat

    course_over_ground = input("Enter course over ground range 0-359 default 360 = ")
    if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
        course_over_ground = '360'
    binary_payload = binary_payload + '{:012b}'.format(int(course_over_ground) * 10)

    true_heading = input("True heading range 0-259 default 360 = ")
    if len(true_heading) == 0 or not (0 <= int(true_heading) <= 359):
        true_heading = '360'
    binary_payload = binary_payload + '{:09b}'.format(int(true_heading))

    # setr timestamp to 0 and regional reserved bits
    binary_payload = binary_payload + '000000' + '0000'

    text = input("Enter Vessel Name 20 chars upper case")
    if len(text) == 0 or len(text) > 20:
        text = 'INVALID TEXT'

    while len(text) < 20:
        text = text + '@'

    text = text.upper()[0:20]
    binary_payload = binary_payload + diction.char_to_binary(text)
    print("len name", len(text))

    ship_type = input('Enter Ship Type - 0-99, default 0 ')
    if len(ship_type) == 0 or not (1 <= int(ship_type) <= 99):
        ship_type = '0'
    binary_payload = binary_payload + '{:08b}'.format(int(ship_type))

    dim_to_bow = input('Enter Dimension to Bow - max 511, default 0')
    if len(dim_to_bow) == 0 or not (1 <= int(dim_to_bow) <= 511):
        dim_to_bow = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_bow))

    dim_to_stern = input('Enter Dimension to Stern - max 511, default 0')
    if len(dim_to_stern) == 0 or not (1 <= int(dim_to_stern) <= 511):
        dim_to_stern = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_stern))

    dim_to_port = input('Enter Dimension to Port - max 511, default 0')
    if len(dim_to_port) == 0 or not (1 <= int(dim_to_port) <= 63):
        dim_to_port = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_port))

    dim_to_stbd = input('Enter Dimension to Starboard - max 511, default 0')
    if len(dim_to_stbd) == 0 or not (1 <= int(dim_to_stbd) <= 63):
        dim_to_stbd = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_stbd))

    epfd_type = input("Enter EPFD Type range 0-8 default 0 (undefined) ")
    if len(epfd_type) == 0 or not (epfd_type in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
        epfd_type = '0'
    binary_payload = binary_payload + '{:04b}'.format(int(epfd_type))


    # set  RAIM Flag to 0, DTE Flag to 0, assigned flag to 0 and four spare bits
    binary_payload = binary_payload + '0' + '0' + '0' + '0000'

    # veracity check print out payload length
    print("Having created Type 19 fields payload length expected 312 got ", len(binary_payload))
    if len(binary_payload) != 312:
        print("ERROR wrong length")

    return binary_payload


def do_21() -> str:
    # now create a binary payload for Aid to Nav, this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01010100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    aid_type = input("Enter Aid Type 0-31 numeric ")
    if len(aid_type) == 0 or not (0 <= int(aid_type) <= 31):
        aid_type = '0'
    binary_payload = binary_payload + '{:05b}'.format(int(aid_type))


    text = input("Enter Vessel Name 20 chars upper case")
    if len(text) == 0 or len(text) > 20:
        text = 'INVALID TEXT'

    while len(text) < 20:
        text = text + '@'

    text = text.upper()[0:20]
    binary_payload = binary_payload + diction.char_to_binary(text)
    print("len name", len(text))

    # set position accuracy bit to 0
    binary_payload = binary_payload + '0'

    binlong, binlat = longlat()
    binary_payload = binary_payload + binlong + binlat
    print("len long, lat", len(binlong), len(binlat))

    dim_to_bow = input('Enter Dimension to Bow - max 511, default 0')
    if len(dim_to_bow) == 0 or not (1 <= int(dim_to_bow) <= 511):
        dim_to_bow = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_bow))

    dim_to_stern = input('Enter Dimension to Stern - max 511, default 0')
    if len(dim_to_stern) == 0 or not (1 <= int(dim_to_stern) <= 511):
        dim_to_stern = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_stern))

    dim_to_port = input('Enter Dimension to Port - max 511, default 0')
    if len(dim_to_port) == 0 or not (1 <= int(dim_to_port) <= 63):
        dim_to_port = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_port))

    dim_to_stbd = input('Enter Dimension to Starboard - max 511, default 0')
    if len(dim_to_stbd) == 0 or not (1 <= int(dim_to_stbd) <= 63):
        dim_to_stbd = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_stbd))

    epfd_type = input("Enter EPFD Type range 0-8 default 0 (undefined) ")
    if len(epfd_type) == 0 or not (epfd_type in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
        epfd_type = '0'
    binary_payload = binary_payload + '{:04b}'.format(int(epfd_type))

    # set UTC second to 0, offposition to 0, 8 reserved bits, raim flag, vitual aid flag, assigned flag plus spare bit

    binary_payload = binary_payload + '000000' + '0'  + '00000000' + '0' + '0' + '0' + '0'

    text = input("Enter Extended Vessel Name 15 chars upper case")
    if len(text) == 0 or len(text) > 15:
        text = 'EXTN TEXT'

    while len(text) < 15:
        text = text + '@'

    text = text.upper()[0:15]
    binary_payload = binary_payload + diction.char_to_binary(text)








    # veracity check print out payload length
    print("Having created Type 19 fields payload length expected 362 got ", len(binary_payload))
    if len(binary_payload) != 362:
        print("ERROR wrong length")

    return binary_payload

def do_24():
    whichone = input("Which TYpe of Type 24 A or B or C (type B non_auxiallry) - null gives Type B ")
    if len(whichone) == 0 or not (whichone in ['A', 'B', 'C']):
        whichone = 'B'

    if whichone == 'B':
        binpayload = do_24B()
    elif whichone == 'C':

        binpayload = do_24C()
    else:
        binpayload = do_24A()

    return binpayload



def do_24A() -> str:
    # now create a binary payload for Static Data REport TYpe A, this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01100000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set part number to 0 (A)
    binary_payload = binary_payload + '00'

    text = input("Enter Vessel Name 20 chars upper case")
    if len(text) == 0 or len(text) > 20:
        text = 'INVALID TEXT'

    while len(text) < 20:
        text = text + '@'

    text = text.upper()[0:20]
    binary_payload = binary_payload + diction.char_to_binary(text)
    print("len name", len(text))

    # and 8 spare bits to pad
    binary_payload = binary_payload + '00000000'

    # veracity check print out payload length
    print("Having created Type 19 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def do_24B() -> str:
    # now create a binary payload for Static Data REport TYpe B, this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01100000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set part number to 1 (B)
    binary_payload = binary_payload + '01'

    ship_type = input('Enter Ship Type - 0-99, default 0 ')
    if len(ship_type) == 0 or not (1 <= int(ship_type) <= 99):
        ship_type = '0'
    binary_payload = binary_payload + '{:08b}'.format(int(ship_type))

    text = input("Enter Vendor ID 3 chars upper case")
    if len(text) == 0 or len(text) > 3:
        text = 'VEN'

    while len(text) < 3:
        text = text + '@'

    text = text.upper()[0:3]
    binary_payload = binary_payload + diction.char_to_binary(text)

    unit_model_code = input('Enter Unit Model Code 0-15, default 0')
    if len(unit_model_code) == 0 or not (0 <= int(unit_model_code) <= 15):
        unit_model_code = '15'
    binary_payload = binary_payload + '{:04b}'.format(int(unit_model_code))

    serial_number = input('Enter Serial Number maximum 1048575 , default 0')
    if len(serial_number) == 0 or int(serial_number) > 1048575:
        serial_number = '99999'
    binary_payload = binary_payload + '{:020b}'.format(int(serial_number[0:7]))

    callsign = input('Enter Callsign 7 characters')
    if len(callsign) == 0 or len(callsign) > 7:
        callsign = 'U/AVAIL'
    while len(callsign) < 7:
        callsign = callsign + '@'
    binary_payload = binary_payload + diction.char_to_binary(callsign)

    dim_to_bow = input('Enter Dimension to Bow - max 511, default 0')
    if len(dim_to_bow) == 0 or not (1 <= int(dim_to_bow) <= 511):
        dim_to_bow = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_bow))

    dim_to_stern = input('Enter Dimension to Stern - max 511, default 0')
    if len(dim_to_stern) == 0 or not (1 <= int(dim_to_stern) <= 511):
        dim_to_stern = '0'
    binary_payload = binary_payload + '{:09b}'.format(int(dim_to_stern))

    dim_to_port = input('Enter Dimension to Port - max 511, default 0')
    if len(dim_to_port) == 0 or not (1 <= int(dim_to_port) <= 63):
        dim_to_port = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_port))

    dim_to_stbd = input('Enter Dimension to Starboard - max 511, default 0')
    if len(dim_to_stbd) == 0 or not (1 <= int(dim_to_stbd) <= 63):
        dim_to_stbd = '0'
    binary_payload = binary_payload + '{:06b}'.format(int(dim_to_stbd))

    # plus 6 spare bits
    binary_payload = binary_payload + '000000'

    # veracity check print out payload length
    print("Having created Type 19 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload


def do_24C():
    # now create a binary payload for Static Data REport TYpe B (auxiallry) , this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01100000'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set part number to 1 (B)
    binary_payload = binary_payload + '01'

    ship_type = input('Enter Ship Type - 0-99, default 0 ')
    if len(ship_type) == 0 or not (1 <= int(ship_type) <= 99):
        ship_type = '0'
    binary_payload = binary_payload + '{:08b}'.format(int(ship_type))

    text = input("Enter Vendor ID 3 chars upper case")
    if len(text) == 0 or len(text) > 3:
        text = 'VEN'

    while len(text) < 3:
        text = text + '@'

    text = text.upper()[0:3]
    binary_payload = binary_payload + diction.char_to_binary(text)

    unit_model_code = input('Enter Unit Model Code 0-15, default 0')
    if len(unit_model_code) == 0 or not (0 <= int(unit_model_code) <= 15):
        unit_model_code = '15'
    binary_payload = binary_payload + '{:04b}'.format(int(unit_model_code))

    serial_number = input('Enter Serial Number max , default 0')
    if len(serial_number) == 0 or int(serial_number) > 1048575:
        serial_number = '1048575'
    binary_payload = binary_payload + '{:020b}'.format(int(serial_number[0:7]))

    callsign = input('Enter Callsign 7 characters')
    if len(callsign) == 0 or len(callsign) > 7:
        callsign = 'U/AVAIL'
    while len(callsign) < 7:
        callsign = callsign + '@'
    binary_payload = binary_payload + diction.char_to_binary(callsign)

    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # plus 6 spare bits
    binary_payload = binary_payload + '000000'




    # veracity check print out payload length
    print("Having created Type 19 fields payload length expected 168 got ", len(binary_payload))
    if len(binary_payload) != 168:
        print("ERROR wrong length")

    return binary_payload
def do_27():
    # now create a binary payload for Static Data REport TYpe A, this will be encoded as a last step

    diction = AISDictionaries()

    binary_payload = '01101100'  # Message Type and Repeat Indicator
    mmsi = input('Enter MMSI - 9 digits, default 503123456 = ')
    if len(mmsi) == 0:
        mmsi = '503123456'
    binary_payload = binary_payload + '{:030b}'.format(int(mmsi))

    # set position Accuracy to 0, raim flasg to 0
    binary_payload = binary_payload + '0' + '0'

    nav_status = input('Enter Navigation Status range 0-15 default 15 ')
    if len(nav_status) == 0:
        nav_status = '15'
    binary_payload = binary_payload + '{:04b}'.format(int(nav_status))  # Navigation Status

    #binlong, binlat = longlat()
    longitude = input('Enter longitude decimal +ve West, -ve East = ')
    if len(longitude) == 0:
        longitude = '147'
    print("longitude ", longitude)
    if not (-180 <= float(longitude) <= 180):
        print("Error longitude must be between -180 and 180 set to 147.0")
        longitude = '147.0'

    intlongitude = int(float(longitude) * 600)
    if intlongitude < 0:
        binlong = '{:018b}'.format(abs(intlongitude))
        binlong = twos_comp_negation(binlong, 18)
    else:
        binlat = '{:018b}'.format(intlongitude)

    latitude = input('Enter latitude decimal +ve North, -ve South = ')
    if len(latitude) == 0:
        latitude = '38'
    if not (-90 <= float(latitude) <= 90):
        print("Error longitude must be between -180 and 180 set to -38.5")
        longitude = '-38.5'
    intlatitude = int(float(latitude) * 600)
    if intlatitude < 0:
        binlat = '{:017b}'.format(abs(intlatitude))
        binlat = twos_comp_negation(binlat, 17)
    else:
        binlat = '{:017b}'.format(intlatitude)

    binary_payload = binary_payload + binlong + binlat
    print("len long, lat", len(binlong), len(binlat))

    speed_over_ground = input('Enter Speed over ground range 0-102 knots default 102.2 = ')
    if len(speed_over_ground) == 0:
        speed_over_ground = '5'
    int_speedoverground = int(float(speed_over_ground) )
    binary_payload = binary_payload + '{:06b}'.format(int_speedoverground)

    course_over_ground = input("Enter course over ground range 0-359 default 360 = ")
    if len(course_over_ground) == 0 or not (0 <= int(course_over_ground) <= 359):
        course_over_ground = '360'
    binary_payload = binary_payload + '{:09b}'.format(int(course_over_ground) )

    # set GNSS flag to 0 and spare bit to 0
    binary_payload = binary_payload + '0' + '0'

    # veracity check print out payload length
    print("Having created Type 27 fields payload length expected 96 got ", len(binary_payload))
    if len(binary_payload) != 96:
        print("ERROR wrong length")

    return binary_payload


def main():
    AISString = ''

    fragmentcount: str = input('Input Fragment Count = ')

    if len(fragmentcount) == 0:  # null count assume 1
        fragmentcount = '1'

    fragmentnumber: str = '1'
    if fragmentcount != '1':
        print("What is number of this fragment = ")
        fragmentnumber = input()

    messageid = input("What is Message_ID default null = ")
    # may be a null entry
    if len(messageid) == 0:
        messageid = ''

    channelid = input("What channel ID = ")
    if len(channelid) == 0:
        channelid = 'A'
    while not (channelid in ['A', 'B', '1', '2']):
        print("Error Channel ID can only be A, B, 1, 2")
        print("Error Payload Type must be in 1-27 try again = ")
        channelid = input()

    # now it gets interesting constructing the payload

    payload_type = input("Input Payload Type (Numeric 1-27 = ")
    if len(payload_type) == 0:
        payload_type = '1'

    while not (0 < int(payload_type) <= 27):
        print("Error Payload Type must be in 1-27 try again = ")
        payload_type = input()
    if 6 <= int(payload_type) <= 8 \
            or 10 <= int(payload_type) <= 11 \
            or int(payload_type) == 13 \
            or 15 <= int(payload_type) <= 17 \
            or int(payload_type) == 20 \
            or 22 <= int(payload_type) <= 23 \
            or 25 <= int(payload_type) <= 26:
        print("Not yet implemented")
    elif 1 <= int(payload_type) <= 3:
        binpayload: str = do_123()
    elif int(payload_type) == 4:
        binpayload: str = do_4()
    elif int(payload_type) == 5:
        binpayload = do_5()
    elif int(payload_type) == 9:
        binpayload = do_9()
    elif int(payload_type) == 12:
        binpayload = do_12()
    elif int(payload_type) == 14:
        binpayload = do_14()
    elif int(payload_type) == 18:
        binpayload = do_18()
    elif int(payload_type) == 19:
        binpayload = do_19()
    elif int(payload_type) == 21:
        binpayload = do_21()
    elif int(payload_type) == 24:
        binpayload = do_24()
    elif int(payload_type) == 27:
        binpayload = do_27()

    print(f'{binpayload}\n{fragmentcount}\n{fragmentnumber}\n{messageid}\n{channelid}\n')

    AISString = do_encode(binpayload, fragmentcount, fragmentnumber, messageid, channelid) + ',0*5'

    print('{} \n {}'.format(binpayload, len(binpayload)))

    print(AISString)


if __name__ == ('__main__'):
    main()
