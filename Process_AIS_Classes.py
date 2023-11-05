# collection of routines to process the various AIS Classes
#


import GlobalDefinitions
import Map
from GlobalDefinitions import Global
import SendAPRS
from datetime import datetime
import logging
from Payloads import Basestation, CNB, Static_data_report, ClassB_position_report
from Payloads import StaticData, SAR_aircraft_position_report
from Payloads import Safety_related_broadcast_message


class AISClass:

    def __init__(self):
        # there are somethings common to every ais item
        # Messagetpe, RepeatrIndicator,MMSI
        pass

    def donothing(payload_type: int, aisobject):
        pass

    def Process1239_18(payload_type: int, aisobject):
        """
        AIS Object is an AISData object containing both
         the payload and a binary version of the payload
        """

        tcpstream = ""

        logging.info("into process1239_18")

        try:

            logging.debug("processing type {} \n Payload {}".format(payload_type, aisobject))

            if payload_type == 9:
                try:
                    packet = SAR_aircraft_position_report(aisobject)
                    logging.debug(
                        "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
                        " Altitude {} SOG {:03.0f} COG {:03.0f} ".format(
                            payload_type,
                            packet.mmsi,
                            packet.latitude,
                            packet.longitude,
                            packet.altitude,
                            packet.speed_over_ground,
                            packet.course_over_ground

                        )
                    )
                except Exception as e:
                    logging.error('ProcessClasses do 9 line 68 ', stack_info=True)
                    raise Exception('ProcessClasses do 9', e) from e
            elif payload_type == 18:
                try:
                    packet = ClassB_position_report(aisobject)
                    logging.debug(
                        "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
                        "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                            payload_type,
                            packet.mmsi,
                            packet.latitude,
                            packet.longitude,
                            packet.speed_over_ground,
                            packet.course_over_ground,
                            packet.true_heading,
                        )
                    )
                except Exception as e:
                    raise Exception('ProcessClasses do 18', e) from e
            else:
                try:
                    packet = CNB(aisobject)
                    logging.debug(
                        "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
                        "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
                            payload_type,
                            packet.mmsi,
                            packet.latitude,
                            packet.longitude,
                            packet.speed_over_ground,
                            packet.course_over_ground,
                            packet.true_heading
                        )
                    )
                except Exception as e:
                    raise Exception('ProcessClasses do 123', e) from e

            if packet.mmsi in Global.Themap:
                try:
                    mapentry = Global.Themap[packet.mmsi]
                except Exception as e:
                    raise Exception('Process 123 getting mapentry', e) from e
                try:
                    mapentry = mapentry.coordinate_map(packet)
                except Exception as e:
                    raise Exception('Process 123 do coordinatemap', e) from e

                try:
                    packet.callsign = mapentry.get_callsign()
                    packet.vessel_name = mapentry.get_vessel_name()

                    logging.debug("1239_18 Callsign = {}  1239_18Name = {}"
                                  .format(packet.callsign, packet.vessel_name))
                except Exception as e:
                    raise Exception('ProcessClasses.line 148 ', e) from e

                try:
                    SendAPRS.SendAPRS(packet.message_type, packet, False, 0)
                except Exception as e:
                    raise RuntimeError(
                        "Error Sending APRS in 12349 - Error in SendAPRS \n", e, "\r\n"
                    ) from e

        except Exception as e:
            logging.error("Exception while processing Type 123_9_18" + str(e), stack_info=True)
            raise RuntimeError(
                "Exception while processing payload_type 1, 2 , 3 or 9 \n", e) from e

    def Process4(self, aisobject):
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
            try:
                SendAPRS.SendAPRS(packet.message_type, packet, False, 0)
            except Exception as e:
                raise Exception('In PreocessClases.do4 line 177 ', e) from e

        except Exception as e:
            logging.error("Exception while processing Type 4 " + str(e), stack_info=True)
            raise RuntimeError("Exception while processing payload_type4", e) from e

    def Process5(self, aisobject):
        logging.info("ínto Process 5")

        try:
            packet = StaticData(aisobject)

            logging.debug(
                "{:s}  Class A Vessel Named {:s} Callsign {:s} Destination {:s} Ship_type {:d}".format(
                    packet.mmsi,
                    packet.vessel_name,
                    packet.callsign,
                    packet.destination,
                    packet.ship_type
                )
            )
            if packet.mmsi in Global.Themap:
                mapentry = Global.Themap[packet.mmsi]

            else:
                mapentry = Map.MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
                                       packet.destination, datetime.utcnow(), False)

            mapentry.update_map(packet)



        except Exception as e:
            logging.error("Exception while processing Type5" + str(e), stack_info=True)
            raise RuntimeError("Exception while processing Type5", e) from e

    # region Process14
    def Process14(self, aisobject):
        try:
            logging.debug("Processing Type 14")

            Bulletin = GlobalDefinitions.Global.Bulletin
            MyMap = GlobalDefinitions.Global.MyMap

            packet = Safety_related_broadcast_message(aisobject)
            diagnostic = False

            #  bulletin rolls over mod 10
            Bulletin += 1
            Bulletin = Bulletin % 10
            try:
                logging.debug("Bulletin {:d} {:s}".format(Bulletin, aisobject.Safetytext))

                SendAPRS.SendAPRS(packet.message_type, packet, False, Bulletin)

            except Exception as e:
                raise RuntimeError("Exception while processing Type14", e, "\r\n") from e
        except Exception as e:
            raise Exception('Process14', e) from e

    def Process24(self, aisobject):
        try:
            packet = Static_data_report(aisobject)
            logging.debug("into process 24 MMSI = " + str(packet.extract_int(8, 30)))
            Themap = Map.Map.Themap
            PartType = packet.part_number
            MMSI = packet.mmsi

            logging.debug('do_24 line 297 \n{}'.format(Static_data_report.T24Records[MMSI]))

            try:
                if packet.mmsi in Themap:
                    mapentry = Themap[packet.mmsi]
                else:
                    mapentry = Map.MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
                                           '', datetime.utcnow(), False)
                mapentry = mapentry.update_map(packet)


            except Exception as e:
                raise RuntimeError("Exception while processing Type 24 updating map", e) from e
        except Exception as e:
            raise Exception('Process24', e) from e


def main(self):
    pass


if __name__ == 'main':
    main()
