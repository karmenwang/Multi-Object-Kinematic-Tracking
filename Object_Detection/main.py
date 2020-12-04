# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
from numpy_ringbuffer import RingBuffer
import time

# file imports
from Classes.CentroidTracker import CentroidTracker
import Classes.IMGProcess as VideoSetUp
import Classes.OnScreenObject as OnScreenObject
import Classes.Scheduler as Scheduler
import Classes.MovingAverage as MovingAverage

# Constants #####################
LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
SAMPLE_SIZE = 5
TIME_INTERVAL = 0.000001
objects_2D_ring_buffer_x = RingBuffer(capacity=4, dtype=RingBuffer)
objects_2D_ring_buffer_y = RingBuffer(capacity=2, dtype=RingBuffer)
objects_2D_ring_buffer_t = RingBuffer(capacity=2, dtype=RingBuffer)
created_2d_ring_buffer = False
past_objects = 0

# Create new object #############
image = VideoSetUp.IMGProcess()
objectSchedule = Scheduler.Scheduler()
trackBar = VideoSetUp.TrackBar()
ct = CentroidTracker()
xMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)
yMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)
tMovingAverage = MovingAverage.MovingAverage(SAMPLE_SIZE)

# Set object parameters #########
image.webcam = True
image.path = 'Example_Code/Shape_Detection/shapes.png'
image.percentage = 60

while True:
    if objectSchedule.scheduler is not None:
        objectSchedule.scheduler.run(True)

    # Initializing img with an option to re.size
    img = image.capture_image()
    imgContour = img.copy()
    image.prep_contour_img(img)
    bounding_box_array = image.get_contour_img(imgContour, LINE_COORD[0][0])
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    # Line Threshold
    cv2.line(imgContour, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)

    objects = ct.update(bounding_box_array)
    # print(objects)

    if not created_2d_ring_buffer:
        for objectID in range(0, len(bounding_box_array)):
            # timeSampleArray = [time.time()] * SAMPLE_SIZE

            objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_y.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_t.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            created_2d_ring_buffer = True
        # print(objects_2D_ring_buffer_x)

    try:
        if len(objects) > past_objects:
            objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
    except TypeError:
        print("past_object is None type")

    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid
        cv2.putText(imgContour, "ID {}".format(objectID), (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(imgContour, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        print("should be: " + str(objectID) + " " + str(centroid[0]) + " " + str(centroid[1]))
        try:
            objects_2D_ring_buffer_x[objectID].append(centroid[0])
            objects_2D_ring_buffer_y[objectID].append(centroid[1])
            objects_2D_ring_buffer_t[objectID].append(time.time())
            print("results X: " + str(objectID) + " " + str(objects_2D_ring_buffer_x))
            print("results Y: " + str(objectID) + " " + str(objects_2D_ring_buffer_y))
            print("results Time: " + str(objectID) + " " + str(objects_2D_ring_buffer_t))

        except (IndexError, AttributeError):
            print("index out of range")

    if objects_2D_ring_buffer_x._left_index + objects_2D_ring_buffer_x._right_index == objects_2D_ring_buffer_x.maxlen:
        print("object_2D_ring_buffer has been filled")
        ct.nextObjectID = 0

    # for (objectID, centroid) in objects.items():
    #     try:
    #         objectOnScreen = OnScreenObject.OnScreenObject(SAMPLE_SIZE, objectID)
    #
    #     except TypeError:
    #         print("No objects detected")
    #
    #     else:
    #         objectOnScreen.determineVectors(centroid=centroid)
    #         objectSchedule.scheduler.enter(TIME_INTERVAL, 0, objectOnScreen.AverageCalculator)

    imgStack = VideoSetUp.stack_images(0.8, ([img, imgContour, image.colorMask]))
    # cv2.imshow("Result", imgStack)
    cv2.imshow("Contour", imgContour)

    past_objects = len(objects)

    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
