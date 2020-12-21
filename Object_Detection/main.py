# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2  # opencv_python
from numpy_ringbuffer import RingBuffer
import time

# file imports
from Classes.CentroidTracker import CentroidTracker
from Classes.IMGProcess import IMGProcess
from Classes.IMGProcess import TrackBar
from Classes.IMGProcess import stack_images
from Classes.Scheduler import Scheduler
from Classes.CalculateAverage import CalculateAverage

# Constants/Initialization ######
MAX_CAPACITY = 5
SAMPLE_SIZE = 5
LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
TIME_INTERVAL = 0.000001
objects_2D_ring_buffer_x = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)
objects_2D_ring_buffer_y = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)
objects_2D_ring_buffer_t = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)
created_2d_ring_buffer = False
past_object_num = 0

# Create new object #############
image = IMGProcess()
object_scheduler = Scheduler()
track_bar = TrackBar()
centroid_tracker = CentroidTracker()
calculate_x_average = CalculateAverage()
calculate_y_average = CalculateAverage()
calculate_t_average = CalculateAverage()

# Set object parameters #########
image.webcam = True
image.path = 'Example_Code/Shape_Detection/shapes.png'
image.percentage = 60

while True:
    if object_scheduler.scheduler is not None:    # time scheduler for velocity calculations
        object_scheduler.scheduler.run(True)

    # Initializing img
    img = image.capture_image()
    img_results = img.copy()
    image.prep_contour_img(img)
    bounding_box_array = image.get_contour_img(img_results, LINE_COORD[0][0])
    image.get_hsv_img(img, track_bar.HSVMinMaxArray)

    # Draw line Threshold
    cv2.line(img_results, (LINE_COORD[0][0], LINE_COORD[0][1]), (LINE_COORD[1][0], LINE_COORD[1][1]), (0, 0, 255), 2)

    # update centroid tracker with bounding boxes of detected objects
    objects = centroid_tracker.update(bounding_box_array)

    # create initial Ring Buffer indexes based on detected objects
    if not created_2d_ring_buffer:
        for objectID in range(0, len(bounding_box_array)):

            objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_y.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_t.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            created_2d_ring_buffer = True
        # print(objects_2D_ring_buffer_x)

    try:
        if len(objects) > past_object_num:
            objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
    except TypeError:
        print("past_object is None type")

    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid
        cv2.putText(img_results, "ID {}".format(objectID), (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(img_results, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        print("should be: " + str(objectID) + " " + str(centroid[0]) + " " + str(centroid[1]))
        try:
            objects_2D_ring_buffer_x[objectID].append(centroid[0])
            objects_2D_ring_buffer_y[objectID].append(centroid[1])
            objects_2D_ring_buffer_t[objectID].append(time.time())
            # print("results X: " + str(objectID) + " " + str(objects_2D_ring_buffer_x))
            # print("results Y: " + str(objectID) + " " + str(objects_2D_ring_buffer_y))
            # print("results Time: " + str(objectID) + " " + str(objects_2D_ring_buffer_t))

        except (IndexError, AttributeError):
            print("index out of range")

    if objects_2D_ring_buffer_x.left_index + objects_2D_ring_buffer_x.right_index == objects_2D_ring_buffer_x.maxlen:
        print("object_2D_ring_buffer has been filled")
        centroid_tracker.nextObjectID = 0

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

    imgStack = stack_images(0.8, ([img, img_results, image.color_mask]))
    # cv2.imshow("Result", imgStack)
    cv2.imshow("Contour", img_results)

    past_object_num = len(objects)

    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
