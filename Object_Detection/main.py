import logging
import threading
import time

from KinematicTrackingThread import KinematicTrackingThread

if __name__ == "__main__":
    kinematic_tracker = KinematicTrackingThread()
    format_ = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format_, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=kinematic_tracker.get_kinematics, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    # x.join()
    logging.info("Main    : all done")