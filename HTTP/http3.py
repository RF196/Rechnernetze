import requests
from bs4 import BeautifulSoup
import time

LOGIN = 'rnetin'
PASSWORT = 'Ueben8fuer8RN'

start_url = 'https://moodle.htwg-konstanz.de/moodle/'

login_url = 'https://moodle.htwg-konstanz.de/moodle/login/index.php'

chat_url = 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=354'

session = requests.Session()

response = session.get(start_url)

soup = BeautifulSoup(response.content, "lxml")


"""
Nachdem wir die Seite besucht haben wollen wir UNSEREN Token haben
"""

"""
Befindet sich im input-tag hole den value aus dem key {'name':'logintoken'}
"""
token = soup.find('input', {'name': 'logintoken'})['value']
print(token)

data = {
    "logintoken": token,
    "username": LOGIN,
    "password": PASSWORT
}

response = session.post(url=login_url, data=data)

file_url = 'https://moodle.htwg-konstanz.de/moodle/pluginfile.php/346660/mod_assign/introattachment/0/AIN%20RN%20' \
           '-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1" id="yui_3_17_2_1_1624096281987_43 '


download_response = session.get(url=file_url)
if download_response.status_code == 200:
    file = open('http.pdf', "wb").write(download_response.content)
    print('Download erfolgreich!')


"Ermitteln des verdammten Session Keys..."
response = session.get(chat_url)
soup = BeautifulSoup(response.content, "lxml")
last = int(time.time())
sesskey = soup.find(attrs={"name": "sesskey"})["value"]

data = {
    "message": "",
    "id": 354,
    "groupid": 0,
    "last": last,
    "sesskey": sesskey,
    "refresh": "Aktualisieren",
    "newonly": 0
}

# Nachrichten auslesen
response = session.post(chat_url, data=data)
soup = BeautifulSoup(response.content, "lxml")
print(soup.find("div", {"id": "messages"}).text)
print()

"""
Hier bitte eine Nachricht eintragen
"""
message = 'Hi'

# FormData bauen
formData = {
    "message": message,
    "id": 354,
    "groupid": 0,
    "last": last,
    "sesskey": sesskey
}

response = session.post(chat_url, data=formData)
