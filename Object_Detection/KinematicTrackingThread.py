# package imports (go to file > settings > project > python interpreter > + in top right > add the following:
import cv2
from numpy_ringbuffer import RingBuffer
import numpy as np
import time
import logging

# file imports
from Classes.CentroidTracker import CentroidTracker
from Classes.IMGProcess import IMGProcess
from Classes.IMGProcess import TrackBar
from Classes.IMGProcess import stack_images
from Classes.CalculateVelocity import CalculateVelocity

class KinematicTrackingThread:
    def __init__(self):
        # Constants/Initialization ######
        self._MAX_CAPACITY = 10
        self._SAMPLE_SIZE = 10
        self._LINE_COORD = [[600, 0], [600, 700]]  # [[x1,y1], [x2, y2]]

        self.objects_2D_ring_buffer_x = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)  # Create parent RB to house all X data
        self.objects_2D_ring_buffer_y = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)  # '' Y data
        self.objects_2D_ring_buffer_t = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)  # '' Time data

        self.x_velocity_array = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)  # array for collecting vectors from each sample data
        self.y_velocity_array = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)

        self.x_average_velocity_array = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)  # use x_velocity_array to create the average
        self.y_average_velocity_array = RingBuffer(capacity=self._MAX_CAPACITY, dtype=RingBuffer)

        self._created_2d_ring_buffer = False
        self._object_ID_prev_max = 0

        # Object instances #############
        self.image = IMGProcess()
        self.track_bar = TrackBar()
        self.centroid_tracker = CentroidTracker(maxCapacity=self._MAX_CAPACITY)

        # Set object parameters #########
        self.image.webcam = True
        self.image.path = 'Example_Code/Shape_Detection/shapes.png'
        self.image.percentage = 60

    def get_kinematics(self, name):
        logging.info("Thread %s: starting", name)
        while True:
            # Initializing img
            img = self.image.capture_image()
            img_results = img.copy()
            self.image.prep_contour_img(img)
            bounding_box_array = self.image.get_contour_img(img_results, self._LINE_COORD[0][0])
            self.image.get_hsv_img(img, self.track_bar.HSVMinMaxArray)

            # Draw line Threshold (arbitrary ATM)
            cv2.line(img_results, (self._LINE_COORD[0][0], self._LINE_COORD[0][1]),
                     (self._LINE_COORD[1][0], self._LINE_COORD[1][1]),(0, 0, 255), 2)

            # Get dictionary of detected objects' ID and centroid
            objects = self.centroid_tracker.update(bounding_box_array)

            # Create initial Ring Buffer indexes based on detected objects
            if not self._created_2d_ring_buffer:
                for initial_objects_detected in range(0, len(objects)):
                    self.objects_2D_ring_buffer_x.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=int))
                    self.objects_2D_ring_buffer_y.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=int))
                    self.objects_2D_ring_buffer_t.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=float))

                    self.x_velocity_array.append(RingBuffer(capacity=self._SAMPLE_SIZE - 1, dtype=float))
                    self.y_velocity_array.append(RingBuffer(capacity=self._SAMPLE_SIZE - 1, dtype=float))

                    self.x_average_velocity_array.append(RingBuffer(capacity=1, dtype=float))
                    self.y_average_velocity_array.append(RingBuffer(capacity=1, dtype=float))

                    self._created_2d_ring_buffer = True

            # Append more ring buffers as more objects are detected
            for detected_object_ID, _ in objects.items():
                if detected_object_ID > self._object_ID_prev_max:
                    for new_objects_detected in range(0, detected_object_ID - self._object_ID_prev_max):
                        self.objects_2D_ring_buffer_x.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=int))
                        self.objects_2D_ring_buffer_y.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=int))
                        self.objects_2D_ring_buffer_t.append(RingBuffer(capacity=self._SAMPLE_SIZE, dtype=float))

                        self.x_velocity_array.append(RingBuffer(capacity=self._SAMPLE_SIZE - 1, dtype=float))
                        self.y_velocity_array.append(RingBuffer(capacity=self._SAMPLE_SIZE - 1, dtype=float))

                        self.x_average_velocity_array.append(RingBuffer(capacity=1, dtype=float))
                        self.y_average_velocity_array.append(RingBuffer(capacity=1, dtype=float))

                    self._object_ID_prev_max = detected_object_ID

            # Clear ring buffers for objects that have disappeared
            if not self.centroid_tracker.cleared_disappeared_objects_ring_buffer:
                for object_index in range(0, len(self.objects_2D_ring_buffer_x)):
                    if object_index in self.centroid_tracker.disappeared_objects:
                        try:
                            for child_ring_buffer_index in range(0, self._SAMPLE_SIZE):  # Iterate through child ring buffer to clear values
                                self.objects_2D_ring_buffer_x[object_index].pop()
                                self.objects_2D_ring_buffer_y[object_index].pop()
                                self.objects_2D_ring_buffer_t[object_index].pop()

                                if child_ring_buffer_index < self._SAMPLE_SIZE-1:     # _velocity_array has a capacity of SAMPLE_SIZE-1
                                    self.x_velocity_array[object_index].pop()
                                    self.y_velocity_array[object_index].pop()

                                if child_ring_buffer_index == 0:    # _average_velocity has capacity of 1
                                    self.x_average_velocity_array[object_index].pop()
                                    self.y_average_velocity_array[object_index].pop()

                        except IndexError:
                            print("index " + str(object_index) + " already cleared")
                self.centroid_tracker.cleared_disappeared_objects_ring_buffer = True

            for (object_ID, centroid) in objects.items():
                # draw both the ID of the object and the centroid
                cv2.putText(img_results, "ID {}".format(object_ID), (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(img_results, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

                # Store centroid points into child ring buffer for respective objects
                self.objects_2D_ring_buffer_x[object_ID].append(centroid[0])
                self.objects_2D_ring_buffer_y[object_ID].append(centroid[1])
                self.objects_2D_ring_buffer_t[object_ID].append(time.monotonic())  # time is in seconds

            # Manages when ID number go above the Max capacity
            if self.objects_2D_ring_buffer_x.right_index == self.objects_2D_ring_buffer_x.maxlen:
                self.centroid_tracker.nextObjectID = self.centroid_tracker.nextObjectID % self._MAX_CAPACITY

            print("detected objects" + str(objects) + " " + "disappeared objects" + str(self.centroid_tracker.disappeared_objects))
            print(" ")
            print("x sample array" + str(self.objects_2D_ring_buffer_x))
            print(" ")
            print("time sample array" + str(self.objects_2D_ring_buffer_t))
            print(" ")

            # Calculate Vectors using the most recent 2 data points
            for vector_object_index in range(0, len(self.objects_2D_ring_buffer_x)):
                x_vector = CalculateVelocity(
                    self.objects_2D_ring_buffer_x[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 2],
                    self.objects_2D_ring_buffer_x[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 1],
                    self.objects_2D_ring_buffer_t[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 2],
                    self.objects_2D_ring_buffer_t[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 1])
                y_vector = CalculateVelocity(
                    self.objects_2D_ring_buffer_y[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 2],
                    self.objects_2D_ring_buffer_y[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 1],
                    self.objects_2D_ring_buffer_t[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 2],
                    self.objects_2D_ring_buffer_t[vector_object_index][len(self.objects_2D_ring_buffer_x[vector_object_index]) - 1])

                if len(self.objects_2D_ring_buffer_x[vector_object_index]) > 1:  # wait for at least 2 data points
                    self.x_velocity_array[vector_object_index].append('%.3f' % x_vector.get_velocity_vector())   # truncate to 3 decimal points
                    self.y_velocity_array[vector_object_index].append('%.3f' % y_vector.get_velocity_vector())

            print("x velocity array" + str(self.x_velocity_array) + " pixels/seconds")
            print("y velocity array" + str(self.y_velocity_array) + " pixels/seconds")
            print(" ")

            # Calculate Vector Average using numpy average
            for velocity_average_object_index in range(0, len(self.objects_2D_ring_buffer_x)):
                self.x_average_velocity_array[velocity_average_object_index].append('%.3f' % np.average(self.x_velocity_array[velocity_average_object_index]))
                self.y_average_velocity_array[velocity_average_object_index].append('%.3f' % np.average(self.y_velocity_array[velocity_average_object_index]))

            print("x average velocity array" + str(self.x_average_velocity_array))
            print("y average velocity array" + str(self.y_average_velocity_array))
            print(" ")

            imgStack = stack_images(0.8, ([img, img_results, self.image.color_mask]))
            # cv2.imshow("Result", imgStack)
            cv2.imshow("Contour", img_results)

            if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
                break
        logging.info("Thread %s: finishing", name)
