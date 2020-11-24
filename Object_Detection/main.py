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

xVelocityArray = [0] * SAMPLE_SIZE
yVelocityArray = [0] * SAMPLE_SIZE

# Create new object #############
image = VideoSetUp.IMGProcess()

trackBar = VideoSetUp.TrackBar()

timeVariable = time.time()
timeLast = time.time()

xMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, xPosSampleArray)
yMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, yPosSampleArray)
tMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE, timeSampleArray)

# Set object parameters #########
image.webcam = True
image.path = 'Resources/6.png'
image.percentage = 60

while True:
    # Initializing img with an option to resize
    img = image.capture_image()

    imgContour = img.copy()
    image.get_dilation_img(img)
    objectEdgePoint = image.object_edge(imgContour)
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    # Line Threshold
    cv2.line(imgContour, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)
    try:
        xMovingAverage.ring_buffer(objectEdgePoint[0])
        yMovingAverage.ring_buffer(objectEdgePoint[1])
        tMovingAverage.ring_buffer(time.time())

    except TypeError:
        print("No object detected")

    xPosSampleArray = xMovingAverage.ring
    yPosSampleArray = yMovingAverage.ring

    # Compare object to threshold line
    try:
        if objectEdgePoint[0] >= LINE_COORD[0][0]:  # if object has crossed threshold along x
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 255, 0), cv2.FILLED)  # Edge point dot will turn green

        else:
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 0, 255), cv2.FILLED)  # Edge point dot will turn green

        xVector = Speed.CalculateSpeed(xPosSampleArray[xMovingAverage.sampleNumber - 2],
                                       xPosSampleArray[xMovingAverage.sampleNumber - 1],
                                       timeSampleArray[tMovingAverage.sampleNumber - 2],
                                       timeSampleArray[tMovingAverage.sampleNumber - 1])
        yVector = Speed.CalculateSpeed(yPosSampleArray[xMovingAverage.sampleNumber - 2],
                                       yPosSampleArray[yMovingAverage.sampleNumber - 1],
                                       timeSampleArray[tMovingAverage.sampleNumber - 2],
                                       timeSampleArray[tMovingAverage.sampleNumber - 1])

    except TypeError:
        objectEdgePoint = pastObjectEdgePoint  # if TypeError occurs previous point
        print("Type Error")

    else:
        pastObjectEdgePoint = objectEdgePoint  # update previous point

    imgStack = VideoSetUp.stack_images(0.8, ([img, imgContour, image.colorMask]))
    cv2.imshow("Result", imgStack)

    xVelocityArray.append(xVector.get_velocity_vector())
    yVelocityArray.append(yVector.get_velocity_vector())
    timeVariable = time.time()
    
    if timeVariable - timeLast >= 1:
        xMovingAverage.avg_function(xVelocityArray, len(xVelocityArray))
        yMovingAverage.avg_function(yVelocityArray, len(yVelocityArray))
        print(xMovingAverage.averageArray)
        print(yMovingAverage.averageArray)
        xVelocityArray.clear()
        yVelocityArray.clear()
        timeLast = time.time()

    if not image.webcam:
        cv2.waitKey(0)

    elif cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
