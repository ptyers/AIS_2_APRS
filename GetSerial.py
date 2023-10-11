"""
Currently a stub
If invoked will collect serial data from serial port defined in MyPreConfigs
Speed will also be defined in that module
Parameters may be set in ini file to override defaults
A boolean in MyPreConfigs determines if the module is invoked

"""

from GlobalDefinitions import Global
import serial
from datetime import datetime


class GetSerial:
    def __init__(self, ComPort: str, Speed: int):
        # at the moment nothing happens except defining the queue used to communicate with the AIS processing section
        outqueue = Global.inputqueue

    def cleanup(self):
        pass


    def GetSerial(self):
        # reads data from a previously recorded file iof AIS input;
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        LogIncomming = Global.LogIncoming

        StatsQ = Global.Statsqueue

        current_time = datetime.now()
        current_input_frames = 0
        current_dropped = 0

        ser = serial.Serial(
            "COM2",
            38400,
            timeout=0,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        ser.open()

        _keepgoing = True

        if diagnostic:
            print(" into get Serial data")

        # now start getting tha data - preprocessed then sent on to the Main program via queue

        while _keepgoing:
            try:
                if diagnostic3:
                    print("Getting Data")
                    #  Blocks until a message returns on this socket from a remote host.
                    pass

                try:

                    stringer = ser.readline().decode("utf-8")

                except Exception as e:
                    raise RuntimeError("Error getting data from serial", e) from e

                if diagnostic3:
                    if len(stringer) > 0:
                        print(
                            " input item from serial = ",
                            stringer[0: len(stringer) - 1],
                        )

                if len(stringer) > 0 and ord(stringer[0]) == 33:
                    # got a record stating with an "!"

                    if diagnostic3:
                        print("Got data")
                        pass

                    if LogIncomming or diagnostic3:
                        # print("returnData = ", returnData[0:returnData.find('\r')])
                        f = open("AISdatastream.txt", "a")
                        f.write("%s" % stringer[0: stringer.find("\r") + 1])
                        f.close()

                    if Global.inputqueue.full():
                        raise RuntimeError("Queue is full")

                    if diagnostic3:
                        print("Global Input Queue status = ", Global.inputqueue.full())

                    if not Global.inputqueue.full():
                        try:
                            if diagnostic3:
                                print("Putting Data into queue", stringer)
                                pass
                            Global.inputqueue.put(stringer)
                        except Exception as e:
                            raise RuntimeError("error putting item on queue", e) from e

                    # now throttle this back a bit so we dont choke the main program

                    else:
                        # dump record n- non valid
                        current_dropped += 1
                else:
                    # dump data - nowhere for it to go
                    current_dropped += 1

                # check if we need stop
                _keepgoing = Global._keepgoing

            except KeyboardInterrupt as e:
                ser.close()
                raise KeyboardInterrupt from e

            except Exception as e:
                raise RuntimeError("Exception in Get Serial Data", e) from e

            delta = (datetime.now() - current_time).total_seconds()
            if delta > 60:
                if not StatsQ.full():
                    try:
                        StatsQ.put(
                            "Nr_Serial_Frames_permin", current_input_frames * 60 / delta
                        )
                        StatsQ.put("Nr_Serial_Frames_RX", current_input_frames)
                        StatsQ.put("Nr_Serial_Frames_Dropped", current_dropped)
                    except:
                        pass  # presumably failed because queue full

                current_time = datetime.now()
                current_input_frames = 0
                current_dropped = 0

    pass


def main(self):
    pass


if __name__ == 'main':
    main()
