class CalculateSpeed:

    def __init__(self, lastPoint, currentPoint, lastPointTime, currentPointTime):
        self.currentPoint = currentPoint
        self.lastPoint = lastPoint
        self.lastPointTime = lastPointTime
        self.currentPointTime = currentPointTime

    def get_velocity_vector(self):
        positionVector = self.currentPoint - self.lastPoint  # position vector = final - initial
        timePassed = (self.currentPointTime - self.lastPointTime)
        if timePassed == 0:
            timePassed = 0.001  # assume 1 microsecond has passed if no time has passed
        velocityVector = positionVector / timePassed    # (pos final - pos initial)/(T final-T initial)

        return velocityVector
