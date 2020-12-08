import numpy as np
from scipy.ndimage.filters import uniform_filter1d


class CalculateAverage:

    def __init__(self):
        self.average_velocity = None

    def avg_function(self, x, length):
        self.average_velocity = uniform_filter1d(x, length, mode='constant', origin=-(length // 2))[
            :-(length - 1)]

    def convolution_avg_function(self, x, length):
        self.average_velocity = np.convolve(x, np.ones(length) / float(length), 'valid')

