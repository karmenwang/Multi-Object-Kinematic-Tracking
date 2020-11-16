import cv2
import time
import numpy as np

coord = [[50, 0], [50, 500], [631, 512], [952, 512]]

while True:
    success, img = cap.read()  # read every frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert image to gray

    # Contour Prep
    imgContour = img.copy()  # Take a copy of original img
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)  # Apply slight blur
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)  # Apply grayscale
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")  # Lower threshold bound
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")  # Upper threshold bound
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)  # Apply edge detection (Canny)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)  # Process for filtering out background noise
    getContours(imgDil, imgContour)  # Call on function to find Contour

    # cv2.line(imgContour, (coord[0][0], coord[0][1]), (coord[1][0], coord[1][1]), (0, 0, 255), 2)

    # for (x, y, w, h) in objects:
    #     objectCenter_x = (x+w)//2
    #     objectCenter_y = (y+h)//2
    #
    #     if (objectCenter_x >= coord[0][0] and objectCenter_y)


    cv2.imshow('img', imgContour)  # Shows the frame

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
