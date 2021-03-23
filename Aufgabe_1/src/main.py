import heapq


h = []
event = EventQueue()
event.print_some()
heapq.heappush(h, (1, 2, 3))
heapq.heappush(h, (3, 1, 3))
heapq.heappush(h, (1, 4, 3))
heapq.heappush(h, (3, 1, 4))
heapq.heapify(h)

# print(h)

for i in range(len(h)):
    print(heapq.heappop(h))
