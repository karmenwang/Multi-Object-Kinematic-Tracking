from numpy_ringbuffer import RingBuffer
count = 0
count1 = 2
r = RingBuffer(capacity=5, dtype=int)
length = 2
ring_buffer_2d = []
created = False

while count < 20:
    if not created:
        for i in range(0, length):
            ring_buffer_2d.append(RingBuffer(capacity=5, dtype=int))
        created = True

    for i in range(0, length):
        if i == 1:
            ring_buffer_2d[i].append(count1)
            count1 = count1*2
        else:
            ring_buffer_2d[i].append(count)
    print(str(ring_buffer_2d[0]._left_index) + " " +str(ring_buffer_2d[0]._right_index))
    count += 1
    print(ring_buffer_2d[0])




