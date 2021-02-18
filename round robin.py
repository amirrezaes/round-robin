import time
from collections import deque

QUANTUM_TIME = 0.05


def work(n):
    arr = list()
    while n >= 0:
        time.sleep(0.02)
        arr.append(n)
        yield
        n -= 1
    yield arr


queue = deque(maxlen=3)
queue.extend([work(10), work(100), work(1000)])
done = {}
time_sum = 0
rounds = {}
while len(queue) > 0:
    current = queue.popleft()
    beg = time.time()
    try:
        result = next(current)
    except StopIteration:
        print(current, 'finished in:', done[current], '\n', 'rounds:',rounds[current] - 1)
        continue
    finally:
        end = time.time()
        rounds[current] = rounds.get(current, 0) + 1
        time_sum += (end - beg)
    if time_sum >= QUANTUM_TIME:
        queue.append(current)
        done[current] = done.get(current, 0.0) + (time_sum)
        time_sum = 0
        continue
    queue.appendleft(current)