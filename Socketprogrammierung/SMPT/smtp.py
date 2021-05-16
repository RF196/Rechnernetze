import socket
import time

socket.setdefaulttimeout(30)

Remote_IP = 'asmtp.htwg-konstanz.de'
Remote_PORT = 587


def start_task(s, message):
    s.send(message.encode('utf-8'))
    time.sleep(2)
    msg = s.recv(1024)
    print(msg)
    s.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Remote_IP, Remote_PORT))
start_task(sock,
           "AUTH LOGIN\r\n\
           cm5ldGlu\r\n\
           bnRzbW9iaWw=\r\n\
           MAIL FROM:<rnetin@htwg-konstanz.de>\r\n\
           RCPT TO:<lu391kal@htwg-konstanz.de>\r\n\
           DATA\r\n\
           From:<rnetin@htwg-konstanz.de>\r\n\
           To:<fritz@example.org>\r\n\
           Subject: Hallo\r\n\
           \r\n\
           Das ist ein Test.\r\n\
           .\r\n\
           QUIT\r\n")
