from unittest import TestCase


class TestPayload(TestCase):
    pass


class TestCNB(TestCase):
    pass


class TestBasestation(TestCase):
    pass


class TestBinary_addressed_message(TestCase):
    pass


class TestBinary_acknowledge(TestCase):
    pass


class TestBinary_broadcast_message(TestCase):
    pass


class TestSAR_aircraft_position_report(TestCase):
    pass


class TestUTC_date_enquiry(TestCase):
    pass


class TestUTC_date_response(TestCase):
    pass


class TestAddressed_safety_related_message(TestCase):
    pass


class TestSafety_relatyed_acknowledgement(TestCase):
    pass


class TestSafety_related_broadcast_message(TestCase):
    pass


class TestInterrogation(TestCase):
    pass


class TestDGNS_broadcast_binaty_message(TestCase):
    pass


class TestClassB_position_report(TestCase):
    pass


class TestExtende_ClassB_position_report(TestCase):
    pass


class TestData_link_management_message(TestCase):
    pass


class Test_aid_to_navigation_report(TestCase):
    pass


class TestChannel_management(TestCase):
    pass


class TestGroup_assigment_command(TestCase):
    pass


class TestStatic_data_report(TestCase):
    pass


class TestSingle_slot_binary_message(TestCase):
    pass


class TestMultiple_slot_binary_message(TestCase):
    pass


class TestLong_range_AIS_broadcast_message(TestCase):
    pass


class TestFragments(TestCase):
    def test_extract_mmsi(self):
        self.fail()

    def test_binary_item(self):
        self.fail()

    def test_put_frag_in_dict(self):
        self.fail()

    def test_match_fragments(self):
        self.fail()
