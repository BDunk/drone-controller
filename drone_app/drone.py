
from drone_app.motor_matrix import MotorMatrix
from drone_app.sensor_data import SensorData, SensorDataManager
from drone_app.PID import PID
import math
import time

class DroneControllerInterface:

    def ready(self):
        raise NotImplementedError



class Drone (SensorDataManager):


    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 0.5
    MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND = 0.5
    MAXIMUM_RADIANS_PER_SECOND = 2*math.pi/5


    MODE_STOPPED = 0
    MODE_SENSOR_LOG = 1
    MODE_ACTIVE_CALIBRATING = 2
    MODE_ACTIVE_CONTROLLING = 3

    #TODO: We are estimating that a 4 meter per second error (approximate speed after dropping 1 meter)
    #TODO: Should result in full control deflection
    RISE_PID_CONFIG = [1.0 / 4.0, 0, 0]

    #TODO: We are estimating that a 1 meter per second error
    #TODO: Should result in full control deflection
    TRANSLATION_PID_CONFIG =[1.0, 0, 0]

    #TODO: No estimates yet
    ROTATIONAL_CONFIG = [1.0, 0, 0]

    #Consider: what motor speed do we want to apply if the error is a particular velocity error.



    def __init__(self, position_unit=None, motor_definition=None):

        self.controller = None

        self.mode = Drone.MODE_STOPPED
        self.calibration_complete_time = None
        self.last_read_time = None

        self.motor_matrix = MotorMatrix(motor_definition=motor_definition)
        self.sensor_data = SensorData(self, position_unit=position_unit)


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
        self.mode = Drone.MODE_ACTIVE_CALIBRATING
        self.motor_matrix.start_your_engines()

        self.sensor_data.start_calibration()

    def calibration_complete(self):

        self.mode = Drone.MODE_ACTIVE_CONTROLLING
        self.last_read_time = time.time()

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
        elif self.mode == Drone.MODE_ACTIVE_CALIBRATING:
            #until calibration is complete, don't act on data
            return
        elif self.mode == Drone.MODE_ACTIVE_CONTROLLING:
            self.read_and_control()
            return
        elif self.mode == Drone.MODE_STOPPED:
            raise RuntimeError('Bad state, called process when stopped')
        else:
            raise RuntimeError('Unknown state')



    def read_and_control(self):

        read_time = time.time()

        delta_read_time = read_time - self.last_read_time
        if delta_read_time == 0:
            #skip processing when negligible timem has passed (i.e. within clock granularity)
            # pid controller should not be called with no time elapsed
            return
        self.last_read_time = read_time

        linear_velocity = self.sensor_data.linear_velocity
        angular_velocity = self.sensor_data.angular_velocity

        forward_adjust = self.forward_controller.calculate(linear_velocity[0], delta_read_time)
        translate_adjust = self.translation_controller.calculate(linear_velocity[1], delta_read_time)
        rise_adjust = self.rise_controller.calculate(linear_velocity[2], delta_read_time)
        # TODO: This assumes that the 3rd axis is yaw
        rotate_adjust = self.rotation_controller.calculate(angular_velocity[2], delta_read_time)

        # Pass values outside of range to motor matrix, as it clamps them
        self.motor_matrix.set_platform_controls(rise_adjust, forward_adjust, translate_adjust, rotate_adjust)

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
