import logging
from test_flight_controller import TestFlightController
from no_op_flight_controller import NoOpFlightController
from drone import Drone
import time
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


def do_control():
    logger.info('Starting main control')
    drone = Drone()

    #TODO: Swap start_sensor_log for start() if not operting in diagnostic mode (add command line switch?)

    #drone.start();
    drone.start_sensor_log()


    #TODO: Swap controller depending on control mode (add command line switch?)
    #controller = TestFlightController(drone)
    controller = NoOpFlightController(drone)

    while True:
        # hack temp to accumulate samples
        time.sleep(10.0 / 1000)
        drone.process_sensors()
        controller.process_actions()




do_control()
