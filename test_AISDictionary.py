from unittest import TestCase
from AISDictionary import AISDictionaries


class TestAISDictionaries(TestCase):
    def test_make_stream(self):
        self.fail()

    def test_makebinpayload(self):
        self.fail()

    def test_get_payload_armour(self):
        self.fail()

    def test_char_to_binary(self):
        # take in single text character and compares to nibble
        # sequences through dictionary nibble_to_text
        diction = AISDictionaries()

        for nibble, text in diction.nibble_to_text.items():
            print('test char -> binary nibble text', nibble, text)
            outstring = diction.char_to_binary(text)
            self.assertEqual(nibble, outstring, "Failed in char_to_binary")


    def test_binary_to_char(self) -> str:
        # take in binary nibble and present single text character back
        # sequences through dictionary nibble_to_text
        diction = AISDictionaries()
        for nibble,text in diction.nibble_to_text.items():
            print('test binary -> char nibble text', nibble, text)
            outstring = diction.binary_to_char(nibble)
            self.assertEqual(text, outstring, "Failed in binary_to_char")




