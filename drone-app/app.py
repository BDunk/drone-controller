
from test_flight_controller import TestFlightController
from no_op_flight_controller import NoOpFlightController
from drone import Drone



def do_control():

    drone = Drone()

    #TODO: Swap start_sensor_log for start() if not operting in diagnostic mode (add command line switch?)

    #drone.start();
    drone.start_sensor_log()


    #TODO: Swap controller depending on control mode (add command line switch?)
    #controller = TestFlightController(drone)
    controller = NoOpFlightController(drone)

    while True:
        drone.process_sensors()
        controller.process_actions()





