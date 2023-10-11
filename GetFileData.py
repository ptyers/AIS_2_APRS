import GlobalDefinitions
import AISData
from GlobalDefinitions import Global
import time


class FileData:
    def __init__(self):
        try:
            self.f = open("AISdatastream.txt", "r")
        except Exception as e:
            raise RuntimeError("couldn't open data file " + Global.AISFileName) from e

    def ReadAISFile(self):
        # reads data from a previously recorded file iof AIS input;
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3

        # parameter to allow remote stopping of file read
        _keepgoing = True

        if diagnostic:
            print(" into get File data")

        # now start getting tha data - preprocessed then sent on to the Main program via queue

        while _keepgoing:
            try:
                if diagnostic3:
                    print("Getting Data")
                    #  Blocks until a message returns on this socket from a remote host.
                    pass

                try:
                    time.sleep(0.1)
                    stringer = self.f.readline()

                except Exception as e:
                    raise RuntimeError("Error getting data from file", e) from e

                if diagnostic3:
                    if len(stringer) > 0:
                        print(
                            " input item from file = ", stringer[0: len(stringer) - 1]
                        )

                if len(stringer) > 0 and ord(stringer[0]) == 33:
                    # got a record stating with an "!"

                    if diagnostic3:
                        print("Got data")
                        pass
                    if Global.inputqueue.full():
                        raise RuntimeError

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
                        # dump record
                        pass
                else:
                    # dump data
                    pass

                # check if we need stop
                _keepgoing = Global._keepgoing
            except Exception as e:
                raise RuntimeError("Exception in Get File Data", e)


def main(self):
    pass


if __name__ == 'main':
    main()
