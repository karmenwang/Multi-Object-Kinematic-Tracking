from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker():
    def __init__(self, maxDisappeared=50):
        self.nextObjectID = 0   # initialize the next unique ID
        self.objects = OrderedDict()    # Dictionary to keep track of mapping given object
        self.disappeared = OrderedDict()    # Mark objects out of given number of frames as "Disappeared"
        self.maxDisappeared = maxDisappeared    # store the number of maximum consecutive frames a given

    # def register(self, objectPoint):
        