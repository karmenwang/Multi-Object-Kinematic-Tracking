from numpy_ringbuffer import RingBuffer
count = 0
count1 = 2
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
    count += 1
print(ring_buffer_2d)
for i in range(0, 5):
    ring_buffer_2d[0].popleft()
print(ring_buffer_2d[0][len(ring_buffer_2d[0])-1])






