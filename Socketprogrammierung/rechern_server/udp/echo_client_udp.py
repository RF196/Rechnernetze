from Socketprogrammierung.rechern_server.operations import send_operation
import socket
from functools import partial

Server_IP = '127.0.0.1'
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(10)


def send_to_def(data, address):
    sock.sendto(data, address)


def receive_def(bufsize):
    d, a = sock.recvfrom(bufsize)
    return d


sendtoPartial = partial(send_to_def, address=(Server_IP, Server_PORT))
send_to = partial(send_operation, send=sendtoPartial, receive=receive_def)

send_to(1, b"Summe", (1, 2))
send_to(2, b"Produkt", (1, 2, 3))
send_to(3, b"Minimum", (5, 20, 14))
send_to(4, b"Maximum", (2, 1, 4))

sock.close()
