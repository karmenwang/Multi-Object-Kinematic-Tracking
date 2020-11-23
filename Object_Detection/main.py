# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
import time

# file imports
import Classes.SpeedDetection as Speed
import Classes.MovingAverage as MovingAverage
import Classes.VideoSetUp as VideoSetUp

# Constants #####################
LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
pastObjectEdgePoint = [0, 0]
SAMPLE_SIZE = 10

timeSampleArray = [time.time()] * SAMPLE_SIZE
xPosSampleArray = [0] * SAMPLE_SIZE
yPosSampleArray = [0] * SAMPLE_SIZE

# Create new object #############
image = VideoSetUp.IMGProcess()

trackBar = VideoSetUp.TrackBar()

xMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, xPosSampleArray)
yMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, yPosSampleArray)
tMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, timeSampleArray)

# Set object parameters #########
image.webcam = True
image.path = 'Resources/6.png'
image.percentage = 60
image.webcam = True

while True:
    # Initializing img with an option to resize
    img = image.capture_image()

    imgContour = img.copy()
    image.get_dilation_img(img)
    objectEdgePoint = image.object_edge(imgContour)
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    # if image.webcam:
    # Line Threshold
    cv2.line(imgContour, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)
    try:
        # print(xMovingAverage.newAveFunction(objectEdgePoint[0]))
        xCounter = xMovingAverage.update_array(objectEdgePoint[0])  # update xPosSampleArray with x coordinate
        yCounter = yMovingAverage.update_array(objectEdgePoint[1])
        tCounter = tMovingAverage.update_array(time.time())

    except TypeError:
        xCounter = 0
        yCounter = 0

    xPosSampleArray = xMovingAverage.get_array()
    yPosSampleArray = yMovingAverage.get_array()

    # Compare object to threshold line
    try:
        if objectEdgePoint[0] >= LINE_COORD[0][0]:  # if object has crossed threshold along x
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 255, 0), cv2.FILLED)  # Edge point dot will turn green

        else:
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 0, 255), cv2.FILLED)  # Edge point dot will turn green

        xVector = Speed.CalculateSpeed(xPosSampleArray[0], xPosSampleArray[xCounter - 1], timeSampleArray[0],
                                       timeSampleArray[tCounter - 1])
        yVector = Speed.CalculateSpeed(yPosSampleArray[0], yPosSampleArray[yCounter - 1], timeSampleArray[0],
                                       timeSampleArray[tCounter - 1])
        print(xMovingAverage.convolutionAveFunction(timeSampleArray))
        # print(xMovingAverage.convolutionAveFunction(xPosSampleArray))
        xVelocity = xVector.get_velocity_vector()
        yVelocity = yVector.get_velocity_vector()
        print("X Velocity {:.2f}".format(xVelocity), "Y Velocity {:.2f}".format(yVelocity))
    except TypeError:
        objectEdgePoint = pastObjectEdgePoint  # if TypeError occurs previous point
        print("Type Error")

    else:
        pastObjectEdgePoint = objectEdgePoint  # update previous point

    imgStack = VideoSetUp.stack_images(0.8, ([img, imgContour, image.colorMask]))
    cv2.imshow("Result", imgStack)

    if not image.webcam:
        cv2.waitKey(0)

    elif cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
