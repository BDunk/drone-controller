
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

    TRANSLATION_PID_CONFIG =[1.0, 0, 0]
    RISE_PID_CONFIG = [1.0, 0, 0]
    ROTATIONAL_CONFIG = [1.0, 0, 0]

    TRANSLATION_MAX_ADJUST = 4
    RISE_MAX_ADJUST = 100
    ROTATION_MAX_ADJUST = 100



    def __init__(self):

        self.controller = None

        self.mode = Drone.MODE_STOPPED
        self.motor_matrix = MotorMatrix()
        self.sensor_data = SensorData(self)


        self.forward_controller = PID(
            Drone.TRANSLATION_PID_CONFIG[0],
            Drone.TRANSLATION_PID_CONFIG[1],
            Drone.TRANSLATION_PID_CONFIG[2],
        )
        self.translation_controller = PID(
            Drone.TRANSLATION_PID_CONFIG[0],
            Drone.TRANSLATION_PID_CONFIG[1],
            Drone.TRANSLATION_PID_CONFIG[2],
        )
        self.rise_controller = PID(
            Drone.RISE_PID_CONFIG[0],
            Drone.RISE_PID_CONFIG[1],
            Drone.RISE_PID_CONFIG[2],
        )
        self.rotation_controller = PID(
            Drone.ROTATIONAL_CONFIG[0],
            Drone.ROTATIONAL_CONFIG[1],
            Drone.ROTATIONAL_CONFIG[2],
        )

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

        linear_velocity = self.sensor_data.linear_velocity
        angular_velocity = self.sensor_data.angular_velocity

        self.forward_controller.change_current_point(linear_velocity[0])
        self.translation_controller.change_current_point(linear_velocity[1])
        self.rise_controller.change_current_point(linear_velocity[3])

        #TODO: This assumes that the z axis is yaw, and also doesn't directly force other rotations to zero.
        self.rotation_controller.change_current_point(angular_velocity[3])

        forward_adjust = self.forward_controller.calculate() / Drone.TRANSLATION_MAX_ADJUST
        translate_adjust = self.translation_controller.calculate() / Drone.TRANSLATION_MAX_ADJUST
        rise_adjust = self.rise_controller.calculate() / Drone.RISE_MAX_ADJUST

        rotate_adjust = self.rotation_controller.calculate() / Drone.ROTATION_MAX_ADJUST

        # Pass values outside of range to motor matrix, as it clamps them

        self.motor_matrix.pitch_forward(forward_adjust)
        self.motor_matrix.roll_right(translate_adjust)
        self.motor_matrix.rise(rise_adjust)
        self.motor_matrix.yaw_clockwise(rotate_adjust)


    def rise_at_rate(self, rise_normalized):

        rise_normalized = min(-1, max(1, rise_normalized))
        desired_up_velocity = rise_normalized * Drone.MAXIMUM_RISE_RATE_METERS_PER_SECOND
        self.rise_controller.change_set_point(desired_up_velocity)

    def forward_at_rate(self, forward_normalized):

        forward_normalized = min(-1, max(1, forward_normalized))
        desired_forward_velocity = forward_normalized * Drone.MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND
        self.forward_controller.change_set_point(desired_forward_velocity)

    def translate_right_at_rate(self, right_normalized):

        right_normalized = min(-1, max(1, right_normalized))
        desired_right_velocity = right_normalized * Drone.MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND
        self.translation_controller.change_set_point(desired_right_velocity)

    def rotate_clockwise_at(self, clockwise_percent):

        pass
        # Don't permit rotation other than zero

        #clockwise_percent = min(-1, max(1, clockwise_percent))
        #desired_clockwise_velocity = clockwise_percent * Drone.MAXIMUM_RADIANS_PER_SECOND
        #self.rotation_controller.change_set_point(desired_clockwise_velocity)



    def cleanup(self):
        self.motor_matrix.cleanup()
