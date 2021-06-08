class Controller:
    def __init__(self, client):
        self.client = client
        self.logged_in = False

    def connect(self, name):
        self.client.connect(name=name)

    def disconnect(self):
        self.client.disconnect()

    def stups(self, name):
        self.client.stups(nick_name=name)

    def start_chat(self, name, port):
        self.client.start_chat(nick_name=name, port=port)

    def broadcast(self):
        self.client.broadcast()
