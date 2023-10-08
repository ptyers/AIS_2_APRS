class FRAGMENT:
    #  used to store fragmented messages prior to invoking AIS_data
    #  stashes away the seven comma seperated fields of the incoming stream
    #  and are stored in a Dictionary with the key being the fragment number
    #  nominally the message id should be used to recombine thye data but from
    #  data seen this does not remain coinstant over fragments of the same message
    #
    p_talker = ""
    p_fragcount = "0"
    p_fragno = "0"
    p_messid = ""
    p_channel = ""
    p_payload = ""
    p_trailer = ""

    def __init__(self, inputstring: str, **kwargs):
        #  split the incoming data into discrete strings
        discrete_items = inputstring.split(",")
        p_talker = discrete_items[0]
        self.p_fragcount = discrete_items[1]
        self.p_fragno = discrete_items[2]
        self.p_messid = discrete_items[3]
        self.p_channel = discrete_items[4]
        self.p_payload = discrete_items[5]
        self.p_trailer = discrete_items[6]

        """
        then start iterating down the argument list 
        position in call determines which parameter is to be initialised
        a dictionary using the position count returns a function against
        which the matching value is to be used
        """
        for keyword, value in kwargs.items():
            # do_function(keyword, kwargs[keyword])
            self.do_function(keyword, value)

    def do_function(self, keyword, value):
        # create a dictionary of functions related to keywords that might be being initialised
        Funcdict = {
            "Talker": self.set_Talker,
            "Fragcount": self.set_FragCount,
            "Fragno": self.set_Fragno,
            "Message_ID": self.set_Message_ID,
            "Channel": self.set_Channel,
            "Payload": self.set_Payload,
            "Trailer": self.set_Trailer,
        }
        if keyword in Funcdict:
            return Funcdict[keyword](value)
        else:
            raise (ValueError, "parameter name unknown")

    def set_Talker(self, value):
        if isinstance(value, str):
            self.p_talker = value
        else:
            self.p_talker = ""
            raise TypeError("Talker must be string")

    def get_Talker(self):
        return self.p_talker

    Talker = property(get_Talker, set_Talker)

    def set_FragCount(self, value):
        if isinstance(value, int):
            self.p_fragcount = value
        else:
            self.p_fragcount = 0
            raise TypeError("FragCount must be int")

    def get_FragCount(self) -> str:
        return self.p_fragcount

    FragCount = property(get_FragCount, set_FragCount)

    def get_IntFragCount(self) -> int:
        return int(self.p_fragcount)

    IntFragCount = property(get_IntFragCount)

    def set_Fragno(self, value):
        if isinstance(value, int):
            self.p_fragno = value
        else:
            self.p_fragno = ""
            raise TypeError("Fragno must be int")

    def get_Fragno(self) -> str:
        return self.p_fragno

    FragNo = property(get_Fragno, set_Fragno)

    def get_IntFragNo(self) -> int:
        return int(self.p_fragno)

    IntFragNo = property(get_IntFragNo)

    def set_Message_ID(self, value):
        if isinstance(value, str):
            self.p_messid = value
        else:
            self.p_messid = ""
            raise TypeError("Message_ID must be string")

    def get_Message_ID(self):
        return self.p_messid

    Message_ID = property(get_Message_ID, set_Message_ID)

    def set_Channel(self, value):
        if isinstance(value, str):
            self.p_channel = value
        else:
            self.p_channel = ""
            raise TypeError("Channel must be string")

    def get_Channel(self):
        return self.p_channel

    Channel = property(get_Channel, set_Channel)

    def set_Payload(self, value):
        if isinstance(value, str):
            self.p_payload = value
        else:
            self.p_payload = ""
            raise TypeError("Payload must be string")

    def get_Payload(self):
        return self.p_payload

    PayLoad = property(get_Payload, set_Payload)

    def set_Trailer(self, value):
        if isinstance(value, str):
            self.p_trailer = value
        else:
            self.p_trailer = ""
            raise TypeError("Trailer must be string")

    def get_Trailer(self):
        return self.p_trailer

    Trailer = property(get_Trailer, set_Trailer)

    def FillBits(self) -> int:
        return int(self.p_trailer[0:1])

    def ValidBits(self) -> int:
        return 6 - int(self.p_trailer[0:1])
