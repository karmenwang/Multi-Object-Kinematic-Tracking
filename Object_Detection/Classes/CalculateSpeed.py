class CalculateSpeed:

    def __init__(self, lastPoint, current_point, lastPoint_time, current_point_time):
        self.current_point = current_point
        self.last_point = lastPoint
        self.last_point_time = lastPoint_time
        self.current_point_time = current_point_time

    def get_velocity_vector(self):
        position_vector = self.current_point - self.last_point  # position vector = final - initial
        time_passed = (self.current_point_time - self.last_point_time)
        if time_passed == 0:
            time_passed = 0.001  # assume 1 microsecond has passed if no time has passed
        velocity_vector = position_vector / time_passed    # (pos final - pos initial)/(T final-T initial)

        return velocity_vector
