from station import Station


# (int, int, int) = (T: time_to_station, W: threshold_to_skip_stations, N: num_of_purchases)
class Customer:
    def __init__(self, stations: [(Station, int, int, int)]):
        self.customer_trace = list(stations)
        self.current_station = 0

    def start_purchase(self):
        # todo
        self.customer_trace.pop()
        pass

    def arrive_at_station(self):
        # todo
        pass

    def leave_station(self):
        # todo
        pass