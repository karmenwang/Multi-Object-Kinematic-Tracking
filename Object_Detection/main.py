# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
import time
import sched

# file imports

import Classes.IMGProcess as VideoSetUp
import Classes.OnScreenObject as OnScreenObject
import Classes.Scheduler as Scheduler

# Constants #####################
LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
SAMPLE_SIZE = 10
TIME_INTERVAL = 1000
var = 0

# Create new object #############
image = VideoSetUp.IMGProcess()
objectSchedule = Scheduler.Scheduler()
trackBar = VideoSetUp.TrackBar()

# Set object parameters #########
image.webcam = True
image.path = 'Example_Code/shapes.png'
image.percentage = 60

while True:
    if objectSchedule.scheduler is not None:
        objectSchedule.scheduler.run(True)

    # Initializing img with an option to re.size
    img = image.capture_image()
    imgContour = img.copy()
    image.prep_contour_img(img)
    objectEdgePoint_array = image.get_contour_img(imgContour, LINE_COORD[0][0])
    # objectEdgePoint = image.object_edge(imgContour)
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    # Line Threshold
    cv2.line(imgContour, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)

    for objectEdgePoint in objectEdgePoint_array:
        # print(str(objectEdgePoint_array.index(objectEdgePoint)) + str(objectEdgePoint))
        cv2.putText(imgContour, "%s" % objectEdgePoint_array.index(objectEdgePoint),
                    (objectEdgePoint[0] + 10, objectEdgePoint[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)
        try:
            objectOnScreen = OnScreenObject.OnScreenObject(SAMPLE_SIZE)

        except TypeError:
            print("No objects detected")

        else:
            objectOnScreen.determineVectors(objectEdgePoint=objectEdgePoint)
            objectSchedule.scheduler.enter(1, 0, objectOnScreen.AverageCalculator(), argument=(var,))

    imgStack = VideoSetUp.stack_images(0.8, ([img, imgContour, image.colorMask]))
    # cv2.imshow("Result", imgStack)
    cv2.imshow("Contour", imgContour)

    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
