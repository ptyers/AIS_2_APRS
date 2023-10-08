from socket import socket, AF_INET, SOCK_DGRAM
import MyPreConfigs
from GlobalDefinitions import Global
import time


class ReadAISFile:
    FileName = MyPreConfigs.AISFileName

    def __init__(self, FileName):
        # open data file for reading
        try:
            f = open(FileName, "r")
        except Exception as e:
            raise RuntimeError("Error opening ", FileName, " for reading", e) from e
        pass

    def GetFileData(self):
        diagnostic = MyPreConfigs.diagnostic
        diagnostic2 = MyPreConfigs.diagnostic2
        diagnostic3 = MyPreConfigs.diagnostic3
        LogIncomming = MyPreConfigs.LogIncoming
        FileName = MyPreConfigs.AISFileName
        f = open(FileName, "r")
        try:
            while True:
                try:

                    if diagnostic3:
                        print("Getting Data")
                        #  Blocks until a message returns on this socket from a remote host.
                        pass
                    receiveBytes = f.readline()
                    # print(receiveBytes)
                    time.sleep(0.1)

                    # print('Bytesreceive = ' , receiveBytes)

                    if diagnostic3:
                        print("Got data")
                        pass
                        # print(receiveBytes[0],str(receiveBytes[0]))
                    try:
                        # print('receive bytes 0 = ',receiveBytes[0], ord(receiveBytes[0]),type(receiveBytes))
                        if receiveBytes[0] == "!":
                            returnData = receiveBytes
                            # print(returnData)
                            # print('status queue = full ',bool(Global.inputqueue.full()))
                            if not Global.inputqueue.full():
                                # print('sending data', returnData)
                                Global.inputqueue.put(returnData)

                            else:
                                # dump record
                                pass

                        else:
                            # dump data
                            pass

                    except:
                        print("oops")
                        pass
                except Exception as e:
                    raise RuntimeError("Exception in ReadAISFile", e) from e
        except Exception as e:
            #  Last gasp attempt to catch thread failure
            raise RuntimeError("Thread getting AISFile data failed", e) from e

        # Exceptionstring = ExceptionExtension.ToFullDisplayString(e)
        # print(Exceptionstring)
