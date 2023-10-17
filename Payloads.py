'''
Group of Classes covering all breeds of payloads

Base Class is Payload all other classes inherit from this

'''

class Payload:
    # fields
    message_type: int
    repeat_indicator: int
    mmsi: str
    longitude: int
    latitude: int
    raim_flag: int
    radio_status: int = 0  # Not implemented







    def __init__(self, p_payload: str):

        pass

class CNB(Payload):
    # additional fields

    navigation_status: int
    rate_of_turn: int
    speed_over_ground: int
    position_accuracy: int
    course_over_ground: float
    true_heading: int
    time_stamp: int
    maneouver_indicator: int
    raim_flag: int


    def __init__(self, p_payload: str):
        super().__init__(p_payload)

        pass

class Basestation(Payload):
    # base station report - Type 4

    # items specific to base station
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    EPFD_type: int


    def __init__(self, p_payload: str):
        super().__init__(p_payload)

        pass

class Binary_addressed_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass


class Binary_acknowledge(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass


class Binary_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass



class SAR_aircraft_position_report(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass


class UTC_date_enquiry(Payload):
    # to be implemented

    def __init__(self, p_payload):
        super().__init__(p_payload)


class UTC_date_response(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Addressed_safety_related_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass


class Safety_relatyed_acknowledgement(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Safety_related_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass
class Interrogation(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class DGNS_broadcast_binaty_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class ClassB_position_report(Payload):
    # to be implemented
    # type 18

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass


class Extende_ClassB_position_report(Payload):
    # to be implemented
    # type 19

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass
class Data_link_management_message(Payload):
    # to be implemented
    # type 20

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Aid_to_navigation_report(Payload):
    # to be implemented
    # type 21

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Channel_management(Payload):
    # to be implemented
    # type 22

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Group_assigment_command(Payload):
    # to be implemented
    # type 23

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Static_data_report(Payload):
    # to be implemented
    # type 24

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Single_slot_binary_message(Payload):
    # to be implemented
    # type 25

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

class Multiple_slot_binary_message(Payload):
    # to be implemented
    # type 26

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass
class Long_range_AIS_broadcast_message(Payload):
    # to be implemented

    def __init__(self, p_payload)
        super().__init__(p_payload)

        pass

