import time
import Classes.SpeedDetection as Speed
import Classes.MovingAverage as MovingAverage


class OnScreenObject:
    def __init__(self, SAMPLE_SIZE, objectID):
        self.objectID = objectID
        self.timeSampleArray = [time.time()] * SAMPLE_SIZE
        self.xPosSampleArray = [0] * SAMPLE_SIZE
        self.yPosSampleArray = [0] * SAMPLE_SIZE

        self.xVelocityArray = [0] * SAMPLE_SIZE
        self.yVelocityArray = [0] * SAMPLE_SIZE

        self.pastObjectEdgePoint = [0, 0]

        self.xMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)
        self.yMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)
        self.tMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)

        self.xVector = 0
        self.yVector = 0

    def determineVectors(self, centroid):
        try:
            self.xMovingAverage.ring_buffer(centroid[0])
            self.yMovingAverage.ring_buffer(centroid[1])
            self.tMovingAverage.ring_buffer(time.time())
            # print(str(self.objectID) + str(self.xMovingAverage.ring))

        except TypeError:
            self.xMovingAverage.ring_buffer(self.pastObjectEdgePoint[0])
            self.yMovingAverage.ring_buffer(self.pastObjectEdgePoint[1])

        else:
            self.pastObjectEdgePoint = centroid

        self.xPosSampleArray = self.xMovingAverage.ring
        self.yPosSampleArray = self.yMovingAverage.ring
        self.timeSampleArray = self.tMovingAverage.ring
        # print(str(self.objectID) + str(self.xPosSampleArray))

        self.xVector = Speed.CalculateSpeed(self.xPosSampleArray[self.xMovingAverage.sampleNumber - 2],
                                            self.xPosSampleArray[self.xMovingAverage.sampleNumber - 1],
                                            self.timeSampleArray[self.tMovingAverage.sampleNumber - 2],
                                            self.timeSampleArray[self.tMovingAverage.sampleNumber - 1])
        self.yVector = Speed.CalculateSpeed(self.yPosSampleArray[self.yMovingAverage.sampleNumber - 2],
                                            self.yPosSampleArray[self.yMovingAverage.sampleNumber - 1],
                                            self.timeSampleArray[self.tMovingAverage.sampleNumber - 2],
                                            self.timeSampleArray[self.tMovingAverage.sampleNumber - 1])

        self.xVelocityArray.append(self.xVector.get_velocity_vector())
        self.yVelocityArray.append(self.yVector.get_velocity_vector())

    def AverageCalculator(self):
        self.xMovingAverage.avg_function(self.xVelocityArray, len(self.xVelocityArray))
        self.yMovingAverage.avg_function(self.yVelocityArray, len(self.yVelocityArray))
        # print(str(self.objectID) + str(self.xMovingAverage.averageVelocity))
        self.xVelocityArray.clear()
        self.yVelocityArray.clear()
