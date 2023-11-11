# collection of routines to process the various AIS Classes
#


import GlobalDefinitions
from Map import Map, MapItem
from APRS import SendAPRS
from datetime import datetime
import logging
from Payloads import Payload


class AISClass:

    def __init__(self):
        # there are somethings common to every ais item
        # Messagetpe, RepeatrIndicator,MMSI
        # a bool "test" is defaulted on all routines to facilitate testing

        self.valid_process = False

    def process_generic_class(self, packet: Payload, test: bool = False):
        '''
        Takes in a generic packet and despatches it accordingly


        :param packet:
        :return:
            bool valid_process: True if processed OK, false otherwise
        '''
        self.valid_process = False
        logging.info('Entering ProcessClasses.generic message_type ={}'.format(packet.message_type))

        if packet.message_type in [1, 2, 3, 4, 9, 18, 19, 21, 27]:
            self.valid_process, function = self.do_position(packet, test)
        elif packet.message_type in [5, 24]:
            self.valid_process, function = self.do_data(packet, test)
        elif packet.message_type in [12, 14]:
            self.valid_process, function = self.do_safety(packet, test)
        else:
            pass

        return self.valid_process

    def do_position(self, packet, test: bool = False):
        logging.info('Entering ProcessClasses.do_position')
        logging.debug('In ProcessClasses.do_position Message_type = {}\n{}'
                      .format(packet.message_type, packet))

        if packet.message_type in [19, 21]:
            logging.info('Type 19 or 21 presented')
            try:
                if packet.mmsi in Map.Themap:
                    mapentry = Map.Themap[packet.mmsi]
                    logging.debug(f'map found for {packet.mmsi} map entry {Map.Themap[packet.mmsi]}')
                    if mapentry.vessel_name != packet.vessel_name and packet.vessel_name != '':
                        mapentry.vessel_name = packet.vessel_name

                else:
                    mapentry = MapItem(packet.mmsi, '', packet.vessel_name,
                                           '', datetime.utcnow(), False)

                Map.Themap.update({packet.mmsi: mapentry})
            except Exception as e:
                raise Exception(f'Exception while attempting to update map in ProcessClasses.do_position '
                                f'for types 19 or 21', e) from e

        try:

            if not test:
                logging.info('In ProcessClasses.do_position about to SEndAPRS')
                SendAPRS(packet.message_type, packet, False, 0)
            return True, 'do_position'

        except Exception as e:
            raise RuntimeError(
                    "Error Sending APRS in do_position - Error in SendAPRS \n", e) from e



    def do_data(self, packet, test: bool = False):
        logging.info("ínto ProcessClasses.do_data")
        logging.debug('In ProcessClasses.do_data Message_type = {}\n{}'
                      .format(packet.message_type, packet))

        logging.debug(
            f'Type 5 or 24 presented Type {packet.message_type} mmsi {packet.mmsi}  callsign {packet.callsign} '
            f'name {packet.vessel_name}')

        try:
            if packet.mmsi in Map.Themap:
                mapentry = Map.Themap[packet.mmsi]
                logging.debug(f'map found for {packet.mmsi} map entry {Map.Themap[packet.mmsi]}')
                if mapentry.callsign != packet.callsign and packet.callsign != '':
                    mapentry.callsign = packet.callsign
                if mapentry.vessel_name != packet.vessel_name and packet.vessel_name != '':
                    mapentry.vessel_name = packet.vessel_name
                if packet.message_type == 5:
                    if mapentry.destination != packet.destination and packet.destination != '':
                        mapentry.destination = packet.destination


            else:
                if packet.message_type == 24:
                    # type 24 has no destination attribute
                    mapentry = MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
                                           '', datetime.utcnow(), False)
                else:
                    mapentry = MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
                                           packet.destination, datetime.utcnow(), False





                                       )

                    packet.int_latitude = 91 * 600000
                    packet.latitude = 91.0
                    packet.int_longitude = 181 * 600000
                    packet.longitude = 181
                    SendAPRS(packet.message_type, packet, True, 0)

            Map.Themap.update({packet.mmsi: mapentry})

        except Exception as e:
            logging.error(
                "Exception in processing Type5 establishing mapentry\n {}\nmmsdi {}".format(str(e), packet.mmsi),
                stack_info=True)
            raise RuntimeError("Exception in ProcessClasses.do_data create mapentry", e) from e

        return True, 'do_data'

    def do_safety(self, packet, test: bool = False):
        logging.info("ínto ProcessClasses.do_safety")
        logging.debug('In ProcessClasses.do_safety Message_type = {}\n{}'
                      .format(packet.message_type, packet))

        bulletin = GlobalDefinitions.Global.Bulletin

        #  bulletin rolls over mod 10
        bulletin += 1
        bulletin = bulletin % 10
        try:
            if not test:
                logging.info('In ProcessClasses.do_safety about to SEndAPRS')
                SendAPRS(packet.message_type, packet, False, bulletin)
            return True, 'do_safety'
        except Exception as e:
            raise RuntimeError("Exception in ProcessClasses.do_safety, probable failure in SendAPRS", e, "\r\n") from e

    def donothing(payload_type: int, aisobject):
        pass

    # def Process1239_18(payload_type: int, aisobject, test: bool = False):
    #     """
    #     AIS Object is an AISData object containing both
    #      the payload and a binary version of the payload
    #      input:
    #         a binary payload string
    #
    #     output:
    #         call to SendAPRS
    #     """
    #
    #     tcpstream = ""
    #
    #     logging.info("into process1239_18")
    #
    #     try:
    #
    #         logging.debug("processing type {} \n Payload {}".format(payload_type, aisobject))
    #
    #         if payload_type == 9:
    #             try:
    #                 packet = SAR_aircraft_position_report(aisobject)
    #                 logging.debug(
    #                     "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
    #                     " Altitude {} SOG {:03.0f} COG {:03.0f} ".format(
    #                         payload_type,
    #                         packet.mmsi,
    #                         packet.latitude,
    #                         packet.longitude,
    #                         packet.altitude,
    #                         packet.speed_over_ground,
    #                         packet.course_over_ground
    #
    #                     )
    #                 )
    #             except Exception as e:
    #                 logging.error('ProcessClasses do 9 line 68 ', stack_info=True)
    #                 raise Exception('ProcessClasses do 9', e) from e
    #         elif payload_type == 18:
    #             try:
    #                 packet = ClassB_position_report(aisobject)
    #                 logging.debug(
    #                     "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
    #                     "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
    #                         payload_type,
    #                         packet.mmsi,
    #                         packet.latitude,
    #                         packet.longitude,
    #                         packet.speed_over_ground,
    #                         packet.course_over_ground,
    #                         packet.true_heading,
    #                     )
    #                 )
    #             except Exception as e:
    #                 raise Exception('ProcessClasses do 18', e) from e
    #         else:
    #             try:
    #                 packet = CNB(aisobject)
    #                 logging.debug(
    #                     "payload_type {:d} MMSI {}  Latitude {:06.2f} Longitude {:06.2f} "
    #                     "SOG {:03.0f} COG {:03.0f} HDG {:03.0f}".format(
    #                         payload_type,
    #                         packet.mmsi,
    #                         packet.latitude,
    #                         packet.longitude,
    #                         packet.speed_over_ground,
    #                         packet.course_over_ground,
    #                         packet.true_heading
    #                     )
    #                 )
    #             except Exception as e:
    #                 raise Exception('ProcessClasses do 123', e) from e
    #
    #         if packet.mmsi in Map.Themap:
    #             try:
    #                 mapentry = Map.Themap[packet.mmsi]
    #             except Exception as e:
    #                 raise Exception('Process 123 getting mapentry', e) from e
    #             try:
    #                 mapentry = mapentry.coordinate_map(packet)
    #             except Exception as e:
    #                 raise Exception('Process 123 do coordinatemap', e) from e
    #
    #             try:
    #                 packet.callsign = mapentry.get_callsign()
    #                 packet.vessel_name = mapentry.get_vessel_name()
    #
    #                 logging.debug("1239_18 Callsign = {}  1239_18Name = {}"
    #                               .format(packet.callsign, packet.vessel_name))
    #             except Exception as e:
    #                 raise Exception('ProcessClasses.line 148 ', e) from e
    #
    #
    #         else:
    #             mapentry = Map.MapItem(packet.mmsi, '','','')
    #             mapentry.update_map(packet)
    #
    #         try:
    #             if not test:
    #                 SendAPRS.SendAPRS(packet.message_type, packet, False, 0)
    #             else:
    #                 pass
    #         except Exception as e:
    #             raise RuntimeError(
    #                 "Error Sending APRS in 12349 - Error in SendAPRS \n", e, "\r\n"
    #             ) from e
    #
    #     except Exception as e:
    #         logging.error("Exception while processing Type 123_9_18" + str(e), stack_info=True)
    #         raise RuntimeError(
    #             "Exception while processing payload_type 1, 2 , 3 or 9 \n", e) from e

    # def Process4(self, aisobject, test: bool = False):
    #     try:
    #         packet = Basestation(aisobject)
    #         logging.info(" processing payload_type 4")
    #         logging.debug(
    #             " Base Station {:s}   {:f} {:f}".format(
    #                 packet.mmsi,
    #                 packet.latitude,
    #                 packet.longitude,
    #             )
    #         )
    #         try:
    #             if not test:
    #                 SendAPRS.SendAPRS(packet.message_type, packet, False, 0)
    #             else:
    #                 pass
    #         except Exception as e:
    #             raise Exception('In PreocessClases.do4 line 177 ', e) from e
    #
    #     except Exception as e:
    #         logging.error("Exception while processing Type 4 " + str(e), stack_info=True)
    #         raise RuntimeError("Exception while processing payload_type4", e) from e

    # def Process5(self, aisobject, test: bool = False):
    # logging.info("ínto Process 5")
    #
    # try:
    #     packet = StaticData(aisobject)
    # except Exception as e:
    #     logging.error("Exception while creating type 5 packet in Process 5\n {}\nbinary payload\n {}"
    #                   .format(str(e),aisobject ), stack_info=True)
    #     raise RuntimeError("Exception while processing Type5 create packet", e) from e
    #
    # logging.debug(
    #     "{:s}  Class A Vessel Named {:s} Callsign {:s} Destination {:s} Ship_type {:d}".format(
    #         packet.mmsi,
    #         packet.vessel_name,
    #         packet.callsign,
    #         packet.destination,
    #         packet.ship_type
    #             )
    #         )
    # try:
    #     if packet.mmsi in Map.Themap:
    #         mapentry = Map.Themap[packet.mmsi]
    #
    #     else:
    #         mapentry = Map.MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
    #                                packet.destination, datetime.utcnow(), False)
    # except Exception as e:
    #     logging.error("Exception in processing Type5 establihing mapentry\n {}\nmmsdi {}".format(str(e), packet.mmsi),
    #               stack_info=True)
    #     raise RuntimeError("Exception while processing Type5 create mapentry", e) from e
    # try:
    #     mapentry.update_map(packet)
    # except Exception as e:
    #     logging.error("Exception in processing Type5 updating map\n {}\n{}"
    #                   .format(str(e), packet), stack_info=True)
    #     raise RuntimeError("Exception while processing Type5 update map", e) from e

    # region Process14
    # def Process14(self, aisobject, test: bool = False):
    #     try:
    #         logging.debug("Processing Type 14")
    #
    #         Bulletin = GlobalDefinitions.Global.Bulletin
    #         MyMap = GlobalDefinitions.Global.MyMap
    #
    #         packet = Safety_related_broadcast_message(aisobject)
    #         diagnostic = False
    #
    #         #  bulletin rolls over mod 10
    #         Bulletin += 1
    #         Bulletin = Bulletin % 10
    #         try:
    #             logging.debug("Bulletin {:d} {:s}".format(Bulletin, aisobject.Safetytext))
    #             if not test:
    #                 SendAPRS.SendAPRS(packet.message_type, packet, False, Bulletin)
    #             else:
    #                 pass
    #
    #         except Exception as e:
    #             raise RuntimeError("Exception while processing Type14", e, "\r\n") from e
    #     except Exception as e:
    #         raise Exception('Process14', e) from e

    # def Process24(self, aisobject, test: bool = False):
    # try:
    #     packet = Static_data_report(aisobject)
    #     logging.debug("into process 24 MMSI = {}".format(str(packet.extract_int(8, 30))))
    #     Themap = Map.Map.Themap
    #     PartType = packet.part_number
    #     MMSI = packet.mmsi
    #
    #     logging.debug('do_24 line 297 \n{}'.format(Static_data_report.T24Records[MMSI]))
    #
    #     try:
    #         if packet.mmsi in Themap:
    #             mapentry = Themap[packet.mmsi]
    #         else:
    #             mapentry = Map.MapItem(packet.mmsi, packet.callsign, packet.vessel_name,
    #                                    '', datetime.utcnow(), False)
    #         mapentry = mapentry.update_map(packet)
    #
    #
    #     except Exception as e:
    #         raise RuntimeError("Exception while processing Type 24 updating map", e) from e
    # except Exception as e:
    #     raise Exception('Process24', e) from e


def main(self):
    pass


if __name__ == 'main':
    main()
