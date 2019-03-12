from motor import Motor


# NOTE design choice: this class is passively attempting to accomplish the rotations pitch requested.
# External logic must be sensing and requesting adjustments.
#Pinout diagram found here: https://www.codecubix.eu/index.php/2018/05/29/hardware-pwm-with-raspberry-pi-zero/


class MotorMatrix(object):
    # NOTE: this could a config file or whatever, coded in this class for now
    # Todo: get pinouts decided
    FRONT_LEFT_PIN = 12
    FRONT_RIGHT_PIN = 18
    BACK_LEFT_PIN = 13
    BACK_RIGHT_PIN = 19

    def __init__(self):
        #NOTE: this is very static code, may be better to loop and calculuate these, or subclass to isolate motor

        self.front_left = Motor(MotorMatrix.FRONT_LEFT_PIN)
        self.front_right = Motor(MotorMatrix.FRONT_RIGHT_PIN)
        self.back_left = Motor(MotorMatrix.BACK_LEFT_PIN)
        self.back_right = Motor(MotorMatrix.BACK_RIGHT_PIN)

        self.front_array = [self.front_left, self.front_right]
        self.back_array = [self.back_left, self.back_right]
        self.left_array = [self.front_left, self.back_left]
        self.right_array = [self.front_right, self.back_right]
        # NOTE: a special calibration item: clockwise and counter clockwise motors on the correct diagonals
        self.clockwise_motors = [self.front_right, self.back_right]
        self.anticlockwise_motors = [self.front_left, self.back_left]

        self.all = [self.front_left, self.front_right, self.back_right, self.back_left]

    def start_your_engines(self):

        # Todo: loop through all motors, calling start
        raise NotImplementedError

    #Todo: define something that runs on a loop that just stabilizes the drone
    #Todo: decide how it chooses to recover from a given stimulus
    #Todo: decide how it determines whether it should yaw then pitch, or pitch and roll?
    #Todo: define fundamental control operation in addition to rotation; pitch? roll?
    #Todo: is something special required to deal with oriented inversion? how to sum effects?
    def rotate(self, percent_max_positive_clockwise:float):

        # Todo: figure out if there is a maximum rotation that needs to be calibrated.
        raise NotImplementedError



    def cleanup(self):
        # Todo: loop and stop all motors and cleanup (question: how to confirm started?)
        raise NotImplementedError


