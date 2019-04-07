
from motor_matrix import MotorMatrix
from sensor_data import SensorData
import time


class DroneControllerInterface:

    def ready(self):
        raise NotImplementedError



class Drone (object):

    #TODO: set constant to conservative value, affects the set point targeted when passing a percent.
    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 1234

    MODE_STOPPED = 0
    MODE_SENSOR_LOG = 1
    MODE_ACTIVE = 2



    def __init__(self):
        self.is_calibrating = False
        self.calibration_end_time = -1

        self.mode = Drone.MODE_STOPPED
        self.motor_matrix = MotorMatrix()
        self.sensor_data = SensorData()




    def start_sensor_log(self, controller: DroneControllerInterface):
        self.controller = controller
        self.mode = Drone.MODE_SENSOR_LOG
        self.sensor_data.start_debugging()
        self.controller.ready()


    def start(self, controller: DroneControllerInterface):
        self.controller = controller
        self.mode = Drone.MODE_ACTIVE
        self.motor_matrix.start_your_engines()

        self.is_calibrating = True
        self.sensor_data.start_calibration()
        self.calibration_end_time = time.time() + Drone.CALIBRATION_SECONDS



    def process_sensors(self):

        # Note: This both reads from the chip and updates position information.
        # It may be more testable and clear to separate the two functions by
        # reading the sensor directly here, and passing it back into a purely functional
        # piece of code to accumulate the implications
        self.sensor_data.process_sensor()

        if self.mode == Drone.MODE_SENSOR_LOG:
            # No control functions, early return
            return

        current_time = time.time()

        if self.is_calibrating and current_time > self.calibration_end_time


        # TODO: adjust motor matrix

        # This is the magic of stability control and responding to instructions
        raise NotImplementedError


    # all of these functions have a percentage, because they will have negative percentages to move backwards
    def rise_at_rate(self, rise_percent):
        #check velocity, if velocity is not at desired rate, increase motor rate
        #check velocity, if it is changing in the wrong way, counter that
        raise NotImplementedError()


    # Note: this interface structure is likely to result in awkward movements (or I suppose we could use superposition),
    # imagine rotating in place than warlking forward rather than turning and walking smoothly
    # alternate model would be something like "desired new position" or "desired new vector"
    def forward_at_rate(self, forward_percent):

        raise NotImplementedError()

    def right_at_rate(self, right_percent):

        raise NotImplementedError()

    def yaw_right_at(self, yaw_right_percent):
        raise NotImplementedError




    def cleanup(self):
        self.motor_matrix.cleanup()
