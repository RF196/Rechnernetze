import pickle
import socket
import sys
import threading
import time
import errno
import colorit

# Farben
GREY = '\033[37m'
BLUE = '\033[94m'
GREEN = '\033[92m'
BOLD = '\033[1m'
ENDC = '\033[0m'

from P2PChat.Client.Protocol import protocol_broadcast, protocol_stups, protocol_message, protocol_login

IP = '127.0.0.13'
START = 12607
REMSocket = None
MSG_SIZE = 8


class Client:

    def __init__(self):
        self.ip = IP  # str(socket.gethostbyname(socket.gethostname()))

        self.port_tcp_server = self.next_free_port()
        self.udp_port = self.next_free_port()

        self.sock_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock_tcp_server.bind((self.ip, self.port_tcp_server))
        self.sock_udp.bind((self.ip, self.udp_port))

        self.name = ''
        self.user_list = []
        self.connected = False

    def connect(self, name):
        try:
            self.name = name
            self.sock_tcp_server.connect(('127.0.0.1', 50000))
            user_info = pickle.dumps(protocol_login(name, IP, self.udp_port))
            self.sock_tcp_server.send(user_info)
            connect_response = self.sock_tcp_server.recv(4096)
            connect_response = pickle.loads(connect_response)
            print(connect_response['reply_text'])  # Ausgabetext
            self.user_list = connect_response['user_list']  # Hier geben wir dem User auch die User-Liste
            thread_tcp = threading.Thread(target=self.start_tcp)
            thread_udp = threading.Thread(target=self.start_udp)
            thread_udp.start()
            thread_tcp.start()

        except socket.error as e:
            print(e)

    def disconnect(self):
        self.port_tcp_server = self.next_free_port()
        self.sock_tcp_server.close()
        self.sock_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp_server.bind((self.ip, self.port_tcp_server))

    def start_udp(self):
        while True:
            try:
                data, addr = self.sock_udp.recvfrom(1024)
                thread = threading.Thread(target=self.handle_udp_request, args=(data, addr))
                thread.start()
            except socket.timeout:
                print('Socket timed out at', time.asctime())

    def start_tcp(self):
        global REMSocket
        self.port_tcp_chat_listen = self.next_free_port()
        sock_tcp_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp_chat.bind((self.ip, self.port_tcp_chat_listen))
        sock_tcp_chat.listen()
        while True:
            try:
                conn, addr = sock_tcp_chat.accept()
                REMSocket = conn
                thread = threading.Thread(target=self.handle_tcp_request, args=(conn,))
                thread.start()
            except socket.timeout:
                print('Socket timed out listening', time.asctime())

    def handle_udp_request(self, b_data, addr):
        while True:
            if not b_data:
                break
            data = pickle.loads(b_data)
            if data["operation"] == "stups":
                print(data["user_info"])
            elif data["operation"] == "broadcast":
                print(BLUE + str(data["from"]) + ENDC + " >> " + str(data["msg"]))
            elif data["operation"] == "add":
                self.user_list.append(data["user_info"])
                nick_name = data["user_info"]["nick_name"]
                print(BOLD + f"{nick_name} ist auf den Server gehüpft")
                for user in self.user_list:
                    if user["nick_name"] == self.name:
                        continue
                    print(GREY + user["nick_name"]+str(":") + GREEN + str("  ONLINE") + ENDC)
            elif data["operation"] == "del":
                self.user_list.remove(data["user_info"])
                nick_name = data["user_info"]["nick_name"]
                print(f"{nick_name} hat uns verlassen!")
            else:
                print(data)
            break

    def handle_tcp_request(self, conn):
        receive_task = threading.Thread(target=self.receive_task, args=(conn,))
        receive_task.start()
        receive_task.join()

    def start_chat(self, nick_name, port):
        addr = self.get_udp_addr_by_name(nick_name=nick_name)
        port_tcp_chat = self.next_free_port()
        sock_tcp_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp_chat.bind((self.ip, port_tcp_chat))
        if addr:
            try:
                sock_tcp_chat.connect((addr[0], int(port)))
                send_task = threading.Thread(target=self.send_task, args=(sock_tcp_chat,))
                recv_task = threading.Thread(target=self.receive_task, args=(sock_tcp_chat,))
                print("Die Unterhaltung beginnt")
                recv_task.start()
                send_task.start()
                send_task.join()
                recv_task.join()
            except socket.error as e:
                print(e)
        else:
            print("User ist nicht auf dem Server!")

    def receive_task(self, socket):
        b_full_msg = b''
        new_msg = True
        sock = socket
        while True:
            try:
                while True:
                    b_msg = sock.recv(16)
                    if new_msg:
                        _msg_size = int(b_msg[:MSG_SIZE])
                        new_msg = False
                    b_full_msg += b_msg
                    if len(b_full_msg) - MSG_SIZE == _msg_size:
                        msg = pickle.loads(b_full_msg[MSG_SIZE:])
                        if msg == "quit":
                            break
                        print(msg['user_info'])
                        new_msg = True
                        b_full_msg = b''
            except OSError as e:
                print("Die Unterhaltung wurde beendet!")
                break
        sock.close()

    def send_task(self, socket):
        sock = socket
        while True:
            try:
                msg = input()  # einlesen der nachricht
                if msg == "quit":
                    break
                b_msg = pickle.dumps(protocol_message(msg))           # verpacken der nachricht
                b_msg = f'{len(b_msg):<{MSG_SIZE}}'.encode() + b_msg  # Nachrichtengröße + Nachricht selber
                sock.send(b_msg)                                      # und ab die post
            except OSError as e:
                print("Die Unterhaltung ist beendet")
                break
        sock.close()

    def stups(self, nick_name):
        global REMSocket
        addr = self.get_udp_addr_by_name(nick_name=nick_name)
        stups_user = protocol_stups(self.name, self.port_tcp_chat_listen)
        if addr:
            self.sock_udp.sendto(pickle.dumps(stups_user), addr)
            print("Bitte warten Sie bis die Unterhaltung startet...")
            while True:
                if not REMSocket:
                    pass
                else:
                    send_task = threading.Thread(target=self.send_task, args=(REMSocket,))
                    print("Die Unterhaltung beginnt!")
                    send_task.start()
                    send_task.join()
                    break

        else:
            print("User ist nicht auf dem Server!")

    def broadcast(self):
        print("Du bist jetzt im Broadcast Mode - Deine Nachrichten richten sich an alle \n"
              "Gebe 'quit' ein um den Broadcast Mode zu verlassen")
        while True:
            try:
                msg = input()  # einlesen der nachricht
                if msg == "quit":
                    break
                b_msg = pickle.dumps(protocol_broadcast(msg, self.name))  # verpacken der nachricht
                self.sock_tcp_server.send(b_msg)  # und ab die post
            except OSError as e:
                print("Die Unterhaltung ist beendet")
                break
        print("Broadcast Mode beendet!")

    def next_free_port(self, port=START, max_port=65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind((IP, port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError('no free ports')

    def get_udp_addr_by_name(self, nick_name):
        for user in self.user_list:
            if user['nick_name'] == nick_name:
                return user['ip_address'], user['udp_port']
