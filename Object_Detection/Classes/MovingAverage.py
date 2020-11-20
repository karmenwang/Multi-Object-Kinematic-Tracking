import collections


class MovingAverage:

    def __init__(self, sampleNumber=None, sampleArray=[0]):
        self.sampleNumber = sampleNumber
        self.indexNumber = 0
        self.sampleArray = sampleArray
        self.indexCounter = 0  # checks to see if our array has been filled up

    # update array with new points, replacing array[sampleNumber-1] with the new data point and shifting prev data left
    def update_array(self, sampleData):
        if self.indexNumber < self.sampleNumber:
            self.sampleArray[self.indexNumber - 1] = sampleData

            if self.indexCounter == self.sampleNumber:  # counter tells us that we are at the max index
                self.indexCounter = self.indexCounter

            else:
                self.indexCounter = self.indexNumber

            self.indexNumber += 1

        else:
            self.indexNumber = self.sampleNumber  # if we have filled the array, stay in the max index
            temp = collections.deque(self.sampleArray)  # create temporary array for shifting
            temp.rotate(-1)  # shift left
            self.sampleArray = list(temp)  # convert to a list
            self.sampleArray[self.indexNumber - 1] = sampleData  # only index at max array gets new data
            self.indexCounter = self.sampleNumber  # lets us know that array is still fully occupied

        return self.indexCounter

    def get_array(self):
        return self.sampleArray
