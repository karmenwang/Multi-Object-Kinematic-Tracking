# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
import numpy as np  # numpy

# file imports
import Objectives.ContourAndColorDetection as ContourAndColor

##########################
# Video Settings

webcam = True  # Toggle between image or webcam
cap = cv2.VideoCapture(0)  # use default camera
cap.set(10, 160)  # brightness
cap.set(3, 1920)  # width
cap.set(4, 1080)  # height

# Image Settings
path = '../Resources/9.png'
scale_percent = 60  # 30

##########################
line_coord = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
pastObjectEdgePoint = [0, 0]

while True:
    if webcam:
        success, img = cap.read()
    else:
        img = cv2.imread(path)

    # Resizing and Cropping Original Photo
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dimensions = (width, height)
    imgResized = cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)
    # imgCropped = imgResized[y:y + h, x:x + w]
    imgCropped = imgResized

    # Contour Prep
    imgContour = imgCropped.copy()  # Take a copy of original img
    imgBlur = cv2.GaussianBlur(imgCropped, (7, 7), 1)  # Apply slight blur
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)  # Apply grayscale
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")  # Lower threshold bound
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")  # Upper threshold boundq
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)  # Apply edge detection (Canny)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)  # Process for filtering out background noise
    objectEdgePoint = ContourAndColor.getContours(imgDil, imgContour)  # Call on function to find Contour

    # Line Threshold
    cv2.line(imgContour, (line_coord[0][0], line_coord[0][1]), (line_coord[1][0], line_coord[1][1]), (0, 0, 255), 2)

    # compare object to threshold line
    try:
        if objectEdgePoint[0] >= line_coord[0][0]:  # if object has crossed threshold along x
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 255, 0), cv2.FILLED)
            print("passed")

        else:
            cv2.circle(imgContour, objectEdgePoint, 5, (0, 0, 255), cv2.FILLED)
            print("not passed")

    except TypeError:
        objectEdgePoint = pastObjectEdgePoint   # if TypeError occurs previous point
        print("Type Error")

    else:
        pastObjectEdgePoint = objectEdgePoint   # update previous point

    # Select Custom Color to Detect
    imgHsv = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2HSV)    #convert BGR to HSV

    # record track bar position (user input)
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # create mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(imgCropped, imgCropped, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the different types of images together
    imgHsvStack = ContourAndColor.stackImages(0.8, ([imgCropped, imgHsv], [mask, result]))
    imgEdgeStack = ContourAndColor.stackImages(0.8, ([imgCropped, imgCanny], [imgDil, imgContour]))

    # display image
    cv2.imshow("Contour Result", imgEdgeStack)
    # cv2.imshow("HSV Result", imgHsvStack) # commented out for now to reduce traffic when running

    # press 'q' to exit from run
    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
