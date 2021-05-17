import socket
import struct
import threading
import time

socket.setdefaulttimeout(300)

PORT = 50500
SERVER = "127.0.0.1"  # oder socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


# Socket erstellen und an Adresse binden
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)


def handle_client(data, addr):
    print(f"Verbindung zu {addr} wurde aufgebaut!")
    while True:
        if not data:
            break
        response = calculate(data)
        server.sendto(str(response).encode(), addr)
        break


def calculate(request):
    l = int((len(request) - 12) / 4)
    var = struct.unpack(f'<I7sB{l}i', request)
    print(var)
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
    while True:
        try:
            data, addr = server.recvfrom(1024)
            thread = threading.Thread(target=handle_client, args=(data, addr))
            thread.start()
        except socket.timeout:
            print('Socket timed out at',time.asctime())


print("Server ist gestartet...")
start()
server.close()
