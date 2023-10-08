from datetime import datetime


class MAPPER:
    #  used to map MMSI to callsign,Name, Destination
    #  uses Dictionary MyMapper with key MMSI
    # region def Properties
    _callsign = ""
    _name = ""
    _destination = ""
    _type = 0  # not available
    _vendor = ""  # 3 chars
    _model = 0
    _serial = 0
    _d2bow = 0
    _d2stern = 0
    _d2port = 0
    _d2starboard = 0
    _mother = 0  # this field is open to interpretation - definition is confused 30 bits
    _killsent = False
    _timestamp = None

    # endregion
    # region def Properties

    def __init__(self, Callsign: str, Name: str, Destination: str):
        self._callsign = Callsign
        self._name = Name
        self._destination = Destination
        self._killsent = False
        self._timestamp = datetime.now()

    def set_kill_sent(self, value):
        self._killsent = value

    def get_kill_sent(self):
        return self._killsent

    KillSent = property(get_kill_sent, set_kill_sent)

    def set_Callsign(self, value):
        if isinstance(value, str):
            self._callsign = value
        else:
            self._callsign = ""
            raise (TypeError, "Callsign must be string ")

    def get_Callsign(self):
        return self._callsign

    Callsign = property(get_Callsign, set_Callsign)

    def set_Name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            self._name = ""
            raise (TypeError, "Name must be string ")

    def get_Name(self):
        return self._name

    Name = property(get_Name, set_Name)

    def set_Destination(self, value):
        if isinstance(value, str):
            self._destination = value
        else:
            self._destination = ""
            raise (TypeError, "Destination must be string ")

    def get_Destination(self):
        return self._destination

    Destination = property(get_Destination, set_Destination)

    def get_ShipType(self) -> int:
        return self._type

    def set_ShipType(self, value):
        if isinstance(value, int):
            self._type = value
        else:
            self._type = 0
            raise (ValueError, " Type error ShipType must be a int")

    ShipType = property(get_ShipType, set_ShipType)

    def get_Vendor(self) -> str:
        return self._vendor

    def set_Vendor(self, value):
        if isinstance(value, str):
            self._vendor = value
        else:
            self._vendor = ""
            raise (ValueError, " Type error Vendor must be a str")

    Vendor = property(get_Vendor, set_Vendor)

    def get_Model(self) -> int:
        return self._model

    def set_Model(self, value):
        if isinstance(value, int):
            self._model = value
        else:
            self._model = 0
            raise (ValueError, " Type error Model must be a int")

    Model = property(get_Model, set_Model)

    def get_SerialNo(self) -> int:
        return self._serial

    def set_SerialNo(self, value):
        if isinstance(value, int):
            self._serial = value
        else:
            self._serial = 0
            raise (ValueError, " Type error SerialNo must be a int")

    SerialNo = property(get_SerialNo, set_SerialNo)

    def get_Dim2Bow(self) -> int:
        return self._d2bow

    def set_Dim2Bow(self, value):
        if isinstance(value, int):
            self._d2bow = value
        else:
            self._d2bow = 0
            raise (ValueError, " Type error Dim2Bow must be a int")

    Dim2Bow = property(get_Dim2Bow, set_Dim2Bow)

    def get_Dim2Stern(self) -> int:
        return self._d2stern

    def set_Dim2Stern(self, value):
        if isinstance(value, int):
            self._d2stern = value
        else:
            self._d2stern = 0
            raise (ValueError, " Type error Dim2Stern must be a int")

    Dim2Stern = property(get_Dim2Stern, set_Dim2Stern)

    def get_Dim2Port(self) -> int:
        return self._d2port

    def set_Dim2Port(self, value):
        if isinstance(value, int):
            self._d2port = value
        else:
            self._d2port = 0
            raise (ValueError, " Type error Dim2Port must be a int")

    Dim2Port = property(get_Dim2Port, set_Dim2Port)

    def get_Dim2Starboard(self) -> int:
        return self._d2starboard

    def set_Dim2Starboard(self, value):
        if isinstance(value, int):
            self._d2starboard = value
        else:
            self._d2starboard = 0
            raise (ValueError, " Type error Dim2Starboard must be a int")

    Dim2Starboard = property(get_Dim2Starboard, set_Dim2Starboard)

    def get_MotherMMSI(self) -> int:
        return self._mother

    def set_MotherMMSI(self, value):
        if isinstance(value, int):
            self._mother = value
        else:
            self._mother = 0
            raise (ValueError, " Type error MotherMMSI must be a int")

    MotherMMSI = property(get_MotherMMSI, set_MotherMMSI)

    def set_Timestamp(self, value):
        self._timestamp = value

    def get_Timestamp(self):
        return self._timestamp

    TimeStamp = property(get_Timestamp, set_Timestamp)
