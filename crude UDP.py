
from socket import socket, AF_INET, SOCK_DGRAM




address = ''
port = 4158
# initialise by establishing the socket
sock = socket(AF_INET, SOCK_DGRAM)

sock.bind((address, port) )
while True:
    msg, addr = sock.recvfrom(port)
    print (msg[1])
    if msg[1] != 65:
        print(msg, ' ', addr)