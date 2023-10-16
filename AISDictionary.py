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
                      '4': '000100', '5': '000101', '6': '000110', '7': '000111',
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
        0: 'Under way using engin', 1: 'At anchor',
        2: 'Not under command',
        3: 'Restricted manoeuverability',
        4: 'Constrained by er draught',
        5:  'Moored',
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


    def __init__(self):
        pass


    def makebinpayload(self, binpay: str, payload_char: str) -> str:

        #print(self.payload_armour[payload_char])
        #print(payload_char,"", self.payload_armour[payload_char] )
        return binpay + self.payload_armour[payload_char]

    def get_payload_armour(self,char: str) -> str:
        return self.payload_armour[char]
