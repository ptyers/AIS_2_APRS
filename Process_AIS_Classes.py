# collection of routines to process the various AIS Classes
#


import Static24
import GlobalDefinitions
from GlobalDefinitions import Global
from Mapper import MAPPER
import CNB
import SendAPRS
import BaseStation
from datetime import datetime


class AISClass:
    diagnostic = Global.diagnostic
    diagnostic2 = Global.diagnostic2
    diagnostic3 = Global.diagnostic3

    def __init__(self):
        # there are somethings common to every ais item
        # Messagetpe, RepeatrIndicator,MMSI

        pass

    def donothing(Type: int, AISObject):
        pass

    def Process1239_18(Type: int, AISObject):
        """
        AIS Object is an AISData object containing both
         the payload and a binary version of the payload
        """
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        diagnostic2 = False
        diagnostic3 = False
        diagnostic = False

        MyMap = GlobalDefinitions.Global.MyMap
        mydata = Global.mydata

        # TEMPORARY for development
        tcpstream = ""

        if diagnostic3:
            print("into process1239_18")

        try:
            if diagnostic3:
                print(" processing type %d class A", Type, AISObject)

            CNB.do_CNB(AISObject)

            if diagnostic2:
                # print('In Process Classes')
                if Type == 9:
                    #  print(" processing type 9
                    print(
                        "Type {:d} MMSI {:d} Channel {} Latitude {:06.2f} Longitude {:06.2f} SOG {:03.0f} COG {:03.0f} Altitude {:03.0f}".format(
                            Type,
                            AISObject.MMSI,
                            AISObject.AIS_Channel,
                            AISObject.Latitude,
                            AISObject.Longitude,
                            AISObject.SOG,
                            AISObject.COG,
                            AISObject.Altitude,
                        )
                    )
                elif Type == 18:
                    print(
                        "Type {:d} MMSI {:d} Channel {} Latitude {:06.2f} Longitude {:06.2f} SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                            Type,
                            AISObject.MMSI,
                            AISObject.AIS_Channel,
                            AISObject.Latitude,
                            AISObject.Longitude,
                            AISObject.SOG,
                            AISObject.COG,
                            AISObject.HDG,
                        )
                    )
                else:
                    print(
                        "Type {:d} MMSI {:d} Channel {} Latitude {:06.2f} Longitude {:06.2f} SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                            Type,
                            AISObject.MMSI,
                            AISObject.AIS_Channel,
                            AISObject.Latitude,
                            AISObject.Longitude,
                            AISObject.SOG,
                            AISObject.COG,
                            AISObject.HDG,
                        )
                    )
            try:
                #  print("Wrote Input Line")
                if AISObject.String_MMSI in MyMap:
                    # print("tested for MyMapKey matching MMSI")
                    if diagnostic:
                        print(
                            (
                                "Substituting MMSI",
                                AISObject.String_MMSI,
                                MyMap[AISObject.String_MMSI].Callsign,
                                MyMap[AISObject.String_MMSI].Name,
                                MyMap[AISObject.String_MMSI].Destination,
                            )
                        )
                    # if moving from MMSI as Callsign to Name need to kill off MMSI object in APRS
                    if not MyMap[AISObject.String_MMSI].KillSent:
                        try:
                            SendAPRS.SendAPRS(
                                AISObject.AIS_Payload_ID, AISObject, True, 0
                            )
                            MyMap[AISObject.String_MMSI].KillSent = True
                        except Exception as e:
                            raise RuntimeError(
                                "Error Sending kill APRS in 12349 - Error in SendAPRS",
                                e,
                                "\r\n",
                            ) from e

                    AISObject.Callsign = MyMap[AISObject.String_MMSI].Callsign
                    AISObject.Name = MyMap[AISObject.String_MMSI].Name
                    if diagnostic:
                        print(
                            "1239_18 Callsign = ",
                            AISObject.Callsign,
                            " 1239_18Name = ",
                            AISObject.Name,
                        )
            except Exception as e:
                raise RuntimeError(
                    " Error checking MyMap in 12349 ='\
                                   ' Error in Checking matching MMSI",
                    e,
                    "\r\n",
                ) from e

            try:
                SendAPRS.SendAPRS(AISObject.AIS_Payload_ID, AISObject, False, 0)
            except Exception as e:
                raise RuntimeError(
                    "Error Sending APRS in 12349 - Error in SendAPRS", e, "\r\n"
                ) from e

        except Exception as e:
            raise RuntimeError(
                "Exception while processing Type 1, 2 , 3 or 9", e, "\r\n"
            ) from e

    def Process4(self, AISObject):
        try:
            diagnostic = Global.diagnostic
            diagnostic2 = Global.diagnostic2
            diagnostic3 = Global.diagnostic3
            MyMap = Global.MyMap

            my_base = BaseStation.BASESTATION(AISObject)
            if diagnostic3:
                print(" processing type 4")
            if diagnostic2:
                print(
                    " Base Station {:s} {:s}  {:f} {:f}".format(
                        AISObject.String_MMSI,
                        AISObject.AIS_Channel,
                        AISObject.Latitude,
                        AISObject.Longitude,
                    )
                )

            SendAPRS.SendAPRS(AISObject.AIS_Payload_ID, AISObject, False, 0)

        except Exception as e:
            raise RuntimeError("Exception while processing Type4", e, "\r\n") from e

    def Process5(self, AISObject):

        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        diagnostic2 = False

        if diagnostic:
            print("ínto Process 5")

        try:
            # print('AISObject,MMSI = ', AISObject.MMSI)
            # print('AISOJECT Binary', AISObject.AIS_Binary_Payload)
            my_base = Static24.STATIC24(AISObject)
            MyMap = Global.MyMap
            # print('AISObject,MMSI = ', AISObject.MMSI)

            if diagnostic3:
                print(
                    "{:s} {:s} Class A Vessel Named {:s} Callsign {:s} Destination {:s} ShipType {:d}".format(
                        AISObject.String_MMSI,
                        AISObject.AIS_Channel,
                        AISObject.Name,
                        AISObject.Callsign,
                        AISObject.Destination,
                        AISObject.ShipType,
                    )
                )

            #  check if we have a record in the mapping directory for this MMSI

            if AISObject.String_MMSI in MyMap:
                # print("tested for MyMapKey matching MMSI")
                if diagnostic:
                    print(
                        "Substituting Type 5 MMSI {:s} Callsign {:s} Name {:s} {Destination {:s}".format(
                            AISObject.String_MMSI,
                            MyMap[AISObject.String_MMSI].Callsign,
                            MyMap[AISObject.String_MMSI].Name,
                            MyMap[AISObject.String_MMSI].Destination,
                        )
                    )
                    AISObject.Callsign = MyMap[AISObject.String_MMSI].Callsign
                    AISObject.Name = MyMap[AISObject.String_MMSI].Name

            if AISObject.String_MMSI in MyMap:
                #  key/value pair exists
                #  update its timestamp
                MyMap[AISObject.String_MMSI].TimeStamp = datetime.now()

            else:

                #  no key/value pair exists
                #  send a kill stream for the MMSI referenced version
                #  then create a key/value pair
                #  for the purpose of the exercise the position of the object is set to the South Pole when killing
                #  coordinates 90S, 0E

                AISObject.int_latitude = 90 * 600000
                AISObject.int_longitude = 0
                SendAPRS.SendAPRS(AISObject.AIS_Payload_ID, AISObject, True, 0)
                mapitem = MAPPER(
                    AISObject.Callsign, AISObject.Name, AISObject.Destination
                )

                MyMap[AISObject.String_MMSI] = mapitem
                # print("after Add" + xx.Key + " " + xx.Value.Callsign + " " + xx.Value.Callsign)
                # print("Loading MyMap {0:G} {1:G} {2:G} {3:G}", AISObject.String_MMSI, MyMap[AISObject.String_MMSI].Callsign,
                #     MyMap[AISObject.String_MMSI].Name, MyMap[AISObject.String_MMSI].Destination)
                if diagnostic2:
                    print(
                        "mapitem = "
                        + AISObject.String_MMSI
                        + " "
                        + mapitem.Callsign
                        + " "
                        + mapitem.Name
                    )

                    for key in MyMap:
                        item = MyMap[key]
                        print(key, item.Callsign, item.Name, item.Destination)

                    #  on the next position report the new stream will have identity by callsign
                    #  this mapping is done in the createObject method of class APRS
            # flush outdated entries from map MMSI to ShipName

            flushMyMap()

        except Exception as e:
            raise RuntimeError("Exception while processing Type5", e, "\r\n") from e

    # region Process14
    def Process14(self, AISObject):
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        Bulletin = GlobalDefinitions.Global.Bulletin
        MyMap = GlobalDefinitions.Global.MyMap

        diagnostic = False

        #  bulletin rolls over mod 10
        Bulletin += 1
        Bulletin = Bulletin % 10
        try:

            if diagnostic:
                print("Bulletin {:d} {:s}".format(Bulletin, AISObject.Safetytext))

            SendAPRS.SendAPRS(AISObject.AIS_Payload_ID, AISObject, False, Bulletin)
        except Exception as e:
            raise RuntimeError("Exception while processing Type14", e, "\r\n") from e

    def Process24(self, AISObject):
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        MyMap = GlobalDefinitions.Global.MyMap
        Type24s = GlobalDefinitions.Global.Type24s
        diagnostic = False
        diagnostic2 = False
        diagnostic3 = False

        if diagnostic:
            print("into process 24 MMSI = ", str(AISObject.ExtractInt(8, 30)))

        try:
            PartType = AISObject.Type24PartNo
            MMSI = str(AISObject.ExtractInt(8, 30))

            if diagnostic3:
                print("Looking for MMSI in Type24s", MMSI)
            if MMSI in Type24s:
                try:
                    if diagnostic:
                        print(
                            "Found MMSI in 24s",
                            MMSI,
                            Type24s[MMSI].Name,
                            Type24s[MMSI].Callsign,
                        )
                    #  There is an existing type24 record in the dictionary for this MMSI
                    new24 = Type24s[MMSI]
                    # now update the record with new data
                    new24.update(AISObject)
                    Type24s[MMSI] = new24
                    if diagnostic:
                        print(
                            " After type24s update For MMSI ",
                            MMSI,
                            Type24s[MMSI].Name,
                            Type24s[MMSI].Callsign,
                        )

                    if diagnostic3:
                        print("ValidA = ", new24.Valid_A, "  ValidB = ", new24.Valid_B)

                    if new24.Valid_A and new24.Valid_B:
                        # have a valid composite Type24 record
                        # update the Mapper Directory
                        if MMSI in MyMap:
                            # update the map otherwise create a new map object
                            update24(MMSI, MyMap, new24)
                        else:  # create new Mapper Entry
                            newMap = MAPPER(
                                new24.Callsign, new24.Name, ""
                            )  # for Type 24 Destination is null
                            if diagnostic3:
                                print("In Process24 MyMap before addition =")
                                for data in MyMap:
                                    print(data, MyMap[data].Callsign, MyMap[data].Name)
                            MyMap[MMSI] = newMap
                            if diagnostic3:
                                print("In Process24 MyMap after addition =")
                                for MMSI in MyMap:
                                    print(MMSI, MyMap[MMSI].Callsign, MyMap[MMSI].Name)
                            update24(MMSI, MyMap, new24)

                    # finally flush old entries from the map
                    flushMyMap()
                except Exception as e:
                    raise RuntimeError(
                        "Exception while processing existing Type 24\r\n"
                        + "ShipType {:d} Vendor {:s} Model {:d} Callsign {:s} \r\n"
                        + "DimBow {:d} DimStern {:d} DimPort {:d} DimStartboard {:d}"
                        + "\r\n MotherMMSI {:d} "
                        + "Valid {:s}\n\r {:s}\r\n".format(
                            new24.ShipType,
                            new24.Vendor,
                            new24.Model,
                            new24.Callsign,
                            new24.Dim2Bow,
                            new24.Dim2Stern,
                            new24.Dim2Port,
                            new24.Dim2Starboard,
                            new24.MotherMMSI,
                            new24.Valid_B,
                            e,
                        )
                    ) from e

            else:  # this is a new Type24 MMSI
                # instantiate a Type24 object and put it into the Type24s Dictionary
                try:
                    new24 = Static24.STATIC24(AISObject)
                    Type24s[MMSI] = new24

                except Exception as e:
                    raise RuntimeError(
                        "Exception while processing new Type 24\r\n"
                        + "ShipType {:d} Vendor {:s} Model {:d} Callsign {:s} \r\n"
                        + "DimBow {:d} DimStern {:d} DimPort {:d} DimStartboard {:d}\r\n MotherMMSI {:d} "
                        + "Valid {:s}\n\r {:s}\r\n".format(
                            new24.ShipType,
                            new24.Vendor,
                            new24.Model,
                            new24.Callsign,
                            new24.Dim2Bow,
                            new24.Dim2Stern,
                            new24.Dim2Port,
                            new24.Dim2Starboard,
                            new24.MotherMMSI,
                            new24.Valid_B,
                            e,
                        )
                    ) from e
        except Exception as e:
            raise RuntimeError("Exception while processing Type 24", e, "\r\n") from e


def update24(MMSI, MyMap, new24):
    # takes data from new24 and updates the Mapper entry

    MyMap[MMSI].Callsign = new24.Callsign
    tname = new24.Name
    while len(tname) > 1 and tname[len(tname) - 1] == " ":  # suppress trailing spaces
        if len(tname) > 1:
            tname = tname[0: (len(tname) - 1)]
        else:
            break
    new24.Name = tname
    MyMap[MMSI].Name = new24.Name
    MyMap[MMSI].ShipType = new24.ShipType
    MyMap[MMSI].Vendor = new24.Vendor
    MyMap[MMSI].Model = new24.Model
    MyMap[MMSI].SerialNo = new24.SerialNo
    MyMap[MMSI].Dim2Bow = new24.Dim2Bow
    MyMap[MMSI].Dim2Stern = new24.Dim2Stern
    MyMap[MMSI].Dim2Port = new24.Dim2Port
    MyMap[MMSI].Dim2Starboard = new24.Dim2Starboard
    MyMap[MMSI].MotherMMSI = new24.MotherMMSI
    MyMap[MMSI].TimeStamp = datetime.now()


def flushMyMap():
    # flushes outdated enties from the map MMSI to ShipName
    # according to paramet MappingTTL in GlobalDefinitions

    currtime = datetime.now()
    # create empty list of MMSIs to be deleted from Map
    deletelist = []

    for key in Global.MyMap:
        if (currtime - Global.MyMap[key].TimeStamp).total_seconds() > Global.MappingTTL:
            deletelist.append(key)
    # now have a list of keys to delete

    for xx in deletelist:
        del Global.MyMap[xx]


def main(self):
    pass


if __name__ == 'main':
    main()
