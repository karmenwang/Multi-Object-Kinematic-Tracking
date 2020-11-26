import cv2
import numpy as np
import imutils


def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        # hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                         scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def empty():
    pass


class TrackBar:
    def __init__(self):
        # create track bars
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 640, 240)
        cv2.createTrackbar("Threshold1", "Parameters", 50, 255, empty)
        cv2.createTrackbar("Threshold2", "Parameters", 50, 255, empty)
        cv2.createTrackbar("Area", "Parameters", 500, 30000, empty)

        cv2.namedWindow("HSV")
        cv2.resizeWindow("HSV", 640, 240)
        cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
        cv2.createTrackbar("HUE Max", "HSV", 57, 179, empty)
        cv2.createTrackbar("SAT Min", "HSV", 25, 255, empty)
        cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
        cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
        cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

    @property
    def HSVMinMaxArray(self):
        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

        HSVMinMaxArray = [[h_min, s_min, v_min], [h_max, s_max, v_max]]
        return HSVMinMaxArray


class IMGProcess:
    def __init__(self, webcam=True, path=None, percentage=100):
        self.webcam = webcam
        self.path = path
        self.cap = cv2.VideoCapture(1)
        self.percentage = percentage

        self.cap.set(10, 160)  # brightness
        self.cap.set(3, 1920)  # width
        self.cap.set(4, 1080)  # height
        # self.cap.set(5, 60)  # set frame rate

        self.imgDilation = 0
        self.colorMask = 0
        self.imgCanny = 0
        self.img_thresh = 0

    def capture_image(self):
        if self.webcam:
            success, img = self.cap.read()
        else:
            img = cv2.imread(self.path)

        width = int(img.shape[1] * self.percentage / 100)
        img_resized = imutils.resize(img, width=width)
        return img_resized

    def prep_contour_img(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

        threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")  # Lower threshold bound
        threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")  # Upper threshold bound
        self.imgCanny = cv2.Canny(img_blur_gray, threshold1, threshold2)
        # consider adding a kernel & dilation or morph to rid noise (will need to tune to see if necessary)

    def get_contour_img(self, img_contour, line_coord):
        contours, hierarchy = cv2.findContours(self.imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                cv2.drawContours(img_contour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                object_edge = (x + w, y + (h // 2))  # (right most point, center)
                cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if object_edge[0] >= line_coord:  # if object has crossed threshold along x
                    cv2.circle(img_contour, object_edge, 5, (0, 255, 0), cv2.FILLED)  # Edge point dot will turn green
                else:
                    cv2.circle(img_contour, object_edge, 5, (0, 0, 255), cv2.FILLED)  # Edge point dot will turn red

    def get_hsv_img(self, img, HSVArray):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert BGR to HSV
        lower = np.array(HSVArray[0])  # lower bound
        upper = np.array(HSVArray[1])  # upper bound
        mask = cv2.inRange(imgHSV, lower, upper)
        self.colorMask = cv2.bitwise_and(img, img, mask=mask)
        # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    def object_edge(self, imgContour):
        contours, hierarchy = cv2.findContours(self.imgCanny, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)  # Use edge detection map img
        for cnt in contours:
            area = cv2.contourArea(cnt)
            areaMin = cv2.getTrackbarPos("Area", "Parameters")  # Min area set by trackbar
            if area > areaMin:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 2)
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                x, y, w, h = cv2.boundingRect(approx)  # Find bounding box
                object_edge = (x + w, y + (h // 2))  # (right most point, center)

                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(imgContour, "w={},h={}".format(w, h), (x - 175, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (36, 255, 12), 2)
                return object_edge
