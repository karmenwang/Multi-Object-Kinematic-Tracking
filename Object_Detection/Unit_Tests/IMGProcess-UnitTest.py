import cv2
import Classes.VideoSetUp as VideoSetUp

trackBar = VideoSetUp.TrackBar()
image = VideoSetUp.IMGProcess()
image.webcam = True
image.path = '../Example_Code/shapes.png'
image.percentage = 60

while True:
    img = image.capture_image()
    imgContour = img.copy()
    image.get_canny_img(img)
    image.get_contour_img(imgContour)

    # HSV color detection
    image.get_hsv_img(img, trackBar.HSVMinMaxArray)

    cv2.imshow("Result", imgContour)

    if not image.webcam:
        cv2.waitKey(0)
    elif cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
        break
