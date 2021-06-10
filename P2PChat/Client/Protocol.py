"""
Bei den folgenden Methoden handelt es sich dabei
WIE verschicke ich meine Nachrichten
Dabei wird eine Nachricht als Dictionary-Format (möchtegern JSON) versendet
Vorgehensweise Beispiel: Anmelden von Markus

    TUI: connect markus

    login_dict = protocol_login(markus, <IP>, <UDP_Port>)

    Um Ganze Objekte oder Strukturen gemütlich als Byte-Format zu
    ver- und entpacken nutzen wir die Bibliothek 'pickle'

    >> byte_login_dict = pickle.dumps(login_dict)
    >> ... conn.send(byte_login_dict)
    ______________________________________________________________
    Gegenseite: Server
    Damit der Server jetzt als Gegenseite weiss was für eine
    Nachricht er bekommt, entpackt er zunächst das Dict-Objekt

    >> ... byte_msg = conn.recv(1024)
       ... msg = pickle.loads(byte_msg)

    Dann schaut er in die Operation um welche es sich handelt.

    operation = msg["operation"]
        if operation == login ?
    >> Weiterverarbeitung für eine Anmeldung

    So haben die Dict Objekte immer den Key 'operation'
    und je nachdem was drinsteht, weiss der Server oder Chat Peer was
    mit der Nachricht zu tun ist.
"""


def protocol_login(name, ip, udp_port):
    """
    Protokoll: Anmeldung
    :param name: Nick-Name
    :return: Anmeldedaten als Dict
    """
    user_info = {
        "operation": "connect",
        "nick_name": name,
        "ip_address": ip,  # str(socket.gethostbyname(socket.gethostname()))
        "udp_port": udp_port
    }
    return user_info


def protocol_broadcast(msg, person):
    """
    Protokoll: Broadcast Nachricht die an Server geschickt wird
    Der Server leitet die Nachricht per UDP an alle anderen
    Teilnehmer weiter
    :param msg: Nachricht
    :param person: Eigener Name damit dieser beim Chat-Partner
    angezeigt wird
    :return: Broadcast Nachricht als Dict
    """
    broadcast = {
        "operation": "broadcast",
        "from": person,
        "msg": msg
    }
    return broadcast


def protocol_stups(name, socket):
    """
    Protokoll: Zum Stupsen wird der eigene Name und
    der eigene TCP Port mitgeschickt
    :param name: nick_name
    :param socket: TCP Socket
    :return: Stupser als Dict
    """
    stups = {
        "operation": "stups",
        "user_info": f"Du wurdest von {name} angestupst!\n"
                     f"Sein port: {socket}\n"
                     f"Um zu chatten: \n"
                     f"chat <name> <port>     : Anschreiben\n"
    }
    return stups


def protocol_message(msg):
    message = {
        "operation": "chat",
        "user_info": msg
    }
    return message
