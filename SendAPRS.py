import MyPreConfigs
import GlobalDefinitions
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR, SOCK_DGRAM
from APRS import APRS
from Payloads import CNB


# region SendAPRS


def SendAPRS(p, mydata, kill: bool, Bulletin: int):

    print('into sendAPRS with message type {} '.format(mydata.message_type))

    #  takes analysed AIS stream and at periodic intervals sends to APRS server
    tcpbytes = bytearray("", "utf-8")
    try:
        myaprs = APRS(
            mydata.mmsi,
            mydata.latitude,
            mydata.longitude,
            mydata.course_over_ground,
            mydata.speed_over_ground,
            mydata.vessel_name,
            mydata.isAVCGA
        )

        myaprs.MMSI = mydata.mmsi
        if len(mydata.callsign) > 0:
            myaprs.Callsign = mydata.callsign

    except Exception as e:
        raise RuntimeError("Error creating myaprs in SendAPRS", e) from e

        # switch (p)
        # switch statements not available simulate with dictionary of things to do
    thisswitch = {
        1: doposition,
        2: doposition,
        3: doposition,
        4: do4,
        5: do5_24,
        6: donothing,
        7: donothing,
        8: donothing,
        9: doposition,
        10: donothing,
        11: donothing,
        12: donothing,
        13: donothing,
        14: do14,
        15: donothing,
        16: donothing,
        17: donothing,
        18: doposition,
        19: donothing,
        20: donothing,
        21: donothing,
        22: donothing,
        23: donothing,
        24: do5_24,
        25: donothing,
        26: donothing,
        27: donothing,
        28: donothing,
    }

    # types 1,2 , 3, 9 and 18 position reports
    #            if ((mydata.Latitude < 91) && (mydata.Longitude < 181))  #  only send valid lat/long to server
    try:

        if mydata.callsign == "":
            xcallsign = mydata.mmsi
        else:
            xcallsign = mydata.callsign

        tcpbytes = thisswitch[p]((mydata, myaprs), Bulletin, kill)

        #  now queue the aprs stream
        QueueAPRS(xcallsign, tcpbytes)

        try:
            TransmitAPRS(tcpbytes)
        except Exception as e:
            raise RuntimeError(
                "Error Attempting to Transmit APRS following queuing", e
            ) from e

        # finished with myaprs dispose of it
        del myaprs

    except Exception as e:
        raise RuntimeError(
            "Exception while processing tcpbytes queue/transmit  \n", e
        ) from e


def donothing():
    #print('In SendAPRS.donothing')
    pass


def doposition(args, dummy: int, kill: bool):
    #print('In SendAPORS.doposition')
    try:
        mydata = args[0]
        myaprs = args[1]

        tcpbytes = bytearray(myaprs.CreateObjectPosition(True, mydata), "utf-8")

        return tcpbytes

    except Exception as e:
        raise RuntimeError(
            "Exception while processing (queue) Type 1,2,3,9,18", e
        ) from e


def do4(args, dumbull: int, dummy: bool):
    #'In SendAPORS.do4')
    try:
        # print(myaprs.CreateObjectPosition())
        args1, args2 = args
        tcpbytes = bytearray(args2.CreateBasePosition(), " utf-8")

        return tcpbytes

    except Exception as e:
        raise RuntimeError("Exception while processing (queue) Type 4", e) from e


def do14(args, Bulletin: int, dummy: bool):
    #print('In SendAPORS.do14')
    try:
        tcpbytes = bytearray(args.CreateSafetyMessage(Bulletin), "utf-8")

        return tcpbytes

    except Exception as e:
        raise RuntimeError("Exception while processing (queue) Type 14", e) from e


def do5_24(args, dumbull: int, kill: bool):
    #print('In SendAPORS.do5_24')
    try:
        # APRS myaprs = new APRS(mydata.String_MMSI, mydata.Latitude, mydata.Longitude, mydata.COG, mydata.SOG, "")
        args1, args2 = args
        args2.Course = str(args1.COG)
        args2.Speed = str(args1.SOG)

        #                   print(myaprs.CreateObjectPosition())
        tcpbytes = bytearray(args2.CreateObjectPosition(kill, args1), "utf-8")

        return tcpbytes

    except Exception as e:
        raise RuntimeError("Exception while processing (queue) Type 5,24", e) from e


def QueueAPRS(Callsign: str, tcpbytes):
    #print('In SendAPORS.QueueAPRS')
    #  queues APRS text streams deleting duplicates
    #  uses dictionary ServerQueue to hold APRS byte steam keyed on the Callsign field
    #
    #  need to convert the byte array tcpbytes to a string before attempting to check for duplicates
    #

    """# FOR TESTING
    #############################################
    print('FOR TESTING\r\nEntering QueueAPRS\r\nCallsign= {}\r\ntcpbytes ={}' \
    .format(Callsign,tcpbytes))

    ##############################################
    """

    aprsstring = tcpbytes.decode()

    diagnostic = GlobalDefinitions.Global.diagnostic
    diagnostic2 = GlobalDefinitions.Global.diagnostic2
    diagnostic3 = GlobalDefinitions.Global.diagnostic3
    ServerQueue = GlobalDefinitions.Global.ServerQueue

    diagnostic2 = False
    diagnostic3 = False

    if diagnostic2:
        print("In QueueAPRS aprsstring = ", aprsstring)

    try:
        if Callsign in ServerQueue:
            #  already an entry in the queue
            try:
                if ServerQueue[Callsign] != aprsstring:
                    # print('in queue aprs replacing\n', ServerQueue[Callsign], 'with\n', aprsstring)
                    #  need to delete current value in queue and replace by new value
                    ServerQueue[Callsign] = aprsstring
            except KeyError:
                pass

                if diagnostic2:
                    print("In QueueAPRS Queue Count = {}".format(len(ServerQueue)))
                    for xx in ServerQueue:
                        print("MMSI {} Data {} ".format(xx, ServerQueue[xx]))

                #  otherwise do nothing its a duplicate

        else:
            #  Create an entry in queue
            if diagnostic2:
                print("adding record to QueueAPRS ", Callsign, " : ", aprsstring)

            ServerQueue.update({Callsign: aprsstring})

            if diagnostic2:
                print("In QueueAPRS Queue NewEntry Count = {}".format(len(ServerQueue)))

    except Exception as e:
        print("Error while queuing APRS")
        raise RuntimeError("Error in Queue APRS\r\n", e) from e


def Do_diag_print(DiagBool, diagstr):
    if DiagBool:
        print(diagstr)


def TransmitAPRS(tcpstream):
    #print('In SendAPORS.TransmitAPRS')
    diagnostic = GlobalDefinitions.Global.diagnostic
    diagnostic2 = GlobalDefinitions.Global.diagnostic2
    diagnostic3 = GlobalDefinitions.Global.diagnostic3
    diagnostic_Level = GlobalDefinitions.Global.diagnostic_Level

    StatsQ = GlobalDefinitions.Global.Statsqueue
    UseRemote = GlobalDefinitions.Global.UseRemote
    LogAPRS = GlobalDefinitions.Global.LogAPRS
    APRSLogFile = GlobalDefinitions.Global.APRSFileName

    LastTransmit = GlobalDefinitions.Global.LastTransmit
    ServerQueue = GlobalDefinitions.Global.ServerQueue
    NoConnect = GlobalDefinitions.Global.NoConnect
    try:  # all encompassing exception  catch all to pass up the tree

        aprs_stream = socket(AF_INET, SOCK_STREAM)
        aprs_stream.close()

        #  having queued APRS stream now we see if it should be sent
        #  compare current time with LastTransmit time
        current = datetime.now()
        difference = current - GlobalDefinitions.Global.LastTransmit

        diagstr = "tx timedifference {0}".format(difference.total_seconds())
        Do_diag_print(diagnostic3, diagstr)

        if difference.total_seconds() > GlobalDefinitions.Global.ServerPeriod:
            if NoConnect:
                try:
                    aprs_stream = socket(AF_INET, SOCK_STREAM)
                except OSError as e:
                    raise RuntimeError(
                        "Error creating socket in sendAPRS: %s\n" % e
                    ) from e

                # Second try-except block -- connect to given host/port
                try:

                    aprs_stream.connect(define_server_address(UseRemote))
                except ConnectionRefusedError as e:
                    raise RuntimeError(
                        "Connection Refused error in SendAPRS:\r\n'\
                    ' Address %s Port %d\n\r %s"
                        % GlobalDefinitions.Global.ServerAddress,
                        GlobalDefinitions.Global.APRSPort,
                        e,
                    ) from e
                except ConnectionError as e:
                    raise RuntimeError("Connection error in sendAPRS: %s'\n" % e) from e

                except TimeoutError as e:
                    do_print_server_address(UseRemote)
                    raise RuntimeError("Timeout error in sendAPRS: %s'\n" % e) from e

                except Exception as e:
                    raise RuntimeError(
                        "Unspecified Connection Error connecting to server in sendAPRS: '\r''\n %s '\n'\r"
                        % e
                    ) from e

                GlobalDefinitions.Global.NoConnect = (
                    False  # we now have valid connection
                )

                # count number frames sent this time
                period_frame_count = 0

                diagstr = "In TransmitAPRS Queue Count = {0}".format(len(ServerQueue))
                Do_diag_print(diagnostic2, diagstr)
                """if diagnostic2:
                    print("In TransmitAPRS Queue Count = {0}".format(len(ServerQueue)))
                """

                for de in ServerQueue:
                    if ServerQueue[de] != "string2":
                        tcpbytes = bytearray(
                            ServerQueue[de], "utf-8"
                        )  # convert the APRS string to bytes prior to TX

                        try:  # Attempt to send
                            diagstr = "would send tcp data", tcpbytes.decode()
                            Do_diag_print(diagnostic3, diagstr)
                            """if diagnostic3:
                                print("would send tcp data", tcpbytes.decode())
                            """

                            do_log_aprs(LogAPRS, APRSLogFile, tcpbytes)

                            aprs_stream.sendall(tcpbytes)
                            period_frame_count += 1

                        #  end try attempt to send
                        except Exception as e:
                            raise RuntimeError("Error writing APRS to Server", e) from e

                # have sent the block
                GlobalDefinitions.Global.LastTransmit = current
                # now clear the queued items
                ServerQueue.clear()
                # update stats

                StatsQ.put(
                    (
                        "Nr_APRS_permin",
                        int(
                            period_frame_count
                            * 60
                            / GlobalDefinitions.Global.ServerPeriod
                        ),
                    )
                )
                StatsQ.put(("Nr_APRS_TX", period_frame_count))

                # now tidy up - given that we aggregate dont need to leave socket permanently open
                aprs_stream.shutdown(SHUT_RDWR)
                aprs_stream.close()
                GlobalDefinitions.Global.NoConnect = True
        else:  # not ready to transmit yet
            # make sure we know where we arte with the socket
            try:  # I would assume this is going to fail everytime
                aprs_stream.shutdown(SHUT_RDWR)
                aprs_stream.close()
            except Exception:
                pass

            GlobalDefinitions.Global.NoConnect = True

    except Exception as e:
        raise RuntimeError("Error dequeinng in Transmit APRS \n %s", e) from e


def define_server_address(useremote: bool):
    if useremote:
        serveraddress = (
            GlobalDefinitions.Global.remoteEnd,
            int(GlobalDefinitions.Global.APRSPort),
        )
    else:
        serveraddress = (
            GlobalDefinitions.Global.ServerAddress,
            int(GlobalDefinitions.Global.APRSPort),
        )

    return serveraddress


def do_print_server_address(useremote: bool):
    if useremote:
        print(
            GlobalDefinitions.Global.remoteEnd,
            GlobalDefinitions.Global.APRSPort,
        )
    else:
        print(
            GlobalDefinitions.Global.ServerAddress,
            GlobalDefinitions.Global.APRSPort,
        )

    return None


def do_log_aprs(logaprs: bool, aprslogfile, tcpbytes):
    try:
        if logaprs:
            with open(aprslogfile, "a") as f:
                f.write(tcpbytes.decode())

    except Exception as e:
        raise RuntimeError("Exception while appending to logfile %s \n", e) from e
    return None


def main(self):
    pass


if __name__ == 'main':
    main()
