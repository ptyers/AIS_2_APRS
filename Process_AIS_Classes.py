# collection of routines to process the various AIS Classes
#



import GlobalDefinitions
from GlobalDefinitions import Global
from Mapper import MAPPER
import Payloads
import SendAPRS
from datetime import datetime
import logging
from Payloads import AISStream, AISDictionaries, Fragments
from Payloads import Basic_Position, Basestation, CNB, Static_data_report, ClassB_position_report
from Payloads import StaticData, SAR_aircraft_position_report
from Payloads import Safety_related_broadcast_message, Addressed_safety_related_message, \
    Long_range_AIS_broadcast_message


class AISClass:

    def __init__(self):
        # there are somethings common to every ais item
        # Messagetpe, RepeatrIndicator,MMSI

        logging.basicConfig(level=logging.DEBUG)

        pass

    def donothing(payload_type: int, aisobject):
        pass

    def Process1239_18(payload_type: int, aisobject):
        """
        AIS Object is an AISData object containing both
         the payload and a binary version of the payload
        """

        MyMap = GlobalDefinitions.Global.MyMap
        #mydata = Global.mydata

        # TEMPORARY for development
        tcpstream = ""

        logging.info("into process1239_18")

        try:

            logging.debug("processing type {:d} \n Payload {}".format(payload_type, aisobject))


            if payload_type == 9:
                print(" processing payload_type 9")
                packet = SAR_aircraft_position_report(aisobject)
                logging.debug(
                    "payload_type {:d} MMSI {:d}  Latitude {:06.2f} Longitude {:06.2f} "
                    " Altitude {} SOG {:03.0f} COG {:03.0f} ".format(
                        payload_type,
                        packet.int_mmsi,
                        packet.latitude,
                        packet.longitude,
                        packet.speed_over_ground,
                        packet.course_over_ground,
                        packet.altitude
                    )
                )
            elif payload_type == 18:
                print(" processing payload_type 18")
                packet = ClassB_position_report(aisobject)
                logging.debug(
                    "payload_type {:d} MMSI {:d}  Latitude {:06.2f} Longitude {:06.2f} "
                    "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                        payload_type,
                        packet.int_mmsi,
                        packet.latitude,
                        packet.longitude,
                        packet.speed_over_ground,
                        packet.course_over_ground,
                        packet.true_heading,
                    )
                )
            else:
                print("Processing type 123")
                packet = CNB(aisobject)
                logging.debug(
                    "payload_type {:d} MMSI {:d}  Latitude {:06.2f} Longitude {:06.2f} "
                    "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                        payload_type,
                        packet.int_mmsi,
                        packet.latitude,
                        packet.longitude,
                        packet.speed_over_ground,
                        packet.course_over_ground,
                        packet.true_heading
                    )
                )
            try:
                if packet.mmsi in MyMap:
                    print("tested for MyMapKey matching MMSI")

                    logging.debug(
                        (
                            "Substituting MMSI",
                            packet.int_mmsi,
                            MyMap[packet.int_mmsi].Callsign,
                            MyMap[packet.int_mmsi].Name,
                            MyMap[packet.int_mmsi].Destination,
                        )
                    )
                    # if moving from MMSI as Callsign to Name need to kill off MMSI object in APRS
                    if not MyMap[packet.int_mmsi].KillSent:
                        try:
                            SendAPRS.SendAPRS(
                                packet.int_mmsi, packet, True, 0
                            )
                            MyMap[packet.int_mmsi].KillSent = True
                        except Exception as e:
                            raise RuntimeError(
                                "Error Sending kill APRS in 12349 - Error in SendAPRS",
                                e,
                                "\r\n",
                            ) from e

                    packet.callsign = MyMap[packet.int_mmsi].Callsign
                    packet.vessel_name = MyMap[packet.int_mmsi].Name

                    logging.debug(
                        "1239_18 Callsign = ",
                        packet.callsign,
                        " 1239_18Name = ",
                        packet.vessel_name,
                    )
            except Exception as e:
                raise RuntimeError(
                    " Error checking MyMap in 12349 ='\
                                   ' Error in Checking matching MMSI",
                    e,
                    "\r\n",
                ) from e

            try:
                SendAPRS.SendAPRS(payload_type, packet, False, 0)
            except Exception as e:
                raise RuntimeError(
                    "Error Sending APRS in 12349 - Error in SendAPRS", e, "\r\n"
                ) from e

        except Exception as e:
            raise RuntimeError(
                "Exception while processing payload_type 1, 2 , 3 or 9", e, "\r\n"
            ) from e

    def Process4(self, aisobject):

        print("Processing Type 4")

        try:
            MyMap = Global.MyMap

            packet = Basestation(aisobject)
            logging.info(" processing payload_type 4")
            logging.debug(
                " Base Station {:s}   {:f} {:f}".format(
                    packet.mmsi,
                    packet.latitude,
                    packet.longitude,
                )
            )

            SendAPRS.SendAPRS(packet.message_type, packet, False, 0)

        except Exception as e:
            raise RuntimeError("Exception while processing payload_type4", e, "\r\n") from e

    def Process5(self, aisobject):

        print("Processing Type 5")

        logging.info("ínto Process 5")

        try:
            # print('packet,MMSI = ', packet.MMSI)
            # print('AISOJECT Binary', packet.AIS_Binary_Payload)
            packet = StaticData(aisobject)
            MyMap = Global.MyMap
            # print('packet,MMSI = ', packet.MMSI)

            logging.debug(
                "{:s}  Class A Vessel Named {:s} Callsign {:s} Destination {:s} Ship_type {:d}".format(
                    packet.int_mmsi,
                    packet.Name,
                    packet.Callsign,
                    packet.destination,
                    packet.ship_type
                )
            )

            #  check if we have a record in the mapping directory for this MMSI

            if packet.int_mmsi in MyMap:
                # print("tested for MyMapKey matching MMSI")
                logging.debug(
                    "Substituting Type 5 MMSI {:s} Callsign {:s} Name {:s} {Destination {:s}".format(
                        packet.int_mmsi,
                        MyMap[packet.int_mmsi].Callsign,
                        MyMap[packet.int_mmsi].Name,
                        MyMap[packet.int_mmsi].Destination,
                    )
                )
                packet.Callsign = MyMap[packet.int_mmsi].Callsign
                packet.Name = MyMap[packet.int_mmsi].Name

            if packet.int_mmsi in MyMap:
                #  key/value pair exists
                #  update its timestamp
                MyMap[packet.int_mmsi].TimeStamp = datetime.now()

            else:

                #  no key/value pair exists
                #  send a kill stream for the MMSI referenced version
                #  then create a key/value pair
                #  for the purpose of the exercise the position of the object is set to the South Pole when killing
                #  coordinates 90S, 0E

                packet.int_latitude = 90 * 600000
                packet.int_longitude = 0
                SendAPRS.SendAPRS(packet.message_type, packet, True, 0)
                mapitem = MAPPER(
                    packet.Callsign, packet.Name, packet.destination
                )

                MyMap[packet.int_mmsi] = mapitem
                # print("after Add" + xx.Key + " " + xx.Value.Callsign + " " + xx.Value.Callsign)
                # print("Loading MyMap {0:G} {1:G} {2:G} {3:G}", packet.int_mmsi, MyMap[packet.int_mmsi].Callsign,
                #     MyMap[packet.int_mmsi].Name, MyMap[packet.int_mmsi].Destination)

                logging.debug(
                    "mapitem = "
                    + packet.mmsi
                    + " "
                    + mapitem.Callsign
                    + " "
                    + mapitem.Name
                )

                for key in MyMap:
                    item = MyMap[key]
                    logging.debug("{} {} {} {}".format(key, item.Callsign, item.Name, item.Destination))

                #  on the next position report the new stream will have identity by callsign
                #  this mapping is done in the createObject method of class APRS
        # flush outdated entries from map MMSI to ShipName

            flushMyMap()

        except Exception as e:
            raise RuntimeError("Exception while processing Type5", e, "\r\n") from e

    # region Process14
    def Process14(self, aisobject):

        print("Processing Type 14")

        Bulletin = GlobalDefinitions.Global.Bulletin
        MyMap = GlobalDefinitions.Global.MyMap

        packet = Safety_related_broadcast_message(aisobject)
        diagnostic = False

        #  bulletin rolls over mod 10
        Bulletin += 1
        Bulletin = Bulletin % 10
        try:

            if diagnostic:
                print("Bulletin {:d} {:s}".format(Bulletin, aisobject.Safetytext))

            SendAPRS.SendAPRS(packet.message_type, packet, False, Bulletin)
        except Exception as e:
            raise RuntimeError("Exception while processing Type14", e, "\r\n") from e

    def Process24(self, aisobject):

        print("Processing Type 24")
        MyMap = GlobalDefinitions.Global.MyMap
        Type24s = Static_data_report.Type24s
        diagnostic = False
        diagnostic2 = False
        diagnostic3 = False


        packet = Static_data_report(aisobject)

        logging.debug("into process 24 MMSI = " + str(packet.extract_int(8, 30)))


        PartType = packet.part_number
        MMSI = packet.mmsi


        try:
            logging.debug("Looking for MMSI in Type24s " + MMSI)
            if MMSI in Type24s:

                # print(
                #     "Found MMSI in 24s",
                #     MMSI,
                #     Type24s[MMSI].vessel_name,
                #     Type24s[MMSI].callsign
                # )
                print(Type24s)
                #  There is an existing type24 record in the dictionary for this MMSI
                new24 = Type24s[MMSI]
                    # now update the record with new data
                try:
                    new24.update(packet)
                    Type24s[MMSI] = new24
                    logging.debug(
                        " After type24s update For MMSI {} {} {}".format(
                            MMSI,
                            Type24s[MMSI].Name,
                            Type24s[MMSI].Callsign,
                        )
                    )
                except RuntimeError as e:
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

                except UnboundLocalError as e:
                    raise UnboundLocalError( 'Unbound error at line 345 of Process AISClasses', e) from e
                except AttributeError as e:
                    raise AttributeError( 'Attribute error at line 345 of Process AISClasses', e) from e

                logging.debug("ValidA = {} ValidB = {}".format(new24.Valid_A, new24.Valid_B))
                try:
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
                except RuntimeError as e:
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

                except UnboundLocalError as e:
                    raise UnboundLocalError( 'Unbound error at line 394 of Process AISClasses', e) from e
                except AttributeError as e:
                    raise AttributeError( 'Attribute error at line 394 of Process AISClasses', e) from e

            else:  # this is a new Type24 MMSI
                # instantiate a Type24 object and put it into the Type24s Dictionary
                try:
                    new24 = packet
                    Type24s[MMSI] = new24
                except RuntimeError as e:
                    raise RuntimeError(
                        "Exception while processing new Type 24\r\n"
                        + "ShipType {:d} Vendor {:s} Model {:d} Callsign {:s} \r\n"
                        + "DimBow {:d} DimStern {:d} DimPort {:d} DimStartboard {:d}\r\n MotherMMSI {:d} "
                        + "Valid {:s}\n\r {:s}\r\n".format(
                            new24.ship_type,
                            new24.vendor_id,
                            new24.unit_model_code,
                            new24.callsign,
                            new24.dim_to_bow,
                            new24.dim_to_stern,
                            new24.dim_to_port,
                            new24.dim_to_stbd,
                            new24.mothership_mmsi,

                            e
                        )
                    ) from e
                except UnboundLocalError as e:
                    raise UnboundLocalError('Unbound error at line 400 of Process AISClasses', e) from e
                except AttributeError as e:
                    raise AttributeError( 'Attribute error at line 400 of Process AISClasses', e) from e
        except Exception as e:
            raise RuntimeError("Exception while processing Type 24", e) from e


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
