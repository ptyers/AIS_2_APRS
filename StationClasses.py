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
    coarse_over_ground: float
    true_heading: int
    time_stamp: int
    Maneuver_indicator: int
    raim_flag: bool
    radio_status: int
    callsign: str
    AIS_version: int

    def __init__(self, in_mmsi: str):
        self.mmsi = in_mmsi
        self.lat = 0.0
        self.long = 0.0
        self.position_accuracy: bool = 0  # False
        self.speed_over_ground: float = 0.0
        self.rate_of_turn: int = 0
        self.navigation_status: int = 15
        self.coarse_over_ground: float = 0.0
        self.true_heading: int = 0
        self.time_stamp: int = 0
        self.Maneuver_indicator: int = 0
        self.raim_flag: bool = 0  # False
        self.radio_status: int = 0
        self.callsign: str = ''
        self.AIS_version: int = 0


class Vessel(GenericStation):
    speed_over_ground: float
    Vessel_name: str
    Ship_type: int
    Dim_bow: int
    Dim_stern: int
    Dim_port: int
    Dim_starboard: int
    Position_fix: int
    IMO_number: int
    vendor_id: str
    unit_MODEL_CODE: int
    serial_number: int
    mother_ship_mmsi: str

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)
        self.speed_over_ground: float = 0.0
        self.Vessel_name: str = ''
        self.Ship_type: int = 0
        self.Dim_bow: int = 0
        self.Dim_stern: int = 0
        self.Dim_port: int = 0
        self.Dim_starboard: int = 0
        self.Position_fix: int = 0
        self.IMO_number: int = 0


class ClassA_Vessel(Vessel):
    rate_of_turn: int
    navigation_status: int
    ETA_month: int
    ETA_day: int
    ETA_hour: int
    ETA_min: int
    Draught: float
    Destination: str
    DTE: bool
    type_epfd: int

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)
        self.ETA_month: int = 0
        self.ETA_day: int = 0
        self.ETA_hour: int = 0
        self.ETA_min: int = 0
        self.Draught: float = 0.0
        self.Destination: str = ''
        self.DTE: int = 1
        self.type_epfd: int = 0


class ClassB_Vessel(Vessel):
    CS_unit: bool
    display_flag: bool
    DSC_flag: bool
    band_flag: bool
    message22_fladg: bool
    assigned_flag: bool

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)
        self.CS_unit: bool = 0
        self.display_flag: bool = 0
        self.DSC_flag: bool = 0
        self.band_flag: bool = 0
        self.message22_fladg: bool = 0
        self.assigned_flag: bool = 0


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
        super().__init__(in_mmsi)
        self.utc_year: int = 0
        self.utc_month: int = 0
        self.utc_day: int = 0
        self.utc_hour: int = 0
        self.utc_second: int = 0
        self.fix_quality: bool = 0  # False
        self.type_of_epfd: int = 0
        self.sotdma_state: int = self.radio_status


class SAR(GenericStation):
    altitude: int
    DTE: int
    assigned: bool

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)
        self.altitude: int = 0
        self.DTE: int = 1
        self.assigned: bool = 0


class Aid_To_Nav(GenericStation):
    aid_type: int
    name: str
    Dim_bow: int
    Dim_stern: int
    Dim_port: int
    Dim_starboard: int
    type_epfd: int
    UTC_second: int
    off_position_indicator: bool
    virtual_aid_flag: bool
    assigned: bool
    name_extension: str

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)
        self.Dim_bow: int = 0
        self.Dim_stern: int = 0
        self.Dim_port: int = 0
        self.Dim_starboard: int = 0
        self.type_epfd: int
        self.UTC_second: int
        self.off_position_indicator: bool
        self.virtual_aid_flag: bool
        self.assigned: bool
        self.name_extension: str


class Aux_Craft(GenericStation):

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)


class AIS_SART(GenericStation):

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)


class MOB_Device(GenericStation):

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)


class EPIRB(GenericStation):

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)


class Diver(GenericStation):

    def __init__(self, in_mmsi: str):
        super().__init__(in_mmsi)


def main(self):
    pass


if __name__ == 'main':
    main()
