from unittest import TestCase
from AISData import AIS_Data
from AISDictionary import AISDictionaries


class TestAIS_Data(TestCase):
    '''
    block of strings to get test data
    '''

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

    def test_print_ais(self):
        self.fail()

    def test_m_initialise(self):
        self.fail()

    def test_m_setup(self):
        self.fail()

    def test_extract_string(self):
        self.fail()

    def test_extract_int(self):
        self.fail()

    def test_binary_item(self):
        for i in range(5):
            payload = self.mytestdata[i].split(',')
            self._binary_payload, self.binlen = AIS_Data.create_binary_payload(payload[5])

            #print(self._binary_payload)

            intmmsi = AIS_Data.Binary_Item(self, 8,30)
            #print(intmmsi)




    def test_create_binary_payload(self):
        dict = AISDictionaries()
        print('Testing create_binary_payload')
        for i in range(5):
            self.testpay: str = ''
            payload = self.mytestdata[i].split(',')
            self.binpay, self.binlen = AIS_Data.create_binary_payload(payload[5])
            for char in payload[5]:
                self.testpay = AISDictionaries.makebinpayload(dict, self.testpay, char)

            self.assertEqual(self.binpay, self.testpay, "Create binary payload failure")

        print('Succeeded')


    def test_create_bytearray_payload(self):
        self.fail()

    def test_m_to_int(self):
        self.fail()

    def test_remove_at(self):
        self.fail()

    def test_remove_space(self):
        self.fail()

    def main(self):
        self.test_create_binary_payload()
        pass

    if __name__ == "main":
        main()
