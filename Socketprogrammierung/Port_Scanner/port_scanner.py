from threading import Thread
import socket

# Lists
tcp_open = []
tcp_closed = []
tcp_werror60 = []
tcp_werror61 = []
udp_open = []
udp_werror40 = []
udp_werror54 = []
udp_closed = []

socket.setdefaulttimeout(10)

# Localhost
SERVER_IP = '141.37.168.26'


def tcp_echo(server_port):
    # Setup TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock_tcp.connect((SERVER_IP, server_port))
    except socket.error as e:
        if "[WinError 10060]" in str(e):
            tcp_werror60.append(server_port)
        elif "[WinError 10061]" in str(e):
            tcp_werror61.append(server_port)
        else:
            tcp_closed.append(server_port)
        return

    try:
        msg = sock_tcp.recv(1024).decode('utf-8')
        tcp_open.append((server_port, msg))
    except socket.error:
        tcp_open.append((server_port, ""))
    sock_tcp.close()


def udp_echo(server_port):
    # Setup UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.sendto(b"Hello", (SERVER_IP, server_port))
    try:
        data, addr = sock_udp.recvfrom(1024)
        udp_open.append((server_port, data[:-1].decode("utf-8")))
    except socket.error as e:
        if "[WinError 10040]" in str(e):
            udp_werror40.append(server_port)
        elif "[WinError 10054]" in str(e):
            udp_werror54.append(server_port)
        elif "timed out" in str(e):
            udp_closed.append(server_port)
        else:
            print("Unusual error detected!!", str(e))
    sock_udp.close()


threads = []
for i in range(1, 51):
    threads.append((Thread(target=tcp_echo, args=(i,)), Thread(target=udp_echo, args=(i,))))

for tcp, udp in threads:
    tcp.start()
    udp.start()

for tcp, udp in threads:
    tcp.join()
    udp.join()


print("+++ TCP +++")
print("Open:             {}".format(tcp_open))
print("Closed:           {}".format(tcp_closed))
print("[WinError 10060]: {}".format(tcp_werror60))
print("[WinError 10061]: {}".format(tcp_werror61))
print("+++ UDP +++")
print("Open:             {}".format(udp_open))
print("Closed:           {}".format(udp_closed))
print("[WinError 10040]: {}".format(udp_werror40))
print("[WinError 10054]: {}".format(udp_werror54))
