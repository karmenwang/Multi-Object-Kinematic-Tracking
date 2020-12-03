from numpy_ringbuffer import RingBuffer
count = 0
count1 = 2
r = RingBuffer(capacity=5, dtype=int)
length = 2
ring_buffer_2d = []

while True:
    created = False
    if not created:
        for i in range(0, length):
            ring_buffer_2d.append(RingBuffer(capacity=5, dtype=int))
        created = True

    while count < 10:
        for i in range(0, length):
            if i == 1:
                ring_buffer_2d[i].append(count1)
                count1 = count1*2
            else:
                ring_buffer_2d[i].append(count)
        count += 1
        print(ring_buffer_2d)

    ring_buffer_2d.clear()



