import socket
import threading

socket.setdefaulttimeout(10)
server = '127.0.0.1'
open_tcp_ports = []
closed_tcp_ports = []
open_udp_ports = []
closed_udp_ports = []


def scan_udp(start, stop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for port in range(start, stop):
        sock.sendto("Hallo".encode(), (server, port))
        try:
            data, addr = sock.recvfrom(1024)
            print(data, addr)
            open_udp_ports.append(port)
        except socket.error:
            closed_udp_ports.append(port)
            pass


def scan_tcp(start, stop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(start, stop):
        try:
            sock.connect((server, port))
            print(server, port)
            open_tcp_ports.append(port)
        except socket.error:
            closed_tcp_ports.append(port)
            print(f"{port}  ist geschlossen")
            pass


threads = []
for i in range(1, 51, 5):
    thread_tcp = threading.Thread(target=scan_tcp, args=(i, i + 5))
    thread_udp = threading.Thread(target=scan_udp, args=(i, i + 5))
    threads.append(thread_tcp)
    threads.append(thread_udp)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Offene TCP Ports :" + str(open_tcp_ports))
print("Geschlossene TCP Ports: " + str(closed_tcp_ports))
print("Offene UDP Ports :" + str(open_udp_ports))
print("Geschlossene UDP Ports: " + str(closed_udp_ports))
