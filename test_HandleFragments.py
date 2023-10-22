from unittest import TestCase
from  AISData import AIS_Data
from AISDictionary import AISDictionaries
import logging
import HandleFragments


class Test(TestCase):

    logging.basicConfig(filename='myapp.log', level=logging.CRITICAL)

    # two AIS streams which are a fragmented message
    mytestdata = [
        '!AIVDM,2,1,7,A,57Oi`:021ssqHiL6221L4l8U8V2222222222220l1@F476Ik0;QA1C`88888,0*1E',
        '!AIVDM,2,2,7,A,88888888888,2*2B'
    ]

    def initialise(self):
        diction = AISDictionaries()
        mydata = AIS_Data(
            "!AIVDM", "1", "1", "", "A",
            "17P1cP0P0l:eoREbNV4qdOw`0PSA", "0*18\r\n"
        )
        return diction, mydata
    def test_handle_fragments(self):
        print('Testing Handle Fragments')
        diction, mydata = self.initialise()

        for payload in self.mytestdata:
            HandleFragments.handle_fragments(payload)






        self.fail()
