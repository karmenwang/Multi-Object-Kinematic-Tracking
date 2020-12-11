# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2
from numpy_ringbuffer import RingBuffer
import numpy as np
import time

# file imports
from Classes.CentroidTracker import CentroidTracker
from Classes.IMGProcess import IMGProcess
from Classes.IMGProcess import TrackBar
from Classes.IMGProcess import stack_images
from Classes.Scheduler import Scheduler
from Classes.CalculateSpeed import CalculateSpeed

# Constants/Initialization ######
MAX_CAPACITY = 10
SAMPLE_SIZE = 5
LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]
TIME_INTERVAL = 0.000001

objects_2D_ring_buffer_x = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)  # Create parent RB to house all X data
objects_2D_ring_buffer_y = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)  # '' Y data
objects_2D_ring_buffer_t = RingBuffer(capacity=MAX_CAPACITY, dtype=RingBuffer)  # '' Time data

xVelocityArray = []*MAX_CAPACITY
yVelocityArray = []*MAX_CAPACITY
xVector = 0
yVector = 0
created_2d_ring_buffer = False
object_ID_prev_max = 0

# Object instances #############
image = IMGProcess()
object_scheduler = Scheduler()
track_bar = TrackBar()
centroid_tracker = CentroidTracker(maxCapacity=MAX_CAPACITY)
# calculate_x_average = CalculateAverage()
# calculate_y_average = CalculateAverage()
# calculate_t_average = CalculateAverage()

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

    # Get dictionary of detected objects' ID and centroid
    try:
        objects = centroid_tracker.update(bounding_box_array)
    except RuntimeError:
        print("OrderedDict mutated during iteration")

    # Create initial Ring Buffer indexes based on detected objects
    if not created_2d_ring_buffer:
        for objects_detected in range(0, len(bounding_box_array)):
            objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_y.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            objects_2D_ring_buffer_t.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            created_2d_ring_buffer = True

    # Append more ring buffers as more objects are detected
    for object_ID, _ in objects.items():
        if object_ID > object_ID_prev_max:
            for new_objects_detected in range(0, object_ID - object_ID_prev_max):
                objects_2D_ring_buffer_x.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
                objects_2D_ring_buffer_y.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
                objects_2D_ring_buffer_t.append(RingBuffer(capacity=SAMPLE_SIZE, dtype=int))
            object_ID_prev_max = object_ID

    # Clear ring buffers for objects that have disappeared
    if not centroid_tracker.cleared_disappeared_objects_ring_buffer:
        for object_index in range(0, len(objects_2D_ring_buffer_x)):
            try:
                for index in range(0, SAMPLE_SIZE):     # Iterate through child ring buffer to clear values
                    if index in centroid_tracker.disappeared_objects:
                        objects_2D_ring_buffer_x[object_index].pop()
                        objects_2D_ring_buffer_y[object_index].pop()
                        objects_2D_ring_buffer_t[object_index].pop()
            except IndexError:
                print("index " + str(index) + " already cleared")
        centroid_tracker.cleared_disappeared_objects_ring_buffer = True

    for (object_ID, centroid) in objects.items():
        # draw both the ID of the object and the centroid
        cv2.putText(img_results, "ID {}".format(object_ID), (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(img_results, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Store centroid points into child ring buffer for respective objects
        objects_2D_ring_buffer_x[object_ID].append(centroid[0])
        objects_2D_ring_buffer_y[object_ID].append(centroid[1])
        objects_2D_ring_buffer_t[object_ID].append(time.time())

    # Manages when ID number go above the Max capacity
    if objects_2D_ring_buffer_x._right_index == objects_2D_ring_buffer_x.maxlen:
        centroid_tracker.nextObjectID = centroid_tracker.nextObjectID % MAX_CAPACITY

    print("detected objects" + str(objects))
    print("results x array" + str(objects_2D_ring_buffer_x))

    # Calculate Vectors
    for vector_object_index_number in range(0, len(objects_2D_ring_buffer_x)):
        try:
            xVector = CalculateSpeed(objects_2D_ring_buffer_x[vector_object_index_number][len(objects_2D_ring_buffer_x[object_ID]) - 2],
                                     objects_2D_ring_buffer_x[vector_object_index_number][len(objects_2D_ring_buffer_x[object_ID]) - 1],
                                     objects_2D_ring_buffer_t[vector_object_index_number][len(objects_2D_ring_buffer_x[object_ID]) - 2],
                                     objects_2D_ring_buffer_t[vector_object_index_number][len(objects_2D_ring_buffer_x[object_ID]) - 1])
        #     # yVector = CalculateSpeed(self.yPosSampleArray[self.yMovingAverage.sample_number - 2],
        #     #                               self.yPosSampleArray[self.yMovingAverage.sample_number - 1],
        #     #                               self.timeSampleArray[self.tMovingAverage.sample_number - 2],
        #     #                               self.timeSampleArray[self.tMovingAverage.sample_number - 1])
        #
            # xVelocityArray.append(xVector.get_velocity_vector())
            # print(xVelocityArray)
            # yVelocityArray.append(self.yVector.get_velocity_vector())
        except (TypeError, IndexError):
            print("wait for more data points")



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

    if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
