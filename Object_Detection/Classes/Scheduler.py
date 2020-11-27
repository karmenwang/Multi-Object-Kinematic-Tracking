import sched
import time


class Scheduler:
    def __init__(self):
        if not self.scheduler:
            self.scheduler = sched.scheduler(time.time, time.sleep)
    scheduler = None
