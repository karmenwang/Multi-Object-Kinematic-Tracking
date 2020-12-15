import cv2
import Classes.IMGProcess as IMGProcess
# import Classes.CentroidTracker as CentroidTracker

LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]

trackBar = IMGProcess.TrackBar()
image = IMGProcess.IMGProcess()
# objectDetected = CentroidTracker.CentroidTracker()

image.webcam = True
image.path = '../Example_Code/Shape_Detection/shapes.png'
image.percentage = 60

while True:
    img = image.capture_image()
    imgContour = img.copy()
    image.prep_contour_img(img)
    cv2.line(imgContour, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)

    object_edge_array = image.get_contour_img(imgContour, LINE_COORD[0][0])
    # print(object_edge_array)

    # HSV color detection
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    cv2.imshow("Result", imgContour)

    if not image.webcam:
        cv2.waitKey(0)
    elif cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
