'''
Group of Classes covering all breeds of payloads

Base Class is Payload all other classes inherit from this

'''
from datetime import datetime, timezone
import logging
from GlobalDefinitions import Global


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


class Fragments:
    #
    # class to allow handling of fragments
    # input parameter message is the whole AIS string to be split to alllow consolidation of
    # payloads
    # as well as the normal payload it uses the fragment_count, fragment_number fields

    # if a stream with fragment count > 1 found pass it to this and hopefully when enough
    # portions are found a success = True (1) will be returned and a merged payload and payload_length will be valid
    # using fragment_number can detyect if all fragments are available before merging.
    # a cleanm up will also be done to flush out stale fragments from Fragment Dictionary.
    #       Timeout set in Global_Parameters
    #

    current_time: datetime
    payload: str
    mmnsi: str
    f_no: int
    f_count: int
    messid: int
    ftuple: tuple
    success: bool
    new_bin_payload: str




    def __init__(self, binary_payload: str, fragment_count: int, fragment_number: int, message_id: int):

        current_time =  datetime.utcnow()
        f_count = fragment_count
        f_no = fragment_number
        messid = message_id
        payload = binary_payload
        ftuple = [f_count, f_no, messid, payload, current_time]
        inkey: str
        rtime: datetime
        success = False
        new_bin_payload = ''

        pass

    def put_frag_in_dict(self):
        # create a dictionary key comprising fragment_number and message_id
        key = str(self.f_no) + '-' + str(self.messid)
        Global.FragDict.update(key, self.ftuple)
        logging.debug('In Fragment.put_frag_in_dict dictionary  = ', Global.FragDict)

        pass

    def match_fragments(self, key: str):
        # pass through Global.Fragdict looking for identical keys
        inkey = key
        rtime = datetime.now()
        fraglist = []
        for fkey, ftuple in Global.FragDict.items():
            if fkey == key:
                fraglist.extend(ftuple)
            #
            # now while we are parsing dictionary clean out stale records
            if (datetime.utcnow() - ftuple[4]).total_seconds() > Global.FragDictTTL:
                Global.FragDict.pop(fkey)

        # how many records did we find?

        nr_recs = len(fraglist)

        # compare this with the number of fragments expected
        if nr_recs == self.f_count:
        # got requisite number of fragments
        # get fragments in order
            lump = 1
            while lump <= nr_recs:
                for ftuple in fraglist:
                    if ftuple[1] == 1:
                        self.new_bin_payload = ftuple[3]
                    elif  ftuple[1] == lump:
                        self.new_bin_payload = self.new_bin_payload + ftuple[3]
                lump += 1
            self.success = True
        else:
            # not got all bits yet
            pass

        return self.success , self.new_bin_payload
