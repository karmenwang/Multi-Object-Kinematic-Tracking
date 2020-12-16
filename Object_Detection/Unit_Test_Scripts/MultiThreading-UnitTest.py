import cv2
import logging
import threading
import time
cap = cv2.VideoCapture(0)

def thread_function(name):
    logging.info("Thread %s: starting", name)
    while True:
        success, img = cap.read()
        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xff == ord('q'):  # press q to exit
            break
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format_ = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format_, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    # x.join()
    logging.info("Main    : all done")