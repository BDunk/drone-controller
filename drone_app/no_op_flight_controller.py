from drone import Drone, DroneControllerInterface
import time


class NoOpFlightController (DroneControllerInterface):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control
        self.time_to_stop = None

    def process_actions(self):
        if self.time_to_stop is None:
            return True

        if time.time() < self.time_to_stop:
            return True

        return False

    def ready(self):

        self.time_to_stop = time.time() + 5
        return


