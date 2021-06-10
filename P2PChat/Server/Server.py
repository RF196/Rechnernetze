import pickle
import socket
import threading
import socket
import struct
from P2PChat.Server.Protocol import del_user, protocol_broadcast


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


IP = get_ip_address()


class Server:
    def __init__(self):
        self.user_list = []
        self.ip = IP
        self.tcp_port = 1400
        self.udp_port = 1401
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_tcp.bind((self.ip, self.tcp_port))
        self.sock_udp.bind((self.ip, self.udp_port))

    def handle_client(self, conn, addr):
        print(f"Verbindung zu {addr} wurde aufgebaut")
        while True:
            try:
                b_msg: bytes = conn.recv(4096)
                if not b_msg:
                    break
                user_info = pickle.loads(b_msg)  # Entpacke Message
                if user_info["operation"] == "broadcast":
                    self.broadcast(protocol_broadcast(user_info["msg"], user_info["from"]), addr)
                else:
                    nick_name = user_info["nick_name"]  # Entpacke Nick-Name

                    reply = self.reply(name=nick_name)  # Erstelle Antwort (als Dict)
                    b_reply = pickle.dumps(reply)  # Verpacke Antwort
                    conn.send(b_reply)  # Versende Antwort + User-Liste an User
                    self.add_user_to_list(user_info)  # Füge User zur aktuellen User-Liste hinzu + Benachrichtigung
            except socket.error as e:
                print(e)
                break
        print(f"verbindung zu {addr} geschlossen")
        self.remove_user_from_list(addr)
        conn.close()

    def start(self):
        self.sock_tcp.listen()

        print(f"[Listening] Server is listening on {self.sock_tcp}")
        while True:
            try:
                conn, addr = self.sock_tcp.accept()  # Blockt und wartet auf neue Connections
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()  # Jedes mal wenn eine Connection accepted wird,
                # wird für diese Connection ein Thread gestartet. (handle_client)

            except socket.timeout as e:
                print(e)

    def reply(self, name):
        """
        Text-Ausgabe die erscheint, sobald jemand eingeloggt ist.
        Zusätzlich wird die aktuelle User-Liste mitgeschickt.
        :param name: Nick-Name
        :return: Antwort + User Liste als Dictionary "Json"
        """
        reply = {
            "reply_text": f"Hallo {name}!\nHerzlich Willkommen im HTWG Chat \n"
                          f"Du kannst nun mit folgende Personen chatten: \n"
                          f"{self.get_names()} \n"
                          f"Um mit einer Person chatten zu können, musst du diese zuerst \n"
                          f"anstupsen. Daraufhin kann die Person den Kontakt zu dir aufbauen. \n"
                          f"stups <name>          : Person anstupsen \n"
                          f"broadcast             : Nachricht an alle (Broadcast Mode) \n"
                          f"disconnect            : Abmelden",
            "user_list": self.user_list
        }
        return reply

    def get_names(self):
        """
        Extrahiert die Nicknamen aus der JSON User Info
        :return: Liste aller Nick-Namen die sich auf dem Server befinden
        """
        names = []
        for user in self.user_list:
            names.append(user['nick_name'])
        return names

    def remove_user_from_list(self, addr):
        for user_info in self.user_list:
            nick_name = user_info["nick_name"]
            ip_address = user_info["ip_address"]
            udp_port = user_info["udp_port"]
            user_addr = (ip_address, udp_port)
            if addr[0] == user_addr[0]:
                self.user_list.remove(user_info)
                print(nick_name + " hat uns verlassen.")
                self.leave_notification(user_info=user_info)

    def add_user_to_list(self, user_info):
        self.user_list.append(user_info)
        self.entry_notification(user_info=user_info)

    def next_free_port(self, port=15800, max_port=65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('127.0.0.1', port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError('no free ports')

    def leave_notification(self, user_info):
        from P2PChat.Server.Protocol import del_user
        """
        Benachrichtigt alle User dass jemand den Chat-Server verlassen hat
        :param nick_name:
        :return: (void)
        """
        if self.user_list:
            del_user = del_user(user_info=user_info)
            b_del_user = pickle.dumps(del_user)
            for user in self.user_list:
                ip_address = user["ip_address"]
                udp_port = user["udp_port"]
                self.sock_udp.sendto(b_del_user, (ip_address, udp_port))

    def entry_notification(self, user_info):
        from P2PChat.Server.Protocol import add_user
        """
        Benachrichtigt alle User dass jemand dem Chat-Server beigetreten ist
        :param user_info: 
        :return: (void)
        """
        add_user = add_user(user_info=user_info)
        b_add_user = pickle.dumps(add_user)
        if self.user_list:
            for user in self.user_list:
                ip_address = user["ip_address"]
                udp_port = user["udp_port"]
                self.sock_udp.sendto(b_add_user, (ip_address, udp_port))

    def broadcast(self, msg, addr):
        b_msg = pickle.dumps(msg)
        if self.user_list:
            for user in self.user_list:
                if user["ip_address"] == addr[0]:
                    continue
                ip_address = user["ip_address"]
                udp_port = user["udp_port"]
                self.sock_udp.sendto(b_msg, (ip_address, udp_port))


Server().start()
