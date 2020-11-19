# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
import time

# file imports
import Objectives.ContourAndColorDetection as ContourAndColor
import Objectives.SpeedDetection as Speed
import Objectives.MovingAverage as MovingAverage
import Objectives.Utilities as Utilities

##########################
# Video Settings
webcam = True  # Toggle between image or webcam
cap = cv2.VideoCapture(0)  # use default camera
# cap.set(10, 160)  # brightness
# cap.set(3, 1920)  # width
# cap.set(4, 1080)  # height

# Image Settings
path = '../Resources/9.png'
scale_percent = 60  # 30

##########################
line_coord = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
pastObjectEdgePoint = [0, 0]
sampleSize = 10  # array size

# time, x, y array for sample points
timeSampleArray = [time.time()] * sampleSize
xPosSampleArray = [0] * sampleSize
yPosSampleArray = [0] * sampleSize

# create objects of Moving Average class
xMovingAverage = MovingAverage.MovingAverage(sampleSize, xPosSampleArray)
yMovingAverage = MovingAverage.MovingAverage(sampleSize, yPosSampleArray)
tMovingAverage = MovingAverage.MovingAverage(sampleSize, timeSampleArray)

# create object for display window utilities
image = Utilities.Utilities(webcam, path, cap)

while True:
    # Initializing img with an option to resize
    img = image.InitializeImg(scale_percent)
    imgContour = img.copy()
    imgDilation = ContourAndColor.getDilation(img)
    objectEdgePoint = ContourAndColor.getContours(imgDilation, imgContour)  # Call on function to find Contour

    # Line Threshold
    cv2.line(imgContour, (line_coord[0][0], line_coord[0][1]), (line_coord[1][0], line_coord[1][1]), (0, 0, 255), 2)

    try:
        xCounter = xMovingAverage.updateArray(objectEdgePoint[0])   # update xPosSampleArray with x coordinate
        yCounter = yMovingAverage.updateArray(objectEdgePoint[1])
        tCounter = tMovingAverage.updateArray(time.time())

    except TypeError:
        xCounter = 0
        yCounter = 0

    xPosSampleArray = xMovingAverage.getArray()
    yPosSampleArray = yMovingAverage.getArray()

    # compare object to threshold line
    try:
        if objectEdgePoint[0] >= line_coord[0][0]:  # if object has crossed threshold along x
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 255, 0), cv2.FILLED)
            # print("passed")

        else:
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 0, 255), cv2.FILLED)
            # print("not passed")

        xVector = Speed.CalculateSpeed(xPosSampleArray[0], xPosSampleArray[xCounter - 1], timeSampleArray[0],
                                       timeSampleArray[tCounter - 1])
        yVector = Speed.CalculateSpeed(yPosSampleArray[0], yPosSampleArray[yCounter - 1], timeSampleArray[0],
                                       timeSampleArray[tCounter - 1])

        xVelocity = xVector.getVelocityVector()
        yVelocity = yVector.getVelocityVector()

        # print(xPosSampleArray)
        # print(yPosSampleArray)
    except TypeError:
        objectEdgePoint = pastObjectEdgePoint  # if TypeError occurs previous point
        print("Type Error")

    else:
        pastObjectEdgePoint = objectEdgePoint  # update previous point

    # Select Custom Color to Detect
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert BGR to HSV

    HSVMinMaxArray = ContourAndColor.readTrackBars()

    imgHSVResult = ContourAndColor.getHSV(img, imgHSV, HSVMinMaxArray)

    # stack the different types of images together
    imgStack = Utilities.stackImages(0.8, ([img, imgContour], [imgHSV, imgHSVResult]))

    # display image
    cv2.imshow("Result", imgStack)

    # press 'q' to exit from run
    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
