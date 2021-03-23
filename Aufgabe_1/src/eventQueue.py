from station import Station


# (ereigniszeitpunkt, ereignispriorität, ereignisnummer, ereignisfunktion, ereignisargumenten)
#  int              , int              , int           , Customerfunction, Station[Wursttheke, Käsetheke, ..]
#
class EventQueue:

    def __init__(self):
        self.heap = []
        self.step = 0
        self.time = 0

    def pop(self) -> (int, int, int, (), Station):
        # todo
        pass

    def push(self, event: (int, int, int, (), Station)):
        # todo
        pass

    def start(self):
        # todo
        pass
