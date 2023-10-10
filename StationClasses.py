'''
Currently unused
Class objects for the various Station Types
All derive from base class GenericStation




'''


class GenericStation:
    mmsi: str
    lat: float
    long: float
    position_accuracy: bool
    speed_over_ground: float
    rate_of_turn: int
    navigation_status: int
    coarse_over_ground: float
    true_heading: int
    time_stamp: int
    Maneuver_indicator: int
    raim_flag: bool
    radio_status: int
    callsign: str

    def __init__(self, in_mmsi: str):
        self.mmsi = in_mmsi
        self.lat = 0.0
        self.long = 0.0
        self.position_accuracy: bool = 0 #False
        self.speed_over_ground: float = 0.0
        self.rate_of_turn: int = 0
        self.navigation_status: int = 15
        self.coarse_over_ground: float = 0.0
        self.true_heading: int = 0
        self.time_stamp: int = 0
        self.Maneuver_indicator: int = 0
        self.raim_flag: bool = 0 #False
        self.radio_status: int = 0
        self.callsign: str = ''


class Vessel(GenericStation):




    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class BaseStation(GenericStation):
    utc_year: int
    utc_month: int
    utc_day: int
    utc_hour: int
    utc_second: int
    fix_quality: bool
    type_of_epfd: int
    sotdma_state: int

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)
        self.utc_year: int = 0
        self.utc_month: int = 0
        self.utc_day: int = 0
        self.utc_hour: int = 0
        self.utc_second: int = 0
        self.fix_quality: bool = 0  # False
        self.type_of_epfd: int = 0
        self.sotdma_state: int = self.radio_status

class SAR(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class Aid_To_Nav(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class Aux_Craft(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class AIS_SART(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class MOB_Device(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)

class EPIRB(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


class Diver(GenericStation):

    def __init__(self, in_mmsi: str):
        super.__init__(in_mmsi)


