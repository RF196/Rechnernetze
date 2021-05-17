"""
Multiple Clients to one Server
"""
import socket
import struct
import threading
import time

socket.setdefaulttimeout(300)

PORT = 50000
SERVER = "127.0.0.1"  # oder socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


# Socket erstellen und an Adresse binden
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"Verbindung zu {addr} wurde aufgebaut")
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            response = calculate(msg)
            conn.send(str(response).encode())
        except socket.timeout:
            print('Socket timed out at', time.asctime())
    conn.close()


def calculate(request):
    l = int((len(request) - 12) / 4)
    var = struct.unpack(f'<I7sB{l}i', request)
    if var[1].startswith(b'summe'):
        return str(var[0]) + ": " + str(sum(var[3:]))
    elif var[1].startswith(b'produkt'):
        return str(var[0]) + ": " + str(mul(var[3:]))
    elif var[1].startswith(b'min'):
        return str(var[0]) + ": " + str(min(var[3:]))
    elif var[1].startswith(b'max'):
        return str(var[0]) + ": " + str(max(var[3:]))
    else:
        return "Operation nicht bekannt bitte 'summe'," \
               " 'produkt', 'minimum' oder 'maximum wählen"


def sum(numbers):
    sum = 0
    for n in numbers:
        sum += n
    return sum


def mul(numbers):
    product = 1
    for n in numbers:
        product *= n
    return product


def min(numbers):
    start = numbers[0]
    for n in numbers:
        if n < start:
            start = n
    return start


def max(numbers):
    start = numbers[0]
    for n in numbers:
        if n > start:
            start = n
    return start


def start():
    server.listen()
    print(f"[Listening] Server is listening on {server}")
    while True:
        try:
            conn, addr = server.accept()  # Blockt und wartet auf neue Connections
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()  # Jedes mal wenn eine Connection accepted wird,
            # wird für diese Connection ein Thread gestartet. (handle_client)
        except socket.timeout:
            print('Socket timed out listening', time.asctime())


print("Server ist gestartet...")
start()
server.close()
