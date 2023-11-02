import logging

import GetUDP
import GetSerial
import GlobalDefinitions
from GetFileData import FileData
import Process_AIS_Classes
import sys
import datetime
import MyPreConfigs
from GlobalDefinitions import Global
from threading import Thread
import Statistics
import logging
from Payloads import AISStream, AISDictionaries,  Fragments
from Payloads import Basic_Position, Basestation, CNB, Static_data_report
from Payloads import StaticData, SAR_aircraft_position_report
from Payloads import Safety_related_broadcast_message, Addressed_safety_related_message,Long_range_AIS_broadcast_message


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


def main():
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

        try:  # all encompassing catch of exceptions to allow restart
            if not Global.inputqueue.empty():
                try:

                    stringer = Global.inputqueue.get()
                    current_ais = AISStream(stringer)
                    logging.debug(" input queue item = ", current_ais)


                    processed = False  # indicate we have an unprocessed record

                except Exception as e:
                    if inqueue.empty():
                        print("queue empty")
                    elif inqueue.full():
                        print("queue full")
                    else:
                        print("??? in main re queue state")
                    raise RuntimeError("getting queued item in main - error", e) from e
            else:
                # no record to process at the moment - loop
                pass

            # now the guts of processing the incoming AIS Data
            # have an  encoded string break it down
            if not processed and current_ais.valid_message:




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
                if current_ais.fragment_count == 1:
                    # print('doing stuff nonfragmented pasyload id =',myAIS.AIS_Payload_ID)
                    do_function(current_ais.message_type, current_ais.binary_payload)
                    processed = True
                else:
                    # now handle the fragments
                    # function will return True when fragments have been merged
                    # declare stream to be a fragment
                    current_frag = Fragments(current_ais.binary_payload,current_ais.fragment_count,
                                             current_ais.fragment_number, current_ais.message_id)
                    current_frag.put_frag_in_dict(True)
                    if current_frag.success:
                        current_ais.binary_payload = current_frag.new_bin_payload
                        do_function(current_ais.message_type, current_ais.binary_payload)
                        Processed = True
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
            sys.exit()

        except Exception as e:
            print("Restarting processes after exception\r\n", e)
            logging.error("Restarting processes after exception", stack_info=True)

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


def do_function(keyword, aisobject: AISStream):
    # create a dictionary of functions related to keywords that might be being initialised
    #

    ParseDict = {
        0: Process_AIS_Classes.AISClass.donothing,  # this is an error condition and should not occur
        1: Process_AIS_Classes.AISClass.Process1239_18,
        2: Process_AIS_Classes.AISClass.Process1239_18,
        3: Process_AIS_Classes.AISClass.Process1239_18,
        4: Process_AIS_Classes.AISClass.Process4,
        5: Process_AIS_Classes.AISClass.Process5,
        6: Process_AIS_Classes.AISClass.donothing,
        7: Process_AIS_Classes.AISClass.donothing,
        8: Process_AIS_Classes.AISClass.donothing,
        9: Process_AIS_Classes.AISClass.Process1239_18,
        10: Process_AIS_Classes.AISClass.donothing,
        11: Process_AIS_Classes.AISClass.donothing,
        12: Process_AIS_Classes.AISClass.donothing,
        13: Process_AIS_Classes.AISClass.donothing,
        14: Process_AIS_Classes.AISClass.Process14,
        15: Process_AIS_Classes.AISClass.donothing,
        16: Process_AIS_Classes.AISClass.donothing,
        17: Process_AIS_Classes.AISClass.donothing,
        18: Process_AIS_Classes.AISClass.Process1239_18,
        19: Process_AIS_Classes.AISClass.donothing,
        20: Process_AIS_Classes.AISClass.donothing,
        21: Process_AIS_Classes.AISClass.donothing,
        22: Process_AIS_Classes.AISClass.donothing,
        23: Process_AIS_Classes.AISClass.donothing,
        24: Process_AIS_Classes.AISClass.Process24,
        25: Process_AIS_Classes.AISClass.donothing,
        26: Process_AIS_Classes.AISClass.donothing,
        27: Process_AIS_Classes.AISClass.donothing,
        30: Process_AIS_Classes.AISClass.donothing,  # catchall for malformed packet
    }
    # print('keyword ', keyword, ' payload ',aisobject )
    if keyword in ParseDict:
        return ParseDict[keyword](keyword, aisobject)
    else:
        Errmess = "Error handling payload\r\n"
        if isinstance(keyword, int) or isinstance(keyword, float):
            c_keyword = str(keyword)
            Errmess = (
                Errmess + "Function to handle payload_ID " + c_keyword + "  unknown"
            )

        elif isinstance(keyword, str):
            c_keyword = keyword
            Errmess = (
                Errmess + "Function to handle payload_ID " + c_keyword + "  unknown"
            )
        else:
            c_keyword = type(keyword)
            Errmess = (
                Errmess + "Function to handle payload_ID " + c_keyword + "  unknown"
            )

        print(Errmess + "\nAIS Data PayLoad is\n" + aisobject.AIS_Payload)
        logging.debug(Errmess + "\nAIS Data PayLoad is\n" + aisobject.AIS_Payload)
        return None


#
sys.stdout = Global.stdout
sys.stdin = Global.stdin
sys.stderr = Global.stderr

if __name__ == "__main__":
    main()
