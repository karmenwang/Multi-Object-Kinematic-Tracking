import cv2
import numpy as np


def empty(a):
    pass


# create track bars
cv2.namedWindow("Parameters")  # Window name
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 23, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 20, 255, empty)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 57, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 25, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)


def getDilation(img):
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)  # Apply slight blur
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)  # Apply grayscale
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")  # Lower threshold bound
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")  # Upper threshold bound
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)  # Apply edge detection (Canny)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)  # Process for filtering out background noise
    return imgDil


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)  # Use edge detection map img
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")  # Min area set by trackbar
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 2)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)  # Find bounding box
            objectEdge = (x + w, y + (h // 2))  # (right most point, center)

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, "w={},h={}".format(w, h), (x - 175, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (36, 255, 12), 2)
            return objectEdge


def readTrackBars():
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    HSVMinMaxArray = [[h_min, s_min, v_min], [h_max, s_max, v_max]]
    return HSVMinMaxArray


def getHSV(img, imgHSV, HSVArray):
    lower = np.array(HSVArray[0])   # lower bound
    upper = np.array(HSVArray[1])   # upper bound
    mask = cv2.inRange(imgHSV, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return result
