import sys
from socket import socket, AF_INET, SOCK_DGRAM
import GlobalDefinitions
from GlobalDefinitions import Global
from datetime import datetime


class GetDataUDP:
    sock = socket(AF_INET, SOCK_DGRAM)

    def __init__(self, address: str, udpport: int):

        # initialise by establishing the socket
        self.sock.bind((address, udpport))
        self._logincoming = Global.LogIncoming
        pass

    def set_Port(self, value):
        if isinstance(value, int):
            self._Port = value
        else:
            raise (ValueError, "In GetUDP Port must be integer")

    def get_Port(self) -> int:
        return self._Port

    Port = property(get_Port, set_Port)

    def set_StartStop(self, value):
        if isinstance(value, bool):
            self._keepgoing = value
        else:
            raise (ValueError, "In GetUDP StartStop must be bool")

    def get_StartStop(self):
        return self._keepgoing

    StartStop = property(get_StartStop, set_StartStop)

    _remoteend = ""
    _Port = 4158
    _keepgoing = True
    _logincoming = False

    def GetUDPData(self):
        diagnostic = Global.diagnostic
        diagnostic2 = Global.diagnostic2
        diagnostic3 = Global.diagnostic3
        diagnostic_Level = Global.diagnostic_Level

        UDP_Received_IP_Addresses = Global.UDP_Received_IP_Addresses
        StatsQ = Global.Statsqueue

        current_time = datetime.now()  # used for calculation of statistics
        current_input_frames = 0
        current_dropped = 0

        try:
            if diagnostic or diagnostic2:
                #  for Global.diagnostic purpose want to capture the input stream
                # StreamWriter writer = new StreamWriter(MyPreConfigs.WorkingDir + "InputStream.txt", True)
                # writer.AutoFlush = True
                if diagnostic3:
                    print(
                        "Ëntering GetData Thread {0} {1}\n", self._Port, self._remoteend
                    )
                    pass

            # Creates an IPEndPoint to record the IP Address and port number of the sender.
            #  The IPEndPoint will allow you to read datagrams sent from any source.
            # UdpClient receivingUdpClient = new UdpClient(_Port)
            # IPEndPoint RemoteIpEndPoint = new IPEndPoint(IPAddress.Any, _Port)

            while self._keepgoing:
                if GlobalDefinitions.Global.CloseDown:
                    self._keepgoing = False
                try:

                    if diagnostic3:
                        print("Getting Data")
                        #  Blocks until a message returns on this socket from a remote host.
                        pass
                    receiveBytes, addr = self.sock.recvfrom(4158)
                    if not (addr[0] == "121.214.34.47" or receiveBytes[0] == 10):
                        current_input_frames += 1

                    if (
                            addr[0] not in UDP_Received_IP_Addresses
                    ):  # whether this gets used is uncertain
                        UDP_Received_IP_Addresses[addr[0]] = 1
                        if diagnostic3:
                            print(" adding ", addr, " to list of received addresses")
                    else:
                        UDP_Received_IP_Addresses[addr[0]] += 1

                    # print('Bytesreceive = ' , receiveBytes)

                    if diagnostic3:
                        print("Got data")
                        pass
                    # print(receiveBytes[0],str(receiveBytes[0]))
                    if receiveBytes[0] == 33:
                        try:
                            returnData = receiveBytes.decode()
                            dumpit = False
                        except:
                            print("Invalid utf-8", receiveBytes[0], receiveBytes)
                            dumpit = True
                        if self._logincoming or diagnostic3:
                            # print("returnData = ", returnData[0:returnData.find('\r')])
                            f = open("AISdatastream.txt", "a")
                            f.write("%s" % returnData[0: returnData.find("\r") + 1])
                            f.close()
                        if addr[0] == "60.231.221.5":
                            dumpit = True

                        if not Global.inputqueue.full() and not dumpit:
                            Global.inputqueue.put(
                                returnData[0: returnData.find("\r") + 1]
                            )
                        else:
                            # dump record - nowhere for it to go
                            current_dropped += 1
                    else:
                        # dump data
                        # not a valid frame

                        if not (addr[0] != "121.214.34.47" or receiveBytes[0] != 10):
                            print(addr[0], receiveBytes[0], receiveBytes)
                            current_dropped += 1
                except Exception as e:
                    raise RuntimeError("Exception in UDPGetData", e) from e
                delta = (datetime.now() - current_time).total_seconds()
                if delta > 60:
                    if not StatsQ.full():
                        try:
                            framespm = int(current_input_frames * 60 / delta)
                            StatsQ.put(("Nr_UDP_Frames_permin", framespm))
                            StatsQ.put(("Nr_UDP_Frames_RX", current_input_frames))
                            StatsQ.put(("Nr_UDP_Frames_Dropped", current_dropped))
                        except:
                            pass  # presumably failed because queue full

                    current_time = datetime.now()
                    current_input_frames = 0
                    current_dropped = 0
            # close out thread

        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            #  Last gasp attempt to catch thread failure
            raise RuntimeError("Thread getting UDP data failed", e) from e

        # Exceptionstring = ExceptionExtension.ToFullDisplayString(e)
        # print(Exceptionstring)


def main(self):
    pass


if __name__ == 'main':
    main()
