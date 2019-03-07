
from test_flight_controller import TestFlightController
from drone import Drone


def do_control():

    drone = Drone()
    controller = TestFlightController(drone)

    while True:
        drone.process_sensors()
        controller.process_actions()





