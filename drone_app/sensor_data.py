import logging
import math
import time
from vector_utils import Vector

from position_sensor_driver import PositionSensorDriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SensorDataManager:

    def calibration_complete(self):
        raise NotImplementedError()


class SensorData(object):

    MODE_UNINITIALIZED = 0
    MODE_CALIBRATING = 1
    MODE_READING = 2
    MODE_DEBUGGING = 3

    CALIBRATION_SECONDS = 2.0

    def __init__(self, sensor_manager: SensorDataManager, position_unit=None):
        if not position_unit:
            position_unit = PositionSensorDriver()

        self.sensor_manager = sensor_manager

        self.acceleration_position_unit = position_unit

        self.calibration_end_time = -1

        # all quantities except linear position require the drone to be perfectly upright,
        # stationary, and not accelerating.
        # one of the components of angular position, and all of linear position, end up
        # defined by how it is sitting on startup.
        # to remove this, we could add compass data to lock in the final angular component,
        # and we could use chips like gps to lock in two of the components of the linear position.
        # The final component of linear position, height, is difficult because of changing terrain,
        # and will be relative to starting location regardless, unless we ditch the use of calculating,
        # it, and instead we use lidar/range finder.
        # a lidar/gps or camera/gps/range finder combo could give very interesting data on both angular
        # and linear positional data in a way just accelerometer could not.

        self.linear_acceleration = [0,0,0]
        self._linear_velocity = [0, 0, 0]
        self.linear_position = [0,0,0]

        self.angular_acceleration = [0,0,0]
        self._angular_velocity = [0, 0, 0]
        self.angular_position = [0,0,0]

        self.linear_acceleration_offsets = [0, 0, 0]
        self.linear_calibration_count = 0
        self.linear_acceleration_scaling_factor=1

        self.angular_acceleration_offsets = [0, 0, 0]
        self.angular_acceleration_count = 0
        self.angular_acceleration_scaling_factor=1

        self.mode=SensorData.MODE_UNINITIALIZED

        self.linear_scaling = 9.8

        self.angular_max=2*math.pi

        self.angular_min=0

        #self.angular_scaling=2*math.pi/(self.angular_max-self.angular_min)

        self.acceleration_position_unit.flushFIFO()

    def start_debugging(self):

        self.mode = SensorData.MODE_DEBUGGING
        logger.setLevel(logging.DEBUG)

    # After calibration time has expired, the sensor manager is called with calibration ready
    def start_calibration(self):

        self.linear_acceleration_offsets = [0, 0, 0]
        self.linear_calibration_count = 0

        self.angular_acceleration_offsets = [0, 0, 0]
        self.angular_acceleration_count = 0

        self.calibration_end_time = time.time() + SensorData.CALIBRATION_SECONDS

        self.mode = SensorData.MODE_CALIBRATING

        return

    def start_reading(self):

        self.mode = SensorData.MODE_READING

        return


    def process_sensor(self):

        acceleration_position_unit = self.acceleration_position_unit
        available_batches = acceleration_position_unit.numFIFOBatches()

        if available_batches <= 0:
            return

        if available_batches >= PositionSensorDriver.MAX_BATCHES:
            logger.critical('Exceeded max buffer size, likely lost data')
            return

        linear_acceleration,angular_acceleration, dt = acceleration_position_unit.readRawAcceleration(available_batches)


        if self.mode == SensorData.MODE_READING:
            self.process_read(linear_acceleration,angular_acceleration,dt)
        elif self.mode == SensorData.MODE_DEBUGGING:
            self.process_debug(linear_acceleration,angular_acceleration,dt)
        elif self.mode == SensorData.MODE_CALIBRATING:
            self.process_calibrate(linear_acceleration,angular_acceleration,dt)
        else:
            raise RuntimeError('Processed sensor data without a specific mode')

    def get_linear_acceleration(self):
        return self.linear_acceleration

    def get_angular_acceleration(self):
        return self.angular_acceleration


    ###
    #
    # process_calibrate assumes that the device is level and not moving (e.g. on the ground)
    # It accumulates the accelerations and averages them to calibrate the sensors
    #


    def process_calibrate(self, linear_acceleration, angular_acceleration,dt):

        self.linear_acceleration_offsets, self.linear_calibration_count = self.accumulate_calibration(
            linear_acceleration,
            self.linear_acceleration_offsets,
            self.linear_calibration_count
        )

        self.angular_acceleration_offsets, self.angular_acceleration_count = self.accumulate_calibration(
            angular_acceleration,
            self.angular_acceleration_offsets,
            self.angular_acceleration_count
        )

        current_time = time.time()
        if current_time > self.calibration_end_time:
            self.sensor_manager.calibration_complete()

        return

    def accumulate_calibration(self, acceleration_batch, existing_calibration, existing_calibration_count):

        new_calibration_count = existing_calibration_count + 1
        # Negated to reflect the desired cancelling effect
        new_factor = -1 / new_calibration_count
        old_factor = ((new_calibration_count - 1) / new_calibration_count)

        new_calibration = Vector.add(
            Vector.scale(acceleration_batch, new_factor),
            Vector.scale(existing_calibration, old_factor),
        )


        return new_calibration, new_calibration_count

    def process_read(self, raw_linear_acceleration, raw_angular_acceleration, dt):

        adjusted_linear_acceleration = Vector.subtract(raw_linear_acceleration, self.linear_acceleration_offsets)

        adjusted_scaled_linear_acceleration = Vector.scale(
            adjusted_linear_acceleration,
            self.linear_acceleration_scaling_factor
        )

        adjusted_angular_acceleration = Vector.subtract(raw_angular_acceleration, self.angular_acceleration_offsets)
        adjusted_scaled_angular_acceleration = Vector.scale(
            adjusted_angular_acceleration,
            self.angular_acceleration_scaling_factor
        )


        self.linear_acceleration = adjusted_scaled_linear_acceleration
        self.angular_acceleration = adjusted_scaled_angular_acceleration

        #finds change in linear position and increments linear position by that amount
        delta_linear_position = Vector.scale(self.linear_velocity,dt)
        self.linear_position = Vector.add(self.linear_position, delta_linear_position)

        #finds change in linear velocity and increments linear velocity by that amount
        delta_linear_velocity = Vector.scale(self.linear_acceleration,dt)
        self._linear_velocity = Vector.add(self.linear_velocity,delta_linear_velocity)

        #finds change in angular position and increments angular position by that amount
        delta_angular_position = Vector.scale(self.angular_velocity,dt)
        self.angular_position = Vector.add(self.angular_position, delta_angular_position)

        #finds change in angular velocity and increments angular velocity by that amount
        delta_angular_velocity = Vector.scale(self.angular_acceleration,dt)
        self._angular_velocity = Vector.add(self.angular_velocity,delta_angular_velocity)


    def process_debug(self, linear_acceleration, angular_acceleration,dt):

        #self.acceleration_log.write('{}, {}, {}, {}\n'.format(linear_acceleration[0], linear_acceleration[1], linear_acceleration[2], dt))

        return

    @property
    def linear_velocity(self):
        return self._linear_velocity

    @property
    def angular_velocity(self):
        return self._angular_velocity
