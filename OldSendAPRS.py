import MyPreConfigs
import GlobalDefinitions
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from APRS import APRS


# region SendAPRS
def SendAPRS(p, mydata, kill: bool, Bulletin: int):
    diagnostic = GlobalDefinitions.Global.diagnostic
    diagnostic2 = GlobalDefinitions.Global.diagnostic2
    diagnostic3 = GlobalDefinitions.Global.diagnostic3
    diagnostic3 = False

    #  takes analysed AIS stream and at periodic intervals sends to APRS server
    tcpbytes = bytearray("", "utf-8")
    try:
        myaprs = APRS(
            mydata.String_MMSI,
            mydata.Latitude,
            mydata.Longitude,
            mydata.COG,
            mydata.SOG,
            mydata.Name,
            mydata.isAVCGA,
        )

        myaprs.MMSI = mydata.String_MMSI
        if len(mydata.Callsign) > 0:
            myaprs.Callsign = mydata.Callsign

    except Exception as e:
        raise RuntimeError("Error creating myaprs in SendAPRS", e) from e

    if p < 4 or p == 9 or p == 18:  # types 1,2 , 3, 9 and 18 position reports
        #            if ((mydata.Latitude < 91) && (mydata.Longitude < 181))  #  only send valid lat/long to server
        try:
            if diagnostic3 and len(mydata.Callsign) > 0:
                print("ín SendAPRS mydata.Callsign = ", mydata.Callsign)
            if mydata.Callsign == "":
                XCallsign = mydata.String_MMSI
            else:
                XCallsign = mydata.Name
                myaprs.Name = mydata.Name
                # send a kill for MMSI version
                tcpbytes = bytearray(myaprs.CreateObjectPosition(True, mydata), "utf-8")
                QueueAPRS(mydata.String_MMSI, tcpbytes)

            tcpbytes = bytearray(myaprs.CreateObjectPosition(kill, mydata), "utf-8")

            #  now queue the aprs stream
            QueueAPRS(XCallsign, tcpbytes)
            TransmitAPRS(tcpbytes)
            del myaprs

        except Exception as e:
            raise RuntimeError(
                "Exception while processing (queue) Type 1, 2 , 3 or 9", e
            ) from e

    else:
        try:
            # switch (p)
            # switch statements not available simulate with dictionary of things to do
            thisswitch = {
                1: donothing,
                2: donothing,
                3: donothing,
                4: do4,
                5: do5_24,
                6: donothing,
                7: donothing,
                8: donothing,
                9: donothing,
                10: donothing,
                11: donothing,
                12: donothing,
                13: donothing,
                14: donothing,
                15: donothing,
                16: donothing,
                17: donothing,
                18: donothing,
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
            if p == 14:
                tcpbytes = domyswitch(p, myaprs, Bulletin, thisswitch)
            elif p == 5 or p == 24:
                tcpbytes = domyswitch(p, (mydata, myaprs), kill, thisswitch)

            else:
                tcpbytes = domyswitch(p, myaprs, kill, thisswitch)

            if mydata.Callsign == "":
                XCallsign = mydata.String_MMSI
            else:
                XCallsign = mydata.Callsign

            QueueAPRS(XCallsign, tcpbytes)

            # finished with myaors dispose of it
            del myaprs

        except Exception as e:
            print("Error Attempting to queue 4 5 24")
            raise RuntimeError(
                "Exception while processing (queue) Type 4,5 or 24", e
            ) from e

        try:
            TransmitAPRS(tcpbytes)
        except Exception as e:
            raise RuntimeError(
                "Error Attempting to Transmit APRS following queuing", e
            ) from e


def domyswitch(p, args, secondarg, switchdic):
    # replaces a switch uses switchdict to determine which function to execute
    # with arguments payload and aisobject
    if p in switchdic:
        return switchdic[p](args, secondarg)
    else:
        raise ValueError("Function to handle payload_ID unknown")
    pass


def donothing():
    pass


def do4(args, dummy: bool):
    # print(myaprs.CreateObjectPosition())
    tcpbytes = bytearray(args.CreateBasePosition(), " utf-8")
    #                   print("sending tcp data")\ #  now queue the aprs stream
    return tcpbytes


def do14(args, Bulletin: int):
    tcpbytes = bytearray(args.CreateSafetyMessage(Bulletin), "utf-8")
    # print("sending tcp data")
    return tcpbytes


def do5_24(args, kill: bool):
    # APRS myaprs = new APRS(mydata.String_MMSI, mydata.Latitude, mydata.Longitude, mydata.COG, mydata.SOG, "")
    args1, args2 = args
    args2.Course = str(args1.COG)
    args2.Speed = str(args1.SOG)

    #                   print(myaprs.CreateObjectPosition())
    tcpbytes = bytearray(args2.CreateObjectPosition(kill, args1), "utf-8")
    #                   print("sending tcp data")
    return tcpbytes


def QueueAPRS(Callsign: str, tcpbytes):
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
            except KeyError as e:
                pass

                if diagnostic2:
                    print("In QueueAPRS Queue Count = {}".format(len(ServerQueue)))
                    for xx in ServerQueue:
                        print("MMSI {} Data {} ".format(xx, ServerQueue[xx]))

                #  otherwqise do nothing its a duplicate

        else:
            #  Create an entry in queue
            if diagnostic2:
                print("adding record to QueueAPRS ", Callsign, " : ", aprsstring)
            ServerQueue.update({Callsign: aprsstring})

            if diagnostic2:
                print("In QueueAPRS Queue NewEntry Count = {}".format(len(ServerQueue)))

    except Exception as e:
        print("Error while queuing APRS")
        raise RuntimeError("Error in Queue APRS\r\n", e)


def TransmitAPRS(tcpstream):
    diagnostic = GlobalDefinitions.Global.diagnostic
    diagnostic2 = GlobalDefinitions.Global.diagnostic2
    diagnostic3 = GlobalDefinitions.Global.diagnostic3
    LastTransmit = GlobalDefinitions.Global.LastTransmit
    ServerQueue = GlobalDefinitions.Global.ServerQueue
    NoConnect = GlobalDefinitions.Global.NoConnect

    # first check if socket exists
    if not GlobalDefinitions.Global.APRS_Socket_Status:  # stream not previosdly set up
        try:
            aprs_stream = socket(AF_INET, SOCK_STREAM)
        except OSError as e:
            raise RuntimeError("Error creating socket in sendAPRS: %s" % e)

        # Second try-except block -- connect to given host/port
        try:
            serveraddress = (
                GlobalDefinitions.Global.ServerAddress,
                int(GlobalDefinitions.Global.APRSPort),
            )
            aprs_stream.connect(serveraddress)
        except ConnectionRefusedError as e:
            print(
                "Connection Refused error in SendAPRS:\r\n Address %s Port %d\n\r %s"
                % GlobalDefinitions.Global.ServerAddress,
                GlobalDefinitions.Global.APRSPort,
                e,
            )
        except ConnectionError as e:
            print("Connection error in sendAPRS: %s" % e)

        except Exception as e:
            print("Address-related error connecting to server in sendAPRS: %s" % e)

        GlobalDefinitions.Global.APRS_Socket_Status = True

    #  need an array of bytes to pass to the send stream
    tcpbytes = bytearray("", "utf-8")

    #  having queued APRS stream now we see if it should be sent
    #  compare current time with LastTransmit time
    current = datetime.now()
    difference = current - GlobalDefinitions.Global.LastTransmit
    if diagnostic3:
        print("tx timedifference ", difference.total_seconds())

    if difference.total_seconds() > GlobalDefinitions.Global.ServerPeriod:
        """
        writer = StreamWriter( GlobalDefinitions.Global.WorkingDir + "Aprsstream.txt", true)
        writer.AutoFlush = true
        """
        # first check if socket exists

        try:
            aprs_stream = socket(AF_INET, SOCK_STREAM)
        except OSError as e:
            raise RuntimeError("Error creating socket in sendAPRS: %s" % e)

        # Second try-except block -- connect to given host/port
        try:
            serveraddress = (
                GlobalDefinitions.Global.ServerAddress,
                int(GlobalDefinitions.Global.APRSPort),
            )
            aprs_stream.connect(serveraddress)
        except ConnectionRefusedError as e:
            raise RuntimeError(
                "Connection Refused error in SendAPRS:\r\n Address %s Port %d\n\r %s"
                % GlobalDefinitions.Global.ServerAddress,
                GlobalDefinitions.Global.APRSPort,
                e,
            ) from e
        except ConnectionError as e:
            raise RuntimeError("Connection error in sendAPRS: %s" % e) from e

        except Exception as e:
            raise RuntimeError(
                "Address-related error connecting to server in sendAPRS: %s" % e
            ) from e

        GlobalDefinitions.Global.APRS_Socket_Status = True

        if diagnostic2:
            print("In TransmitAPRS Queue Count = {0}".format(len(ServerQueue)))

        for de in ServerQueue:
            if ServerQueue[de] != "string2":
                tcpbytes = bytearray(
                    ServerQueue[de], "utf-8"
                )  # convert the APRS string to bytes prior to TX

            try:  # Attempt to send
                print("would send tcp data", tcpbytes.decode())
                aprs_stream.sendall(tcpbytes)
                GlobalDefinitions.Global.LastTransmit = datetime.now()

            #  end try attempt to send
            except Exception as e:
                print("Error writing APRS to Server")
                raise RuntimeError("Error in Queue APRS", e) from e

        GlobalDefinitions.Global.APRS_Socket_Status = False

        try:  # flush queue and reset last transmit time
            if not NoConnect:
                ServerQueue.clear()
                LastTransmit = datetime.now()

        except Exception as e:
            print("Error dequeuing in Transmit APRS")
            raise RuntimeError("Error dequeinng in Transmit APRS", e) from e

        GlobalDefinitions.Global.APRS_Socket_Status = False


def main(self):
    pass


if __name__ == 'main':
    main()
