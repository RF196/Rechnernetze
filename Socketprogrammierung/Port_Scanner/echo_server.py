import socket
import time
from threading import Thread

MY_IP = '127.0.0.1'
tcp_port = 10
udp_port = 7

server_activity_period = 30


def udp_echo():
    # Setup UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.settimeout(10)
    sock_udp.bind((MY_IP, udp_port))
    print("Listening on Port", udp_port, "for incoming UDP connections")
    sock_udp.settimeout(10)
    t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

    while time.time() < t_end:
        try:
            data, addr = sock_udp.recvfrom(1024)
            print('received message: ' + data.decode('utf-8') + ' from ', addr)
            sock_udp.sendto(data[::-1], addr)
        except socket.timeout:
            print('Socket timed out at', time.asctime())

    sock_udp.close()


def tcp_echo():
    # Setup TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.settimeout(10)
    sock_tcp.bind((MY_IP, tcp_port))
    print('Listening on Port ', tcp_port, ' for incoming TCP connections')

    t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode
    sock_tcp.listen(1)

    while time.time() < t_end:
        try:
            conn, addr = sock_tcp.accept()
            print('Incoming connection accepted: ', addr)
            break
        except socket.timeout:
            print('Socket timed out listening', time.asctime())

    while time.time() < t_end:
        try:
            data = conn.recv(1024)
            if not data:  # receiving empty messages means that the socket other side closed the socket
                print('Connection closed from other side')
                print('Closing ...');
                conn.close()
                break
            print('received message: ', data.decode('utf-8'), 'from ', addr)
            conn.send(data[::-1])
        except socket.timeout:
            print('Socket timed out at', time.asctime())

    sock_tcp.close()
    if conn:
        conn.close()


t1 = Thread(target=udp_echo)
t2 = Thread(target=tcp_echo)

t1.start()
t2.start()
