import cv2
import time
import numpy as np


class CalculateSpeed:

    def __init__(self, lastPoint, currentPoint, lastPointTime, currentPointTime):
        self.currentPoint = currentPoint
        self.lastPoint = lastPoint
        self.lastPointTime = lastPointTime
        self.currentPointTime = currentPointTime

    def getVelocityVector(self):
        positionVector = self.currentPoint - self.lastPoint
        timePassed = (self.currentPointTime - self.lastPointTime)
        if timePassed == 0:
            timePassed = 1
        velocityVector = positionVector/timePassed
        print(velocityVector)
        return velocityVector


