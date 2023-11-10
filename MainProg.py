import logging
import time

import GetUDP
import GetSerial
from GetFileData import FileData
from Process_AIS_Classes import AISClass
import sys
import MyPreConfigs
import GlobalDefinitions
from GlobalDefinitions import Global
from threading import Thread
import Statistics
import logging
from Payloads import AISStream, Fragments, CNB, ClassB_position_report, Extende_ClassB_position_report
from Payloads import StaticData, SAR_aircraft_position_report, Static_data_report, Safety_related_broadcast_message
from Payloads import Addressed_safety_related_message, Basestation
from Payloads import Aid_to_navigation_report, Long_range_AIS_broadcast_message, Payload


"""
Controlling program for the system

First initialise any Preconfigured parameters from an ini file
by instantiating a Global object

then start up the data gathering threads
    may be one or more of UDP or serial but only one of each
these communicate back to the AIS Processing functions in this module by means of a queue

then start up the send to APRS thread
    also communicating by means of another queue

and finally start up a thread to report statistics communicating by yet another queue

"""
Themap = {}

def main():

    logging.basicConfig(level=logging.ERROR, filename="error.log")
    #logging.basicConfig(level=logging.ERROR)

    inqueue = Global.inputqueue
    #outqueue = Global.outputqueue
    Statsqueue = Global.Statsqueue
    try:

        initialise = MyPreConfigs.MyPreConfigs()

    except Exception as e:
        logging.critical("error initialising PreConfigs", e)
        raise RuntimeError("error initialising PreConfigs", e) from e
    """ the __init__ function in MyPreconfigs will read ini file
    and set any variables that are different from the defaults
    """

    diagnostic = Global.diagnostic
    diagnostic2 = Global.diagnostic2
    diagnostic3 = Global.diagnostic3

    FragDict = Fragments.FragDict


    try:
        # start the data gathering

        if Global.Use_UDP:
            x = GetUDP.GetDataUDP("", 4158)
            tudp = Thread(target=x.GetUDPData, args=())
            tudp.start()

        if Global.Use_Serial:
            y = GetSerial.GetSerial(Global.ComPort, Global.ComSpeed)
            tserial = Thread(target=y.GetSerial, args=())
            tserial.start()

        if Global.Use_AISfile:
            z = FileData()
            treadfile = Thread(target=z.ReadAISFile, args=())
            treadfile.start()

        # and start up a thread looking after reporting Statistics
        # dst = Statistics.statistics()
        sts = Statistics.Statistics()
        tstats = Thread(target=sts.loopstats, args=())
        tstats.start()

    except Exception as e:
        logging.critical("Error starting threads", e)
        print("Error starting threads", e)

    # ##################################################################################################################
    stringer = ""  # will hold incoming encoded AIS string

    processed = True
    while not GlobalDefinitions.Global.CloseDown:
        try:
            try:  # all encompassing catch of exceptions to allow restart
                if not Global.inputqueue.empty():
                    processed = True
                    try:
                        stringer = Global.inputqueue.get()
                    except Exception as e:
                        raise Exception('Error getting aisitem', e) from e
                    try:
                        if len(stringer) == 0:
                            logging.error("Exception zero length payload presented to CreateStream")
                            processed = True
                        else:
                            current_ais = AISStream(stringer)
                            logging.debug(" input queue item = {}".format(current_ais))
                            if current_ais.valid_message:
                                processed = False  # indicate we have an unprocessed record
                    except Exception as e:
                        logging.error('Error creating AISStream',stack_info=True)
                        raise Exception('Error creating AISStream', e) from e
                else:
                    # no record to process at the moment - loop
                    pass

            except Exception as e:
                if inqueue.empty():
                    print("queue empty")
                elif inqueue.full():
                    print("queue full")
                else:
                    print("??? in main re queue state")
                raise RuntimeError("getting queued item in main - error", e) from e

            # now the guts of processing the incoming AIS Data
            # have an  encoded string break it down

            if not processed and current_ais.valid_message:
                try:
                    """
                    We now have a payload, a payload_id
                    can start to parse the payload
                    no case statement in python
                    use a dictionay matching payload_id to function to do the parse
                    """
                    # do whatever function is necessary
                    # calls do_function
                    # the value parameter will probably need tweaking depending on the payload_id
                    # most times it will be either payload or binary_payload I think

                    # print('Checking for fragments ', aisfields[1],myAIS.AIS_FragCount)
                    # TEMPORARY ######throw away fragmented packets
                    packet: Payload = None

                    if current_ais.fragment_count == 1 and current_ais.fragment_number ==1:
                        try:
                            logging.info('doing stuff nonfragmented pasyload id ={}'.format(current_ais.message_type))
                            packet = do_function(current_ais.message_type, current_ais.binary_payload)
                        except Exception as e:
                            raise Exception('In setting packet type prior to processing Main.line 151 ', e) from e
                    else:
                        # now handle the fragments
                        # function will return True when fragments have been merged
                        # declare stream to be a fragment
                        #print('doing fragment')
                        current_frag = Fragments(current_ais.binary_payload,current_ais.fragment_count,
                                                     current_ais.fragment_number, current_ais.message_id)
                        try:
                            current_frag.put_frag_in_dict(True)
                        except Exception as e:
                            raise Exception('Main line 149 ', e) from e
                        if current_frag.success:
                            current_ais.binary_payload = current_frag.new_bin_payload
                            current_ais.message_type = int(current_ais.binary_payload[0:6], 2)
                            packet = do_function(current_ais.message_type, current_ais.binary_payload)

                    # now process the packet
                    if packet != None:      # if non valid packet dump it
                        thisclass = AISClass()
                        logging.info('About to send poacket tp ProcessClasses message_type = {}'
                                     .format(packet.message_type))
                        try:
                            valid_process = thisclass.process_generic_class(packet)
                        except Exception as e:
                            raise Exception('Exception when despatching in ProcessClasses in Main', e) from e
                        if valid_process:
                            processed = True
                except Exception as e:
                    raise Exception('Main line 124-160', e) from e
            else:
                pass  # wait for next record


            if not Statsqueue.empty():
                do_stats()
                if diagnostic3:
                    for xx in Global.Statistics:
                        print(xx, Global.Statistics[xx])
                    for xx in Global.UDP_Received_IP_Addresses:
                        print(xx)




        except KeyboardInterrupt as e:
            print('Keyboard Interrupt occurred - ending threads and exiting')
            GlobalDefinitions.Global.CloseDown = True
            GlobalDefinitions.Global._keepgoing = False
            time.sleep(10)
            sys.exit()

        except AttributeError as e:
            print("Restarting processes after Attribute exception\r\n", e)
            #logging.error("Restarting processes after Attribute exception", stack_info=True)

        except Exception as e:
            print("Restarting processes after exception\r\n", e)
            #logging.error("Restarting processes after Unknown exception", stack_info=True)

        processed = True
        if not Global.Production:
            raise RuntimeError(e) from e




def select_inputs():
    if Global.Use_UDP:
        x = GetUDP.GetDataUDP("", 4158)
        tudp = Thread(target=x.GetUDPData, args=())
        tudp.start()

    if Global.Use_Serial:
        y = GetSerial.GetSerial(Global.ComPort, Global.ComSpeed)
        tserial = Thread(target=y.GetSerial, args=())
        tserial.start()

    if Global.Use_AISfile:
        z = FileData()
        treadfile = Thread(target=z.ReadAISFile, args=())
        treadfile.start()

    return None


def do_stats():
    # reads tupoles off the StatsQueue and uppdates stats
    StatsQ = Global.Statsqueue
    while not StatsQ.empty():
        stat, invalue = StatsQ.get()
        if (
            stat == "Nr_APRS_permin"
            or stat == "Nr_Serial_Frames_permin"
            or stat == "Nr_UDP_Frames_permin"
        ):
            Global.Statistics[stat] = invalue

        else:
            Global.Statistics[stat] = Global.Statistics[stat] + invalue


def ExtractMMSI(Binary_payload):
    # extracts 9 digit MMSI from binary Payload
    pass


# def do_function(keyword, aisobject:str):
#     # create a dictionary of functions related to keywords that might be being initialised
#     #
#     print('entering do function with kedyword = ', keyword)
#     ParseDict = {
#         0: Process_AIS_Classes.AISClass.donothing,  # this is an error condition and should not occur
#         1: Process_AIS_Classes.AISClass.Process1239_18,
#         2: Process_AIS_Classes.AISClass.Process1239_18,
#         3: Process_AIS_Classes.AISClass.Process1239_18,
#         4: Process_AIS_Classes.AISClass.Process4,
#         5: Process_AIS_Classes.AISClass.Process5,
#         6: Process_AIS_Classes.AISClass.donothing,
#         7: Process_AIS_Classes.AISClass.donothing,
#         8: Process_AIS_Classes.AISClass.donothing,
#         9: Process_AIS_Classes.AISClass.Process1239_18,
#         10: Process_AIS_Classes.AISClass.donothing,
#         11: Process_AIS_Classes.AISClass.donothing,
#         12: Process_AIS_Classes.AISClass.donothing,
#         13: Process_AIS_Classes.AISClass.donothing,
#         14: Process_AIS_Classes.AISClass.Process14,
#         15: Process_AIS_Classes.AISClass.donothing,
#         16: Process_AIS_Classes.AISClass.donothing,
#         17: Process_AIS_Classes.AISClass.donothing,
#         18: Process_AIS_Classes.AISClass.Process1239_18,
#         19: Process_AIS_Classes.AISClass.donothing,
#         20: Process_AIS_Classes.AISClass.donothing,
#         21: Process_AIS_Classes.AISClass.donothing,
#         22: Process_AIS_Classes.AISClass.donothing,
#         23: Process_AIS_Classes.AISClass.donothing,
#         24: Process_AIS_Classes.AISClass.Process24,
#         25: Process_AIS_Classes.AISClass.donothing,
#         26: Process_AIS_Classes.AISClass.donothing,
#         27: Process_AIS_Classes.AISClass.donothing,
#         30: Process_AIS_Classes.AISClass.donothing,  # catchall for malformed packet
#     }
#     # print('keyword ', keyword, ' payload ',aisobject )
#     if keyword in ParseDict:
#         return ParseDict[keyword](keyword, aisobject)
#     else:
#         Errmess = "Error handling payload\r\n"
#         if isinstance(keyword, int) or isinstance(keyword, float):
#             c_keyword = str(keyword)
#             Errmess = (
#                 Errmess + "Function to handle payload_ID " + c_keyword + "  unknown"
#             )
#
#         elif isinstance(keyword, str):
#             c_keyword = keyword
#             Errmess = (
#                 Errmess + "Function to handle payload_ID " + c_keyword + "  unknown"
#             )
#         else:
#             c_keyword = type(keyword)
#             Errmess = (
#                 Errmess + "Function to handle payload_ID " + c_keyword + "  unknown" )
#         logging.debug( "{}\nAIS Data PayLoad is\n{}".format(Errmess, aisobject))
#         return None

def do_function(dummy, aisobject:str):
    '''
    Takes in an AIS binary payload and iniates  packet processing

    output:
        may be ither ca call to sendAPRS or null return having updated Map entries
    '''

    message_type = int(aisobject[0:6], 2)       # determine what sort of packet
    logging.info('In do_function message_type = {}'.format(message_type))

    # should do a binary chop to determine what to do but I think is better to just scan in order of likelihood

    if message_type in [1, 2, 3]:
        packet = CNB(aisobject)
    elif message_type == 18:
        packet = ClassB_position_report(aisobject)
    elif message_type == 19:
        packet = Extende_ClassB_position_report(aisobject)
    elif message_type == 9:
        packet = SAR_aircraft_position_report(aisobject)
    elif message_type == 4:
        packet = Basestation(aisobject)
    elif message_type == 5:
        packet = StaticData(aisobject)
    elif message_type == 24:
        packet = Static_data_report(aisobject)
    elif message_type == 21:
        packet = Aid_to_navigation_report(aisobject)
    elif message_type == 12:
        packet = Addressed_safety_related_message(aisobject)
    elif message_type == 14:
        packet = Safety_related_broadcast_message(aisobject)
    elif message_type == 27:
        packet = Long_range_AIS_broadcast_message(aisobject)
    else:
        packet = None       # default do nothing

    return packet





#
sys.stdout = Global.stdout
sys.stdin = Global.stdin
sys.stderr = Global.stderr

if __name__ == "__main__":
    main()
