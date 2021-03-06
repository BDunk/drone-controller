
from motor_matrix import MotorMatrix
from sensor_data import SensorData, SensorDataManager
from PID import PID
import math
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

class DroneControllerInterface:

    def ready(self):
        raise NotImplementedError



class Drone (SensorDataManager):


    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 1.0
    MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND = 0.5
    MAXIMUM_RADIANS_PER_SECOND = 2*math.pi/5


    MODE_STOPPED = 0
    MODE_SENSOR_LOG = 1
    MODE_ACTIVE_CALIBRATING = 2
    MODE_ACTIVE_CONTROLLING = 3
    MODE_TESTING = 4

    FORWARD_AXIS_INDEX = 0
    RIGHTWARD_AXIS_INDEX = 1
    UPWARD_AXIS_INDEX = 2
    YAW_RIGHTWARD_INDEX = 2

    FORWARD_INVERSION_FACTOR = -1
    RIGHTWARD_INVERSION_FACTOR = 1
    UPWARD_INVERSION_FACTOR = -1
    YAW_RIGHTWARD_FACTOR = -1

    #TODO: We are estimating that a 1 meter per second error
    #TODO: Should result in full control deflection
    RISE_PID_CONFIG = [1.0, 0, 0]

    #TODO: We are estimating that a 10 meter per second error
    #TODO: Should result in full control deflection
    TRANSLATION_PID_CONFIG =[1.0/10, 0, 0]

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
        self.stop_motor_test_time = None


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

    #diagnostic used to see what direction motors are spinning
    def start_motor_test(self,  controller: DroneControllerInterface):
        self.controller = controller
        self.mode = Drone.MODE_TESTING
        self.motor_matrix.start_your_engines()

        self.sensor_data.start_debugging()

        self.motor_matrix.set_platform_controls(0, 0, 0, 0)
        self.controller.ready()


    def start(self, controller: DroneControllerInterface):

        self.controller = controller
        self.mode = Drone.MODE_ACTIVE_CALIBRATING
        self.motor_matrix.start_your_engines()

        self.velocity_and_control = open("velocity_and_control.csv", "w+")
        self.velocity_and_control.write('delta_read_time, '
                                        'forward_velocity, '
                                        'forward_adjust,'
                                        'rightward_velocity, '
                                        'rightward_adjust, '
                                        'upward_velocity, '
                                        'upward_adjust, '
                                        'rotate_velocity, '
                                        'rotate_adjust,\n')

        self.sensor_data.start_calibration()

    def calibration_complete(self):

        logger.critical("Calibration Complete")
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
        elif self.mode == Drone.MODE_TESTING:
            # nothing require for test
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

        forward_velocity = Drone.FORWARD_INVERSION_FACTOR*linear_velocity[Drone.FORWARD_AXIS_INDEX]
        forward_adjust = self.forward_controller.calculate(forward_velocity, delta_read_time)

        rightward_velocity = Drone.RIGHTWARD_INVERSION_FACTOR*linear_velocity[Drone.RIGHTWARD_AXIS_INDEX]
        rightward_adjust = self.translation_controller.calculate(rightward_velocity, delta_read_time)

        upward_velocity = Drone.UPWARD_INVERSION_FACTOR*linear_velocity[Drone.UPWARD_AXIS_INDEX]
        upward_adjust = self.rise_controller.calculate(upward_velocity, delta_read_time)

        rotate_velocity = Drone.YAW_RIGHTWARD_FACTOR*angular_velocity[Drone.YAW_RIGHTWARD_INDEX]
        rotate_adjust = self.rotation_controller.calculate(rotate_velocity, delta_read_time)

        self.velocity_and_control.write('{}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(
            delta_read_time,
            forward_velocity,
            forward_adjust,
            rightward_velocity,
            rightward_adjust,
            upward_velocity,
            upward_adjust,
            rotate_velocity,
            rotate_adjust,
        ))

        # Pass values outside of range to motor matrix, as it clamps them
        self.motor_matrix.set_platform_controls(upward_adjust, forward_adjust, rightward_adjust, rotate_adjust)

    def rise_at_rate(self, rise_normalized):

        rise_normalized = min(1, max(-1, rise_normalized))
        desired_up_velocity = rise_normalized * Drone.MAXIMUM_RISE_RATE_METERS_PER_SECOND
        self.rise_controller.change_set_point(desired_up_velocity)
        logger.critical("Rise value of {}".format(desired_up_velocity))

    def forward_at_rate(self, forward_normalized):

        forward_normalized = min(1, max(-1, forward_normalized))
        desired_forward_velocity = forward_normalized * Drone.MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND
        self.forward_controller.change_set_point(desired_forward_velocity)

    def translate_right_at_rate(self, right_normalized):

        right_normalized = min(1, max(-1, right_normalized))
        desired_right_velocity = right_normalized * Drone.MAXIMUM_TRANSLATE_RATE_METERS_PER_SECOND
        self.translation_controller.change_set_point(desired_right_velocity)

    def rotate_clockwise_at(self, clockwise_percent):

        pass
        # Don't permit rotation other than zero

        #clockwise_percent = min(-1, max(1, clockwise_percent))
        #desired_clockwise_velocity = clockwise_percent * Drone.MAXIMUM_RADIANS_PER_SECOND
        #self.rotation_controller.change_set_point(desired_clockwise_velocity)


    def direct_motor_test(
            self,
            fl_normalized: float,
            fr_normalized: float,
            br_normalized: float,
            bl_normalized: float):

        self.motor_matrix.direct_test(fl_normalized, fr_normalized, br_normalized, bl_normalized)

    def cleanup(self):
        self.motor_matrix.cleanup()
