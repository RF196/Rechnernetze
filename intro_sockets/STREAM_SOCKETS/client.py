import socket
import struct
import time

socket.setdefaulttimeout(30)

IP = '127.0.0.1'
PORT = 50000
ADDRESS = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    while True:
        try:
            client.send(msg)
            print(client.recv(2048).decode())
            print("Für weitere Rechnungen einfach Enter klicken.")
            print("Zum beenden 'end' eingeben.")
            if input() == 'end':
                break
            create_message()
        except socket.timeout:
            print('Socket timed out at', time.asctime())
    client.close()


user_communication = ["Geben Sie eine Gewünschte ID an : ",
                      "Geben Sie nun eine von den gegebenen Operationen an"
                      " 'summe' 'produkt' 'min' 'max'",
                      "Geben Sie nun beliebig viele Zahlen ein und beenden Sie ihre Eingabe mit 'end':"]


def create_message():
    input_list = []
    while True:
        if len(input_list) < 3:                         # Nachdem ID und Operation abgefragt wurde,
            print(user_communication[len(input_list)])  # nur noch einmal wegen Zahlen fragen
        var = input()                                   # Eingabe entgegennehmen
        if var == 'end':
            input_list.insert(2, len(input_list[2:]))   # Wenn Eingabe fertig, anzahl von Zahlen noch in Liste einfügen
            break                                       # und rausspringen.
        if len(input_list) == 1:                        # An zweiter Stelle summe etc. als bytecode umwandeln
            input_list.append(var.encode())
        else:
            input_list.append(int(var))                 # Alles andere sind Zahlen

    le = input_list[2]

    var = struct.pack(f'<I7sB{le}i', *input_list)
    send(var)


create_message()
