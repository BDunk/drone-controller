from motor import Motor
import logging

logger = logging.getLogger()

logger.setLevel(logging.ERROR)

# NOTE design choice: this class is passively attempting to accomplish the rotations pitch requested.
# External logic must be sensing and requesting adjustments.
#Pinout diagram found here: https://www.codecubix.eu/index.php/2018/05/29/hardware-pwm-with-raspberry-pi-zero/


class MotorDefinition:
    def __init__(self, front_left, front_right, back_left, back_right):
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right



class MotorMatrix(object):
    # NOTE: this could a config file or whatever, coded in this class for now
    # Todo: get pinouts decided
    FRONT_LEFT_PIN = 12
    FRONT_RIGHT_PIN = 18
    BACK_LEFT_PIN = 13
    BACK_RIGHT_PIN = 19

    TRANSLATION_GAIN = 1/10

    FL = 0
    FR = 1
    BL = 2
    BR = 3

    ALL = [FL, FR, BL, BR]
    FRONT_ARRAY = [FL, FR]
    BACK_ARRAY = [BL, BR]
    LEFT_ARRAY = [FL, BL]
    RIGHT_ARRAY = [FR, BR]

    CLOCKWISE_ARRAY = [FR, BL] # Clockwise rotating motors
    ANTICLOCKWISE_ARRAY = [FL, BR]

    def __init__(self, motor_definition:MotorDefinition = None):
        #NOTE: this is very static code, may be better to loop and calculuate these, or subclass to isolate motor

        if not motor_definition:
            self.front_left = Motor(MotorMatrix.FRONT_LEFT_PIN)
            self.front_right = Motor(MotorMatrix.FRONT_RIGHT_PIN)
            self.back_left = Motor(MotorMatrix.BACK_LEFT_PIN)
            self.back_right = Motor(MotorMatrix.BACK_RIGHT_PIN)
        else:
            self.front_left = motor_definition.front_left
            self.front_right = motor_definition.front_right
            self.back_left = motor_definition.back_left
            self.back_right = motor_definition.back_right



        # Must be aligned with MotorMatrix.ALL
        self.all = [self.front_left, self.front_right, self.back_left, self.back_right,]



    def start_your_engines(self):

        for motor in self.all:
            motor.start()

    def set_platform_controls(
        self,
        rise_normalized: float,
        forward_normalized: float,
        roll_right_normalized: float,
        yaw_clockwise_normalized: float
    ):

        buffer_speeds = [0.0, 0.0, 0.0, 0.0]

        for motor_index in MotorMatrix.ALL:
            buffer_speeds[motor_index] = rise_normalized

        for motor_index in MotorMatrix.FRONT_ARRAY:
            buffer_speeds[motor_index] -= MotorMatrix.TRANSLATION_GAIN * forward_normalized
        for motor_index in MotorMatrix.BACK_ARRAY:
            buffer_speeds[motor_index] += MotorMatrix.TRANSLATION_GAIN * forward_normalized

        for motor_index in MotorMatrix.RIGHT_ARRAY:
            buffer_speeds[motor_index] -= MotorMatrix.TRANSLATION_GAIN * roll_right_normalized
        for motor_index in MotorMatrix.LEFT_ARRAY:
            buffer_speeds[motor_index] += MotorMatrix.TRANSLATION_GAIN * roll_right_normalized

        for motor_index in MotorMatrix.CLOCKWISE_ARRAY:
            buffer_speeds[motor_index] -= MotorMatrix.TRANSLATION_GAIN * yaw_clockwise_normalized
        for motor_index in MotorMatrix.ANTICLOCKWISE_ARRAY:
            buffer_speeds[motor_index] += MotorMatrix.TRANSLATION_GAIN * yaw_clockwise_normalized

        logger.critical("Buffer speeds FL {} FR {} BR {} BL {}".format(
            buffer_speeds[0],
            buffer_speeds[1],
            buffer_speeds[2],
            buffer_speeds[3],
        ))

        for motor_index in MotorMatrix.ALL:
            motor = self.all[motor_index]
            desired_speed = buffer_speeds[motor_index]
            desired_speed = min(1.0, max(-1.0, desired_speed))

            translated_postive = desired_speed + 1
            scaled_to_percent = (translated_postive/ 2) * 100
            logger.critical("Motor speed index {} value of {}".format(motor_index, scaled_to_percent))
            motor.update_speed(scaled_to_percent)

    def direct_test(
            self,
            fl_normalized: float,
            fr_normalized: float,
            br_normalized: float,
            bl_normalized: float,
        ):

        self.front_left.update_speed(fl_normalized * 100)
        self.front_right.update_speed(fr_normalized * 100)
        self.back_right.update_speed(br_normalized * 100)
        self.back_left.update_speed(bl_normalized * 100)

    def cleanup(self):


        for motor in self.all:
            motor.stop()

        Motor.cleanup_all_motors()

