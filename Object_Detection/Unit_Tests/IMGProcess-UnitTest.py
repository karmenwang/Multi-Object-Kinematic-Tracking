import cv2
import Classes.VideoSetUp as VideoSetUp

trackBar = VideoSetUp.TrackBar()
image = VideoSetUp.IMGProcess()
image.webcam = True
image.path = '../Resources/6.png'
image.percentage = 60

while True:
    img = image.capture_image()
    imgContour = img.copy()
    image.get_dilation_img(img)
    objectEdgePoint = image.object_edge(imgContour)

    # HSV color detection
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    # stack the different types of images together
    imgStack = VideoSetUp.stack_images(0.8, ([img, imgContour, image.colorMask]))
    cv2.imshow("Result", imgStack)

    if not image.webcam:
        cv2.waitKey(0)
    elif cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
