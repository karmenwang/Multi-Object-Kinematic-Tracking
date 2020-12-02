import numpy as np
from numpy_ringbuffer import RingBuffer

count = 0
count1 = 2
r = RingBuffer(capacity=5, dtype=int)
length = 2
ring_buffer_2d = []

while count < 10:
    for i in range(0, length):
        ring_buffer_2d.append(r)

    for i in range(0, length):
        if i == 1:
            ring_buffer_2d[i].append(count1)
            count1 = count1*2
        else:
            ring_buffer_2d[i].append(count)

        print(ring_buffer_2d)

    ring_buffer_2d.clear()

    count += 1

