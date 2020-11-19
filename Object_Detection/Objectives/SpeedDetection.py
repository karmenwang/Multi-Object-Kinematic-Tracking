class CalculateSpeed:

    def __init__(self, lastPoint, currentPoint, lastPointTime, currentPointTime):
        self.currentPoint = currentPoint
        self.lastPoint = lastPoint
        self.lastPointTime = lastPointTime
        self.currentPointTime = currentPointTime

    def getVelocityVector(self):
        positionVector = self.currentPoint - self.lastPoint  # position vector = final - initial
        timePassed = (self.currentPointTime - self.lastPointTime)
        if timePassed == 0:
            timePassed = 1  # assume 1 millisecond has passed if no time has passed
        velocityVector = positionVector / timePassed    # (pos final - pos initial)/(T final-T initial)

        return velocityVector
