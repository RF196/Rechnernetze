import math
from copy import copy
from threading import Thread, Event, Lock, Timer
import time
import os

lock = Lock()

SPEED_UP = 1

PERIOD_A = 200 / SPEED_UP
CUSTOMER_NUMBER_A = 0
PERIOD_B = 60 / SPEED_UP
CUSTOMER_NUMBER_B = 0

CUSTOMER_TOTAL_NUMBER = 0
BUYING_COMPLETED_NUMBER = 0
BUYING_NUMBER = 0

BUYING_DURATION = 0
BUYING_COMPLETED_DURATION = 0

BREAD_STATION_VISITS = 0
SAUSAGE_STATION_VISITS = 0
CHEESE_STATION_VISITS = 0
CASH_DESK_STATION_VISITS = 0

BREAD_STATION_SKIPS = 0
CHEESE_STATION_SKIPS = 0
SAUSAGE_STATION_SKIPS = 0
CASH_DESK_STATION_SKIPS = 0


class Customer(Thread):
    def __init__(self, station_list, customer_type, customer_number):
        Thread.__init__(self)
        self.station_list = station_list
        self.customer_type = customer_type
        self.customer_number = customer_number
        self.serv_ev = Event()
        self.serv_ev.set()

        self.skipped_station = False
        self.start_buying_time = time.perf_counter()

    def run(self):
        while self.station_list:
            self.serv_ev.wait(timeout=1/SPEED_UP)
            lock.acquire()
            output_evaluations()
            lock.release()
            if self.serv_ev.is_set():
                station_t_w_n = self.station_list[0]
                station = station_t_w_n[0]
                transfer = station_t_w_n[1]
                max_people = station_t_w_n[2]

                # Ausgabe
                log_begin(self)

                lock.acquire()
                self.serv_ev.clear()
                lock.release()
                time.sleep(transfer / SPEED_UP)

                if len(station.customer_queue) > max_people:
                    # Überspringe Station
                    print("Überspringe Station")
                    lock.acquire()
                    self.station_list.pop(0)
                    self.skipped_station = True
                    eval_station_skips(station)
                    self.serv_ev.set()
                    lock.release()
                else:
                    log_arrival(self, station)
                    eval_stations(station)
                    station.einreihen(self)


class Station(Thread):
    def __init__(self, name, serving_time):
        Thread.__init__(self)
        self.name = name
        self.serving_time = serving_time
        self.customer_queue = []
        self.arr_ev = Event()
        self.busy = False

    def run(self):
        while True:
            self.arr_ev.wait(timeout=1 / SPEED_UP)
            if self.arr_ev.is_set() and not self.busy:
                self.busy = True
                customer = self.customer_queue.pop(0)
                station_t_w_n = customer.station_list.pop(0)
                station = station_t_w_n[0]
                items_number = station_t_w_n[3]
                waiting_time = station.serving_time * items_number

                time.sleep(waiting_time / SPEED_UP)

                lock.acquire()
                customer.serv_ev.set()
                self.arr_ev.clear()
                self.busy = False
                eval_buying(customer)
                log_leave(self, customer)
                lock.release()

    def einreihen(self, customer):
        lock.acquire()
        self.customer_queue.append(customer)
        self.arr_ev.set()
        lock.release()


def eval_buying(customer):
    global BUYING_COMPLETED_NUMBER
    global BUYING_NUMBER
    global BUYING_DURATION
    global BUYING_COMPLETED_DURATION

    if len(customer.station_list) < 1:
        BUYING_NUMBER += 1
        BUYING_DURATION += time.perf_counter() - customer.start_buying_time
        if not customer.skipped_station:
            BUYING_COMPLETED_NUMBER += 1
            BUYING_COMPLETED_DURATION += time.perf_counter() - customer.start_buying_time


def eval_stations(station):
    global BREAD_STATION_VISITS
    global CHEESE_STATION_VISITS
    global SAUSAGE_STATION_VISITS
    global CASH_DESK_STATION_VISITS
    if station.name == "Brottheke":
        BREAD_STATION_VISITS += 1
    elif station.name == "Wursttheke":
        SAUSAGE_STATION_VISITS += 1
    elif station.name == "Kaesetheke":
        CHEESE_STATION_VISITS += 1
    elif station.name == "Kasse":
        CASH_DESK_STATION_VISITS += 1


def eval_station_skips(station):
    global BREAD_STATION_SKIPS
    global CHEESE_STATION_SKIPS
    global SAUSAGE_STATION_SKIPS
    global CASH_DESK_STATION_SKIPS
    if station.name == "Brottheke":
        BREAD_STATION_SKIPS += 1
    elif station.name == "Wursttheke":
        SAUSAGE_STATION_SKIPS += 1
    elif station.name == "Kaesetheke":
        CHEESE_STATION_SKIPS += 1
    elif station.name == "Kasse":
        CASH_DESK_STATION_SKIPS += 1


def output_evaluations():
    if math.trunc(time.perf_counter()) > 1800 / SPEED_UP:
        print(CHEESE_STATION_VISITS)

        output_strings = ["Anzahl Kunden: " + str(CUSTOMER_TOTAL_NUMBER) + "\n",
                          "Anzahl Einkaeufe " + str(BUYING_NUMBER) + "\n",
                          "Anzahl vollstaendige Einkaeufe: " + str(BUYING_COMPLETED_NUMBER) + "\n",
                          "Mittelere Einkaufsdauer: " + str(BUYING_DURATION / BUYING_NUMBER) + "\n",
                          "Mittelere Einkaufsdauer (vollstaendig) " + str(
                              BUYING_COMPLETED_DURATION / BUYING_COMPLETED_NUMBER) + "\n \n",

                          "Anzahl Besuche Brotstation " + str(BREAD_STATION_VISITS) + " \n",
                          "Anzahl Besuche Wurststation " + str(SAUSAGE_STATION_VISITS) + " \n",
                          "Anzahl Besuche Kaesestation " + str(CHEESE_STATION_VISITS) + " \n",
                          "Anzahl Besuche Kasse " + str(CASH_DESK_STATION_VISITS) + " \n",

                          "Ausfallrate Brotstation " + str((BREAD_STATION_SKIPS / BREAD_STATION_VISITS) * 100) + "%" + "\n",
                          "Ausfallrate Wurststation " + str((SAUSAGE_STATION_SKIPS / SAUSAGE_STATION_VISITS) * 100) + "%" + "\n",
                          "Ausfallrate Kaesestation " + str((CHEESE_STATION_SKIPS / CHEESE_STATION_VISITS) * 100) + "%" + "\n",
                          "Ausfallrate Kasse " + str((CASH_DESK_STATION_SKIPS / CASH_DESK_STATION_VISITS) * 100) + "%" + "\n"]

        output = open("supermarkt.txt", "w+")
        for line in range(len(output_strings)):
            output.write(output_strings[line])
        output.close()
        os._exit(0)


def log_begin(self):
    if ((self.customer_type == 'A' and len(self.station_list) == 4)
            or (self.customer_type == 'B' and len(self.station_list) == 3)):
        print(str(math.trunc(time.perf_counter())) + " Beginn " + str(self.customer_type)
              + str(self.customer_number))


def log_arrival(self, station):
    print(str(math.trunc(time.perf_counter())) + " Ankunft " + str(station.name) + " " + str(
        self.customer_type) + str(self.customer_number))


def log_leave(self, customer):
    print(str(math.trunc(time.perf_counter())) + " Verlassen " + str(self.name) + " " + str(
        customer.customer_type) + str(customer.customer_number))


"""
Initial values
"""

"""
stations with name and duration per item
"""
bread_station = Station("Brottheke", 10)
sausage_station = Station("Wursttheke", 30)
cheese_station = Station("Kaesetheke", 60)
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


def start_customer_a():
    global CUSTOMER_NUMBER_A, CUSTOMER_TOTAL_NUMBER
    CUSTOMER_NUMBER_A += 1
    CUSTOMER_TOTAL_NUMBER += 1
    new_customer = Customer(station_list=copy(station_list_a),
                            customer_type='A',
                            customer_number=CUSTOMER_NUMBER_A)
    new_customer.start()
    Timer(PERIOD_A, start_customer_a).start()


def start_customer_b():
    global CUSTOMER_NUMBER_B, CUSTOMER_TOTAL_NUMBER
    CUSTOMER_NUMBER_B += 1
    CUSTOMER_TOTAL_NUMBER += 1
    new_customer = Customer(station_list=copy(station_list_b),
                            customer_type='B',
                            customer_number=CUSTOMER_NUMBER_B)

    new_customer.start()
    Timer(PERIOD_B, start_customer_b).start()


bread_station.start()
sausage_station.start()
cheese_station.start()
cash_desk_station.start()


def start():
    start_customer_a()
    time.sleep(1)
    start_customer_b()


# Start the simulation
start()
