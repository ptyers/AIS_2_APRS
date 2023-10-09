import datetime
import AISData
import MyPreConfigs
import GlobalDefinitions


class STATIC24:
    #  because type 24 is made up of information from parts "A" and "B"
    #  cannot just throw data into the AIS_Data variable since to get complete information
    #  need to receive at least two information packets

    #  these variables are stored in a dictionary class using (string) MMSI as the key
    #  a boolean flag is used to indicate whether the information is complete
    #  a timestamp is used to allow garbage collection for items which have not been completed within a defined time
    #
    p_mmsi = 0
    p_name = ""
    p_type = 0  # not available
    p_vendor = ""  # 3 chars
    p_model = 0
    p_serial = 0
    p_call = ""
    p_d2bow = 0
    p_d2stern = 0
    p_d2port = 0
    p_d2starboard = 0
    p_mother = (
        0  # this field is open to interpretation - definition is confused 30 bits
    )
    p_complete = (
        False  # used to indicate if all information has been collected and record valid
    )
    p_timestamp = (
        datetime.datetime.now()
    )  # used to allow "garbage collection" for items not validated within given period
    hasbeenDisposed = False
    p_timeout = float(
        180
    )  # defaults to 180 second timeout - adjustable using public (writeonly) Timeout variable
    p_valid_a = False
    p_valid_b = False

    #  dont need to store MMSI with the Type24 data since this is held as key in the dictionary
    #  ditto PartNumber - indicating either Part A or B value of this must be either 0 or 1 representing Part A or Part B

    """

            def get_xxxx(self) -> zz:
                return self.yyyy
            def set_xxxx(self,value):
                if isinstance(value, zz):
                    self.yyyy = value
                else:
                    self.yyyy = ''
                    raise(ValueError, " Type error xxxx must be a zz")
            xxxx = property(get_xxxx, set_xxxx)


    """

    def __init__(self, AISObject):
        # initialise a collection of parameters presumably held in the AISObject
        # first
        # print('Instantiating Type 24')
        # AISObject.print_AIS()
        if AISObject.AIS_Payload_ID == 5:
            if GlobalDefinitions.Global.diagnostic3:
                print(
                    "ín 5 AISObject Binary",
                    len(AISObject.AIS_Binary_Payload),
                    " ",
                    AISObject.AIS_Binary_Payload,
                )
            # first stuff related to a Type 5 (Static and Voyage RElated)
            AISObject.Version = AISObject.ExtractInt(38, 2)
            AISObject.IMO = AISObject.ExtractInt(40, 30)
            AISObject.Callsign = self.get_string(AISObject.AIS_Binary_Payload, 70, 42)
            AISObject.Name = self.get_string(AISObject.AIS_Binary_Payload, 112, 120)
            AISObject.ShipType = AISObject.ExtractInt(232, 8)
            AISObject.Dim2Bow = AISObject.ExtractInt(240, 9)
            AISObject.Dim2Stern = AISObject.ExtractInt(249, 9)
            AISObject.Dim2Port = AISObject.ExtractInt(258, 6)
            AISObject.Dim2StarBoard = AISObject.ExtractInt(264, 6)
            AISObject.PositionFix = AISObject.ExtractInt(270, 4)
            AISObject.ETAMonth = AISObject.ExtractInt(274, 4)
            AISObject.ETADay = AISObject.ExtractInt(278, 5)
            AISObject.ETAHour = AISObject.ExtractInt(283, 5)
            AISObject.ETAMinute = AISObject.ExtractInt(288, 6)
            AISObject.Draught = AISObject.ExtractInt(294, 8)
            AISObject.Destination = self.get_string(
                AISObject.AIS_Binary_Payload, 302, 120
            )
            AISObject.DTE = AISObject.ExtractInt(422, 1)

        if AISObject.AIS_Payload_ID == 24:
            # now we update the objrct just created -
            # whether part A or part B will be chcked in update()
            self.update(AISObject)

    def update(self, AISObject):
        # update the Static24 object with data from the AIS stream
        # Type 24 can come as either TypeA or TypeB (0 or 1 in bits38-39)
        if AISObject.ExtractInt(38, 2) == 0:  # Type A

            self.p_name = self.get_string(AISObject.AIS_Binary_Payload, 40, 120)
            self.p_valid_a = True  # indicates we have had valid part A data

        else:  # Type B

            self.p_type = AISObject.ExtractInt(40, 8)
            self.p_vendor = self.get_string(AISObject.AIS_Binary_Payload, 48, 18)
            self.p_model = AISObject.ExtractInt(66, 4)
            self.p_serial = AISObject.ExtractInt(70, 20)
            self.p_call = self.get_string(AISObject.AIS_Binary_Payload, 90, 42)
            self.p_d2bow = AISObject.ExtractInt(132, 9)
            self.p_d2stern = AISObject.ExtractInt(141, 9)
            self.p_d2port = AISObject.ExtractInt(150, 6)
            self.p_d2starboard = AISObject.ExtractInt(156, 6)
            self.p_mother = AISObject.ExtractInt(132, 30)
            self.p_valid_b = True  # indicates we have had valid part A data

    def get_string(self, Binarystring, sstart, length) -> str:
        diagnostic = GlobalDefinitions.Global.diagnostic
        diagnostic2 = GlobalDefinitions.Global.diagnostic2
        diagnostic3 = GlobalDefinitions.Global.diagnostic3

        if diagnostic3:
            print("in get string start = ", sstart, " length = ", length)
        ba = bytearray()
        st = Binarystring[sstart + 1 : sstart + length + 1]
        if diagnostic3:
            print("length st =", len(st))
        while len(st) < length:
            st = st + "0"
        for i in range(0, int(length / 6)):
            if diagnostic3:
                print(st[i * 6 : (i * 6) + 6])
            temp = int(st[i * 6 : (i * 6) + 5], 2)
            # print("temp = " + temp);
            temp = temp & 0x3F
            if temp < 31:
                temp = temp + 0x40
            ba.append(temp)
            i += 1

        thisstring = ba.decode("utf-8")
        if diagnostic3:
            print(thisstring)

        # SUPRESS @
        no_at = ""
        strlength = len(thisstring) - 1
        for i in range(0, strlength):
            if thisstring[i] == "@":
                no_at = no_at + " "
            else:
                no_at = no_at + thisstring[i]

        # Suppress trailing Spaces
        for i in range(len(no_at) - 1, 1):
            if no_at[i] == " ":
                no_at = no_at[0 : i - 1]
            else:
                break

        # safety check
        if len(no_at) == 0:
            no_at = " "

        return no_at

    def get_int(self, Binarystring, sstart, length) -> int:
        diagnostic = GlobalDefinitions.Global.diagnostic
        diagnostic2 = GlobalDefinitions.Global.diagnostic2
        diagnostic3 = GlobalDefinitions.Global.diagnostic3

        if diagnostic3:
            print("in get int static24 start = ", sstart, " length = ", length)

        st = Binarystring[sstart + 1 : sstart + length + 1]
        if diagnostic3:
            print("in static24 length st =", len(st))
        while len(st) < length:
            st = st + "0"

        # convert binary string to integer base 2

        try:
            my_int = int(st, 2)
        except:
            my_int = 0

        return my_int

    def get_Name(self) -> str:
        return self.p_name

    def set_Name(self, value):
        if isinstance(value, str):
            self.p_name = value
            self.p_name = Remove_at(self.p_name)
            self.p_name = Remove_space(self.p_name)
        else:
            self.p_name = ""
            raise (ValueError, " Type error Name must be a str")

    Name = property(get_Name, set_Name)

    def get_ShipType(self) -> int:
        return self.p_type

    def set_ShipType(self, value):
        if isinstance(value, int):
            self.p_type = value
        else:
            self.p_type = 0
            raise (ValueError, " Type error ShipType must be a int")

    ShipType = property(get_ShipType, set_ShipType)

    def get_Vendor(self) -> str:
        return self.p_vendor

    def set_Vendor(self, value):
        if isinstance(value, str):
            self.p_vendor = value
        else:
            self.p_vendor = ""
            raise (ValueError, " Type error Vendor must be a str")

    Vendor = property(get_Vendor, set_Vendor)

    def get_Model(self) -> int:
        return self.p_model

    def set_Model(self, value):
        if isinstance(value, int):
            self.p_model = value
        else:
            self.p_model = 0
            raise (ValueError, " Type error Model must be a int")

    Model = property(get_Model, set_Model)

    def get_SerialNo(self) -> int:
        return self.p_serial

    def set_SerialNo(self, value):
        if isinstance(value, int):
            self.p_serial = value
        else:
            self.p_serial = 0
            raise (ValueError, " Type error SerialNo must be a int")

    SerialNo = property(get_SerialNo, set_SerialNo)

    def get_Callsign(self) -> str:
        return self.p_call

    def set_Callsign(self, value):
        if isinstance(value, str):
            p_call = value
            p_call = Remove_at(p_call)
            p_call = Remove_space(p_call)
        else:
            self.p_call = ""
            raise (ValueError, " Type error Callsign must be a str")

    Callsign = property(get_Callsign, set_Callsign)

    def get_Dim2Bow(self) -> int:
        return self.p_d2bow

    def set_Dim2Bow(self, value):
        if isinstance(value, int):
            self.p_d2bow = value
        else:
            self.p_d2bow = 0
            raise (ValueError, " Type error Dim2Bow must be a int")

    Dim2Bow = property(get_Dim2Bow, set_Dim2Bow)

    def get_Dim2Stern(self) -> int:
        return self.p_d2stern

    def set_Dim2Stern(self, value):
        if isinstance(value, int):
            self.p_d2stern = value
        else:
            self.p_d2stern = 0
            raise (ValueError, " Type error Dim2Stern must be a int")

    Dim2Stern = property(get_Dim2Stern, set_Dim2Stern)

    def get_Dim2Port(self) -> int:
        return self.p_d2port

    def set_Dim2Port(self, value):
        if isinstance(value, int):
            self.p_d2port = value
        else:
            self.p_d2port = 0
            raise (ValueError, " Type error Dim2Port must be a int")

    Dim2Port = property(get_Dim2Port, set_Dim2Port)

    def get_Dim2Starboard(self) -> int:
        return self.p_d2starboard

    def set_Dim2Starboard(self, value):
        if isinstance(value, int):
            self.p_d2starboard = value
        else:
            self.p_d2starboard = 0
            raise (ValueError, " Type error Dim2Starboard must be a int")

    Dim2Starboard = property(get_Dim2Starboard, set_Dim2Starboard)

    def get_MotherMMSI(self) -> int:
        return self.p_mother

    def set_MotherMMSI(self, value):
        if isinstance(value, int):
            self.p_mother = value
        else:
            self.p_mother = 0
            raise (ValueError, " Type error MotherMMSI must be a int")

    MotherMMSI = property(get_MotherMMSI, set_MotherMMSI)

    def get_Valid(self) -> bool:
        return self.p_complete

    def set_Valid(self, value):
        if isinstance(value, bool):
            self.p_complete = value
        else:
            self.p_complete = False
            raise (ValueError, " Type error Valid must be a bool")

    Valid = property(get_Valid, set_Valid)

    def get_Timeout(self) -> float:
        return self.p_timeout

    def set_Timeout(self, value):
        if isinstance(value, float):
            self.p_timeout = value
        else:
            self.p_timeout = float(0)
            raise (ValueError, " Type error Timeout must be a float")

    Timeout = property(get_Timeout, set_Timeout)

    def get_Outdated(self) -> bool:
        now = datetime.datetime.now()
        tester = self.p_timestamp
        tester = tester.AddSeconds(self.p_timeout)
        if tester.CompareTo(now) < 0:  # if True the timeout period has expired
            return True
        else:
            return False

    Outdated = property(get_Outdated)

    def get_ValidA(self) -> bool:
        return self.p_valid_a

    def set_ValidA(self, value):
        if isinstance(value, bool):
            self.p_valid_a = value
        else:
            self.p_valid_a = False
            raise (ValueError, " Type error ValidA must be a bool")

    Valid_A = property(get_ValidA, set_ValidA)

    def get_ValidB(self) -> bool:
        return self.p_valid_b

    def set_ValidB(self, value):
        if isinstance(value, bool):
            self.p_valid_b = value
        else:
            self.p_valid_b = False
            raise (ValueError, " Type error ValidB must be a bool")

    Valid_B = property(get_ValidB, set_ValidB)


def Remove_at(p: str) -> str:
    try:
        if p.index("@") > 0:
            p = p[0 : p.index("@")]
            return p
        else:
            if p.index("@") == 0:
                return ""
            else:
                return p
    except ValueError:
        return p
    except Exception as e:
        print("Error T24 Remove_at string = " + p + " length = " + str(len(p)) + "\r\n")
        raise RuntimeError("Error in Type 24 Remove_at", e) from e


def Remove_space(p: str) -> str:
    try:
        if p == "":
            return ""
        else:
            if p[len(p) - 1 : 1] == " ":
                while p[len(p) - 1 : 1] == " ":

                    if len(p) > 1:
                        p = p[0 : len(p) - 1]
                    else:
                        return ""
            return p
    except ValueError:
        return ""
    except:
        print(
            "Error T24 Remove_Space string = " + p + " length = " + str(len(p)) + "\r\n"
        )
        raise RuntimeError("Error in TYpe 24 Remove_Space")
