from drone import Drone


class NoOpFlightController (object):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control

    def process_actions(self):

        return

