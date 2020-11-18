import numpy
import collections

class MovingAverage:

    def __init__(self, sampleNumber, sampleArray):
        self.sampleNumber = sampleNumber
        self.indexNumber = 0
        self.sampleArray = sampleArray
        self.indexCounter = 0

    def updateArray(self, sample):
        if self.indexNumber < self.sampleNumber:
            self.sampleArray[self.indexNumber - 1] = sample

            if self.indexCounter == self.sampleNumber:
                self.indexCounter = self.indexCounter

            else:
                self.indexCounter = self.indexNumber

            self.indexNumber += 1

        else:
            self.indexNumber = self.sampleNumber
            temp = collections.deque(self.sampleArray)
            temp.rotate(-1)
            self.sampleArray = list(temp)
            # try:
            self.sampleArray[self.indexNumber-1] = sample
            # except TypeError:
            #     self.sampleArray[self.indexNumber-1] = 1
            # print(self.sampleArray)
            self.indexCounter = self.sampleNumber

        return self.indexCounter

    def getArray(self):
        return self.sampleArray
