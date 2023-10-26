'''
Collection of dictionaries used throughot the application

'''


class AISDictionaries:
    '''
        Conversion from ASCII to AIS Payload Armoring
        6 bit bytes converted as per AIOVDM/AIVDO Protocol Manual
        table AIVDM/AIVDO Payload Armoring table pp4 (approx)

    '''

    payload_armour = {"0": "000000", '1': '000001', '2': '000010', '3': '000011',
                      '4': '000100', '5': '000101', '6': '000110',  '7':'000111',
                      '8': '001000', '9': '001001', ':': '001010', ';': '001011',
                      '<': '001100', '=': '001101', '>': '001110', '?': '001111',
                      '@': '010000', 'A': '010001', 'B': '010010', 'C': '010011',
                      'D': '010100', 'E': '010101', 'F': '010110', 'G': '010111',
                      'H': '011000', 'I': '011001', 'J': '011010', 'K': '011011',
                      'L': '011100', 'M': '011101', 'N': '011110', 'O': '011111',
                      'P': '100000', 'Q': '100001', 'R': '100010', 'S': '100011',
                      'T': '100100', 'U': '100101', 'V': '100110', 'W': '100111',
                      '`': '101000', 'a': '101001', 'b': '101010', 'c': '101011',
                      'd': '101100', 'e': '101101', 'f': '101110', 'g': '101111',
                      'h': '110000', 'i': '110001', 'j': '110010', 'k': '110011',
                      'l': '110100', 'm': '110101', 'n': '110110', 'o': '110111',
                      'p': '111000', 'q': '111001', 'r': '111010', 's': '111011',
                      't': '111100', 'u': '111101', 'v': '111110', 'w': '111111'
                      }

    # REVERSE LOOKUP TABLE TO CONVERT NIBBLES BACK TO ASCII TEXT

    nibble_to_text = {"000000": '@', '000001': 'A', '000010': 'B', '000011': 'C',
                      '000100': 'D', '000101': 'E', '000110': 'F', '000111': 'G',
                      '001000': 'H', '001001': 'I', '001010': 'J', '001011': 'K',
                      '001100': 'L', '001101': 'M', '001110': 'N', '001111': 'O',
                      '010000': 'P', '010001': 'Q', '010010': 'R', '010011': 'S',
                      '010100': 'T', '010101': 'U', '010110': 'V', '010111': 'W',
                      '011000': 'X', '011001': 'Y', '011010': 'Z', '011011': '[',
                      '011100': '\\', '011101': ']', '011110': '^', '011111': '_',
                      '100000': ' ', '100001': '!', '100010': '\"', '100011': '#',
                      '100100': '$', '100101': '%', '100110': '&', '100111': '\'',
                      '101000': '(', '101001': ')', '101010': '*', '101011': '+',
                      '101100': ',', '101101': '-', '101110': '.', '101111': '/',
                      '110000': '0', '110001': '1', '110010': '2', '110011': '3',
                      '110100': '4', '110101': '5', '110110': '6', '110111': '7',
                      '111000': '8', '111001': '9', '111010': ':', '111011': ';',
                      '111100': '<', '111101': '=', '111110': '>', '111111': '?'
                      }

    ch_numb_dict = {'1': 'A', '2': 'B', 'A': 'A', 'B': 'B'}

    MIDFormats: dict = {
        '8MIDXXXXX': 'Diver’s radio (not used in the U.S. in 2013)',
        'MIDXXXXXX': 'Ship',
        '0MIDXXXXX': 'Group of ships; the U.S. Coast Guard, for example, is 03699999',
        '00MIDXXXX': 'Coastal stations',
        '111MIDXXX': 'SAR (Search and Rescue) aircraft',
        '99MIDXXXX': 'Aids to Navigation',
        '98MIDXXXX': "Auxiliary craft associated with a parent ship",
        '970MIDXXX': 'AIS SART (Search and Rescue Transmitter)',
        '972XXXXXX': 'MOB (Man Overboard) device',
        '974XXXXXX': 'EPIRB (Emergency Position Indicating Radio Beacon) AIS'
    }

    Navigation_Status: dict = {
        0: 'Under way using engin',
        1: 'At anchor',
        2: 'Not under command',
        3: 'Restricted manoeuverability',
        4: 'Constrained by er draught',
        5: 'Moored',
        6: 'Aground',
        7: 'Engaged in Fishing',
        8: 'Under way sailing',
        9: 'Reserved for future amendment of Navigational Status for HSC',
        10: 'Reserved for future amendment of Navigational Status for WIG',
        11: 'Power-driven vessel towing astern (regional use)',
        12: 'Power-driven vessel pushing ahead or towing alongside (regional use)',
        13: 'Reserved for future use',
        14: 'AIS-SART is active',
        15: 'Ubdefined (default)'
    }

    Ship_Type: dict = {
        0: ' Not available(default)',
        1: ' Reservedfor future use',
        2: ' Reservedfor future use',
        3: ' Reservedfor future use',
        4: ' Reservedfor future use',
        5: ' Reservedfor future use',
        6: ' Reservedfor future use',
        7: ' Reservedfor future use',
        8: ' Reservedfor future use',
        9: ' Reservedfor future use',
        10: ' Reservedfor future use',
        11: ' Reservedfor future use',
        12: ' Reservedfor future use',
        13: ' Reservedfor future use',
        14: ' Reservedfor future use',
        15: ' Reservedfor future use',
        16: ' Reservedfor future use',
        17: ' Reservedfor future use',
        18: ' Reservedfor future use',
        19: ' Reservedfor future use',
        20: 'Wing in ground (WIG), all ships of this type ',
        21: ' Wing in ground (WIG), Hazardous category A',
        22: ' Wing in ground (WIG), Hazardous category B',
        23: ' Wing in ground (WIG), Hazardous category C',
        24: ' Wing in ground (WIG), Hazardous category D',
        25: ' Wing in ground (WIG), Reserved for future use',
        26: ' Wing in ground (WIG), Reserved for future use',
        27: ' Wing in ground (WIG), Reserved for future use',
        28: ' Wing in ground (WIG), Reserved for future use',
        29: 'Wing in ground (WIG), Reserved for future use',
        30: ' Fishing',
        31: ' Towing',
        32: ' Towing: length exceeds 200 m or breadth exceeds 25 m',
        33: ' Dredging or underwater ops',
        34: ' Diving ops',
        35: ' Military ops',
        36: ' Sailing',
        37: ' Pleasure Craft',
        38: ' Reserved',
        39: ' Reserved',
        40: ' High speed craft(HSC), all ships  of this type',
        41: ' High speed craft(HSC), Hazardous category A',
        42: ' High speed craft(HSC), Hazardous category B',
        43: ' High speed craft(HSC), Hazardous category C',
        44: ' High speed craft(HSC), Hazardous category D',
        45: ' High speed craft(HSC), Reserved for future use',
        46: ' High speed craft (HSC), Reserved for future use',
        47: ' High speed craft (HSC), Reserved for future use',
        48: ' High speed craft (HSC), Reserved for future use',
        49: ' High speed craft (HSC), No additional information',
        50: ' Pilot Vessel',
        51: ' Search and Rescue vessel',
        52: 'Tug',
        53: 'Port Tender',
        54: 'Anti-pollution equipment',
        55: 'Law Enforcement',
        56: 'Spare - Local Vessel',
        57: 'Spare - Local Vessel',
        58: 'Medical Transport',
        59: 'Noncombatant ship according to RR Resolution No.18',
        60: 'Passenger, all ships of this type',
        61: 'Passenger, Hazardous category A',
        62: 'Passenger, Hazardous category B',
        63: 'Passenger, Hazardous category C',
        64: 'Passenger, Hazardous category D',
        65: 'Passenger, Reserved for future use',
        66: 'Passenger, Reserved for future use',
        67: 'Passenger, Reserved for future use',
        68: 'Passenger, Reserved for future use',
        69: 'Passenger, No additional information',
        70: 'Cargo, all ships of this type',
        71: 'Cargo, Hazardous category A',
        72: 'Cargo, Hazardous category B',
        73: 'Cargo, Hazardous category C',
        74: 'Cargo, Hazardous category D',
        75: 'Cargo, Reserved for future use ',
        76: 'Cargo, Reserved for future use',
        77: 'Cargo, Reserved for future use  ',
        78: 'Cargo, Reserved for future use',
        79: 'Cargo, No additional information  ',
        80: 'Tanker, all ships of this type  ',
        81: 'Tanker, Hazardous category A  ',
        82: 'Tanker, Hazardous category B  ',
        83: 'Tanker, Hazardous category C  ',
        84: 'Tanker, Hazardous category D  ',
        85: 'Tanker, Reserved for future use  ',
        86: 'Tanker, Reserved for future use  ',
        87: 'Tanker, Reserved for future use  ',
        88: 'Tanker, Reserved for future use  ',
        89: 'Tanker, No additional information  ',
        90: 'Other Type, all ships of this type  ',
        91: 'Other Type, Hazardous category A  ',
        92: 'Other Type, Hazardous category B: ',
        93: 'Other Type, Hazardous category C  ',
        94: 'Other Type, Hazardous category D  ',
        95: 'Other Type, Reserved for future use  ',
        96: 'Other Type, Reserved for future use  ',
        97: 'Other Type, Reserved for future use  ',
        98: 'Other Type, Reserved for future use  ',
        99: 'Other Type, no additional inf  '
    }

    def __init__(self):
        pass
    def make_stream(self, preamlen: int, testbits: str):
        # creates a fake binary payload to allow testing
        # preamble is number number of bits needed to fill up to beginning of testbits
        # testbits is the binary stream representing the area of thge domain under test
        # a couple of 'constants'
        fakehead: str = '000100'
        faketail: str = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        # prefill the preamble with message type 4
        preamble: str = fakehead
        # fillcount is number of required prefill with allowance for the 6 bit header
        fillcount = preamlen - 6

        while fillcount > 0:
            preamble = preamble + '1'
            fillcount -= 1

        # print('in make_stream nr bits needed, nr bits offered', preamlen, len(preamble))
        return preamble + testbits + faketail

    def makebinpayload(self, binpay: str, payload_char: str) -> str:
        # print(self.payload_armour[payload_char])
        # print(payload_char,"", self.payload_armour[payload_char] )
        return binpay + self.payload_armour[payload_char]

    def get_payload_armour(self, char: str) -> str:
        # takes in character from encoded AIS stream and returns six bit binary nibble it should produce
        return self.payload_armour[char]

    def char_to_nibble(self, character: str) -> str:
        # takes in single character , return binary nibble representing the character
        # as per the Six Bit ASCII table
        # used in producing test data for the various AIS objects
        #print('in char to nibble character = ', character)
        for mykey, dictchar in self.nibble_to_text.items():

            if character == dictchar:
                return mykey

    def char_to_binary(self, character: str) -> str:
        # takes in character string , return binary string representing the character string as 6 bit nibbles
        # as per the Six Bit ASCII table
        # used in producing test data for the various AIS objects
        returnstring = ''
        #print('in char to binary input =', character)
        for sglchar in character:
            returnstring = returnstring + self.char_to_nibble(sglchar)

        return returnstring


    def binary_to_char(self, inputstring) -> str:
        # takes in six bit binary string returns character from dictionary nibble_to_text
        # used in producing text strings from the binary_payloads

        return self.nibble_to_text[inputstring]






