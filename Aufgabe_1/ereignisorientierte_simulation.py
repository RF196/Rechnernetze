import heapq
from copy import deepcopy, copy

"""
Analog to Priority
"""
LEAVE = 1
BEGIN = 2
ARRIVE = 3

"""
Global variables
"""
SIMULATION_TIME = 0
EVENT_NUMBER = 0


class EventQueue:
    event_number = 1

    def __init__(self):
        self.simulation_time = None
        self.heap_queue = []

    def __repr__(self):
        return str(self.heap_queue)

    def pop(self):
        return heapq.heappop(self.heap_queue)

    def push(self, event):
        heapq.heappush(self.heap_queue, event)

    def start(self):
        i = 0
        while i < 300:
            # while self.heap_queue:
            i += 1
            event = self.pop()
            event[3](event[0])


class Customer:
    def __init__(self, station_list, customer_type="", customer_number=0, period=0):
        self.station_list = station_list
        self.customer_type = customer_type
        self.customer_number = customer_number
        self.period = period

    def __repr__(self):
        return str(self.customer_type) + "-" + str(self.customer_number)

    def begin_buying(self, event_time):
        print(str(event_time)+"s "+"Beginn " + str(self.customer_type) + "-" + str(self.customer_number))
        new_events = []

        station_list = copy(self.station_list)
        new_customer = Customer(station_list=station_list,
                                customer_type=self.customer_type,
                                customer_number=self.customer_number + 1,
                                period=self.period)

        EventQueue.event_number += 1
        event_time_begin = event_time + self.period
        new_events.append((event_time_begin, BEGIN, EventQueue.event_number, new_customer.begin_buying))

        EventQueue.event_number += 1
        t_w_n = self.station_list[0][1:4]
        transfer_time = t_w_n[0]
        event_time_arrive = event_time + transfer_time
        new_events.append((event_time_arrive, ARRIVE, EventQueue.event_number, self.arrive_station))

        for i in new_events:
            event_queue.push(i)

    def arrive_station(self, event_time):
        arrived_station = self.station_list[0]
        station = arrived_station[0]
        print(str(event_time)+"s "+"Ankunft " + str(station.station_name) + str(self.customer_type) + "-" + str(self.customer_number))
        station.enqueue(self, event_time)

    def leave_station(self, event_time):
        print(str(event_time)+"s "+"Verlassen " + str(self.customer_type) + "-" + str(self.customer_number))
        finished_station = self.station_list.pop(0)
        station = finished_station[0]
        station.finish(self, event_time)


class Station:
    def __init__(self, station_name="", serving_duration=None, is_busy=False):
        self.queue = []
        self.station_name = station_name
        self.serving_duration = serving_duration
        self.is_busy = is_busy

    def enqueue(self, customer, event_time):
        t_w_n = customer.station_list[0][1:4]
        people_waiting = len(self.queue)
        max_people = t_w_n[1]
        waiting_time = self.serving_duration * t_w_n[2]
        if self.is_busy:
            if people_waiting >= max_people:
                EventQueue.event_number += 1
                transfer_time_to_next = customer.station_list[1][1]
                event_time_arrive = event_time + transfer_time_to_next
                event_queue.push((event_time_arrive, ARRIVE, EventQueue.event_number, customer.arrive_station))
            else:
                self.queue.append(customer)
            return
        else:
            EventQueue.event_number += 1
            self.is_busy = True
            event_time_leave = event_time + waiting_time
            event_queue.push((event_time_leave, LEAVE, EventQueue.event_number, customer.leave_station))

    def finish(self, customer, event_time):
        self.is_busy = False
        people_waiting = len(self.queue)
        if people_waiting > 0:
            EventQueue.event_number += 1
            self.is_busy = True
            waiting_person = self.queue.pop(0)
            waiting_time = self.serving_duration * waiting_person.station_list[0][2]
            event_time_leave = event_time + waiting_time
            event_queue.push((event_time_leave, LEAVE, EventQueue.event_number, waiting_person.leave_station))

        if not customer.station_list:
            return

        EventQueue.event_number += 1
        transfer_time = customer.station_list[0][1]
        event_time_arrive = event_time + transfer_time
        event_queue.push((event_time_arrive, ARRIVE, EventQueue.event_number, customer.arrive_station))


"""
Initial values
"""

"""
stations with name and duration per item
"""
bread_station = Station("Brottheke", 10)
sausage_station = Station("Wursttheke", 30)
cheese_station = Station("Käsetheke", 60)
cash_desk_station = Station("Kasse", 5)

"""
tuple for customer type A
"""
bread_counter_tuple_a = (bread_station, 10, 10, 10)
sausage_counter_tuple_a = (sausage_station, 30, 10, 5)
cheese_counter_tuple_a = (cheese_station, 45, 5, 3)
cash_desk_tuple_a = (cash_desk_station, 60, 20, 30)

"""
tuple for customer type B
"""
sausage_counter_tuple_b = (sausage_station, 30, 5, 2)
cash_desk_tuple_b = (cash_desk_station, 30, 20, 3)
bread_counter_tuple_b = (bread_station, 20, 20, 3)

station_list_a = [
    bread_counter_tuple_a,
    sausage_counter_tuple_a,
    cheese_counter_tuple_a,
    cash_desk_tuple_a
]

station_list_b = [
    sausage_counter_tuple_b,
    cash_desk_tuple_b,
    bread_counter_tuple_b
]

customer_a = Customer(station_list=station_list_a,
                      customer_type='A',
                      customer_number=1,
                      period=200)

customer_b = Customer(station_list=station_list_b,
                      customer_type='B',
                      customer_number=1,
                      period=60)

func_a = customer_a.begin_buying
func_b = customer_b.begin_buying

event_queue = EventQueue()

initial_events = [(0, BEGIN, EventQueue.event_number, func_a),
                  (1, BEGIN, EventQueue.event_number + 1, func_b)]

for ini_event in initial_events:
    event_queue.push(ini_event)

event_queue.start()
