import socket
import time

from Socketprogrammierung.rechern_server.operations import process_request

My_IP = "127.0.0.1"
My_PORT = 50000
server_activity_period = 30  # Zeit, wie lange der Server aktiv sein soll

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((My_IP, My_PORT))

sock.settimeout(10)
t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

while time.time() < t_end:
    try:
        data, addr = sock.recvfrom(1024)
        print('received message: from ', addr)
        print(data)
        result = process_request(data)
        sock.sendto(result, addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock.close()
