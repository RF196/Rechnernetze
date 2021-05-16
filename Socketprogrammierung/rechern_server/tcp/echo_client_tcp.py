import socket
from functools import partial

from Socketprogrammierung.rechern_server.operations import send_operation

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))

sendTo = partial(send_operation, send=sock.send, receive=sock.recv)

sendTo(1, b"Summe", (1, 2))
sendTo(2, b"Produkt", (1, 2, 3))
sendTo(3, b"Minimum", (5, 20, 14))
sendTo(4, b"Maximum", (2, 1, 4))

sock.close()
