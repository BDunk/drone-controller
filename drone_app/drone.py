
from motor_matrix import MotorMatrix
from sensor_data import SensorData, SensorDataManager
from PID import PID
import math

class DroneControllerInterface:

    def ready(self):
        raise NotImplementedError



class Drone (SensorDataManager):


    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 0.5
    MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND = 0.5
    MAXIMUM_RADIANS_PER_SECOND = 2*math.pi/5


    MODE_STOPPED = 0
    MODE_SENSOR_LOG = 1
    MODE_ACTIVE = 2

    #TODO: add PID here for control


    def __init__(self):

        self.mode = Drone.MODE_STOPPED
        self.motor_matrix = MotorMatrix()
        self.sensor_data = SensorData(self)
        self.desired_forward_velocity=0
        self.desired_right_velocity=0
        self.desired_up_velocity=0



    def start_sensor_log(self, controller: DroneControllerInterface):
        self.controller = controller
        self.mode = Drone.MODE_SENSOR_LOG
        self.sensor_data.start_debugging()
        self.controller.ready()


    def start(self, controller: DroneControllerInterface):
        self.controller = controller
        self.mode = Drone.MODE_ACTIVE
        self.motor_matrix.start_your_engines()

        self.sensor_data.start_calibration()


    def calibration_complete(self):
        self.sensor_data.start_reading()
        self.controller.ready()



    def process_sensors(self):

        # Note: This both reads from the chip and updates position information.
        # It may be more testable and clear to separate the two functions by
        # reading the sensor directly here, and passing it back into a purely functional
        # piece of code to accumulate the implications
        self.sensor_data.process_sensor()

        if self.mode == Drone.MODE_SENSOR_LOG:
            # No control functions, early return
            return

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

    def translate_right_at_rate(self, right_percent):

        raise NotImplementedError()

    def rotate_clockwise_at(self, rotate_clockwise_radians):
        raise NotImplementedError()

    def cleanup(self):
        self.motor_matrix.cleanup()
