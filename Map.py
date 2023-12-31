'''
Map.py
Class to hold a map of known vessels, bases etc
contains mmsi, vessel/base/etc name, callsign
Updated by all classes but particularly 1,2,3,5, 9, 24

Used to report on known stations/ships


'''

import time
from datetime import datetime
import logging




class Map:
    # class variable will be generated if not already existing
    Themap = {}

    def __init__(self):
        if len(Map.Themap) == 0:
            mapentry = MapItem('000000000', '', '', '', datetime.utcnow(), False)
            Map.Themap.update({'000000000': mapentry})

    def __repr__(self):
        outstring = f'{self.__class__.__name__}\n'
        for mmsi, data in Map.Themap.items():
            outstring = outstring + (f'MMSI   {mmsi} Callsign {data[0]} Vessel Name {data[1]} '
                                     f'Destination {data[2]} Timestamp {data[3]} Kill_flag {data[4]}\n')

        return outstring


class MapItem:

    def __init__(self, mmsi: str, callsign: str = '', vessel_name: str = '', destination: str = '',
                 timestamp: datetime = datetime.utcnow(), kill_flag: bool = False):
        self.mmsi: str = mmsi
        self.callsign: str = callsign
        self.vessel_name: str = vessel_name
        self.destination: str = destination
        self.timestamp: datetime = timestamp
        self.kill: bool = kill_flag

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'MMSI:             {self.mmsi}\n'
                f'Callsign:         {self.callsign}\n'
                f'Vessel Name:      {self.vessel_name}\n'
                f'Destination:      {self.destination}\n'
                f'Timestamp         {self.timestamp}\n'
                f'Kill              {self.kill}\n'
                )

    def get_callsign(self):
        return self.callsign

    def get_vessel_name(self):
        return self.vessel_name

    def get_destination(self):
        return self.destination

    def get_timestamp(self):
        return self.timestamp

    def get_kill(self):
        return self.kill

    def update_map(self, packet):
        #  check if we have a record in the mapping directory for this MMSI

        if packet.mmsi in Map.Themap:
            if Map.Themap[packet.mmsi].callsign != '':
                packet.callsign = Map.Themap[packet.mmsi].callsign
            if Map.Themap[packet.mmsi].vessel_name != '':
                packet.vessel_name = Map.Themap[packet.mmsi].vessel_name
        else:

            #  no key/value pair exists
            #  send a kill stream for the MMSI referenced version
            #  then create a key/value pair
            #  for the purpose of the exercise the position of the object is set to not available killing
            #  coordinates 90S, 0E

            packet.int_latitude = 91 * 600000
            packet.latitude = 91.0
            packet.int_longitude = 181 * 600000
            packet.longitude = 181
            SendAPRS(packet.message_type, packet, True, 0)

            # update the list of known vessels/bases etc
            if packet.message_type == 5:
                newmap = MapItem(packet.mmsi, packet.callsign, packet.vessel_name, packet.destination,
                                 datetime.utcnow(), False)
            elif packet.message_type == 24:
                newmap = MapItem(packet.mmsi, packet.callsign, packet.vessel_name, '',
                                 datetime.utcnow(), False)
            elif packet.message_type == 19:
                newmap = MapItem(packet.mmsi, '', packet.vessel_name, '',
                                 datetime.utcnow(), False)
            elif packet.message_type == 21:
                newmap = MapItem(packet.mmsi, '', packet.vessel_name, '',
                                 datetime.utcnow(), False)
            else:
                newmap = MapItem(packet.mmsi, '', '', '',
                                 datetime.utcnow(), False)
            Map.Themap.update({packet.mmsi: newmap})
