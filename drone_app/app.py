import logging
from test_flight_controller import TestFlightController
from no_op_flight_controller import NoOpFlightController
from test_motor_controller import TestMotorController
from drone import Drone
import time
import sys

#TODO: should use command line flags, not copying and pasting/ uncommenting

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.WARNING)


def do_control():
    logger.info('Starting main control')
    harpoon_lagoon = Drone()



    #TODO: Swap controller depending on control mode (add command line switch?)
    #controller = TestFlightController(harpoon_lagoon)
    #controller = TestMotorController(harpoon_lagoon)
    controller = NoOpFlightController(harpoon_lagoon)

    #TODO: Swap start_sensor_log for start() if not operting in diagnostic mode (add command line switch?)
    harpoon_lagoon.start(controller)


    still_controlling = True

    while still_controlling:
        harpoon_lagoon.process_sensors()
        still_controlling = controller.process_actions()

    harpoon_lagoon.cleanup()

do_control()
