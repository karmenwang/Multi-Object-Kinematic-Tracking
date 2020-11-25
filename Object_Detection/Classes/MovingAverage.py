import collections
import numpy as np
from scipy.ndimage.filters import uniform_filter1d
from numpy_ringbuffer import RingBuffer


class MovingAverage:

    def __init__(self, sampleNumber=None, sampleArray=None):
        if sampleArray is None:
            sampleArray = [0]
        self.sampleNumber = sampleNumber
        self.indexNumber = 1
        self.sampleArray = sampleArray
        self.indexCounter = 1  # checks to see if our array has been filled up
        self.ring = RingBuffer(sampleNumber, float, True)
        self.averageVelocity = None

    def ring_buffer(self, sampleData):
        self.ring.append(sampleData)
        return

    def avg_function(self, x, length):
        self.averageVelocity = uniform_filter1d(x, length, mode='constant', origin=-(length // 2))[
            :-(length - 1)]

    def convolution_avg_function(self, x, length):
        self.averageVelocity = np.convolve(x, np.ones(length) / float(length), 'valid')

