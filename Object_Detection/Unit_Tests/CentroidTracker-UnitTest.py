# import the necessary packages
from Classes.CentroidTracker import CentroidTracker
import Classes.IMGProcess as VideoSetUp
import cv2

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)
image = VideoSetUp.IMGProcess()

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")

# loop over the frames from the video stream
while True:
    img = image.capture_image()
    imgContour = img.copy()
    image.prep_contour_img(img)

    rects = []

    rects = image.get_bbox(imgContour)
    print(rects)

    # update our centroid tracker using the computed set of bounding
    # box rectangles
    objects = ct.update(rects)

    # loop over the tracked objects
    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        text = "ID {}".format(objectID)
        cv2.putText(imgContour, text, (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(imgContour, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

    # show the output frame
    cv2.imshow("Frame", imgContour)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
