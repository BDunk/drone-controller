from drone import Drone, DroneControllerInterface


class NoOpFlightController (DroneControllerInterface):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control

    def process_actions(self):

        return

    def ready(self):

        return


