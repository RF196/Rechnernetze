import socket
import time
from re import search
from struct import unpack, pack


def op_sum(ops, anzahl):
    sum = 0
    for i in range(anzahl):
        sum += ops[i]
    return sum


def op_mul(ops, anzahl):
    product = 1
    for i in range(anzahl):
        product *= ops[i]
    return product


def op_min(ops, anzahl):
    min_value = ops[0]
    for i in range(anzahl):
        min_value = min(ops[i], min_value)
    return min_value


def op_max(ops, anzahl):
    max_value = ops[0]
    for i in range(anzahl):
        max_value = max(ops[i], max_value)
    return max_value


def process_request(data):
    (id, operation, anzahl) = unpack('<I10sB', data[:15])
    print(anzahl)
    ops = unpack('i' * anzahl, data[15:])
    operation_decoded = operation.decode('utf-8')
    print(operation_decoded)
    result = 0
    print("Performing operation:", operation_decoded)
    if search("Summe", operation_decoded):
        result = op_sum(ops, anzahl)
    elif search("Produkt", operation_decoded):
        result = op_mul(ops, anzahl)
    elif search("Minimum", operation_decoded):
        result = op_min(ops, anzahl)
    elif search("Maximum", operation_decoded):
        result = op_max(ops, anzahl)
    else:
        print("Error: No valid operation")
    return pack('Ii', id, result)


def send_operation(id, operation, ops, send, receive):
    print('Sending:', operation)
    fmt = '<I10sB' + 'i' * len(ops)
    send(pack(fmt, id, operation, len(ops), *ops))
    try:
        msg = receive(1024)  # sock.recv(1024)
        print(msg)
        (id_result, result) = unpack('Ii', msg)
        print('Message received: Id={} Result={}'.format(id_result, result))
    except socket.timeout:
        print('Socket timed out at', time.asctime())
