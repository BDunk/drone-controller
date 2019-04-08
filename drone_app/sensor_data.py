import logging
import math
import time
from .vector_utils import Vector

from .position_sensor_driver import PositionSensorDriver

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

    def __init__(self, sensor_manager: SensorDataManager, position_unit=PositionSensorDriver()):
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
        self.linear_velocity = [0,0,0]
        self.linear_position = [0,0,0]

        self.angular_acceleration = [0,0,0]
        self.angular_velocity = [0,0,0]
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


    ##
    # proccess_calibrate assumes that the device is level and not moving (e.g. on the ground)
    # It accumulates the accelerations and averages them to calibrate the sensors

    def process_calibrate(self, linear_acceleration, angular_acceleration,dt):


        self.linear_acceleration_offsets, self.linear_calibration_count  = self.accumulate_calibration(
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

    def accumulate_calibration(self, acceleration_batches, existing_calibration, existing_calibration_count):
        for acceleration_batch in acceleration_batches:
            existing_calibration_count += 1
            existing_calibration = [
                acceleration_batch[0] * (1 / existing_calibration_count) + existing_calibration[0],
                acceleration_batch[1] * (1 / existing_calibration_count) + existing_calibration[1],
                acceleration_batch[2] * (1 / existing_calibration_count) + existing_calibration[2],
            ]
        return existing_calibration, existing_calibration_count

    def process_read(self, linear_acceleration, angular_acceleration,dt):

        adjusted_linear_acceleration = Vector.add(linear_acceleration, self.linear_acceleration_offsets)
        adjusted_scaled_linear_acceleration = Vector.scale(adjusted_linear_acceleration, self.linear_acceleration_scaling_factor)

        adjusted_angular_acceleration = Vector.add(angular_acceleration, self.angular_acceleration_offsets)
        adjusted_scaled_angular_acceleration = Vector.scale(adjusted_angular_acceleration, self.angular_acceleration_offsets)


        self.linear_acceleration = adjusted_scaled_linear_acceleration
        self.angular_acceleration = adjusted_scaled_angular_acceleration


        self.linear_acceleration=[a_components*self.linear_acceleration_scaling_factor for a_components in self.linear_acceleration]

        self.angular_acceleration=[sum(a_components) for a_components in zip(self.angular_acceleration,self.angular_acceleration_offsets)]
        self.angular_acceleration=[a_components*self.angular_acceleration_scaling_factor for a_components in self.angular_acceleration]

        delta_linear_position = [v_component * dt for v_component in self.linear_velocity]

        self.linear_position = [sum(p_component) for p_component in zip(self.linear_position, delta_linear_position)]

        delta_linear_velocity = [a_component * dt for a_component in linear_acceleration]

        self.linear_velocity = [sum(v_component) for v_component in zip(self.linear_velocity, delta_linear_velocity)]

        # same function as lines above, but updating rotation
        delta_angular_position = [v_component * dt for v_component in self.angular_velocity]

        self.angular_position = [sum(p_component) for p_component in zip(self.angular_position, delta_angular_position)]

        delta_angular_velocity = [a_component * dt for a_component in angular_acceleration]

        self.angular_velocity = [sum(v_component) for v_component in zip(self.angular_velocity, delta_angular_velocity)]

    def process_debug(self, linear_acceleration, angular_acceleration,dt):

        #self.acceleration_log.write('{}, {}, {}, {}\n'.format(linear_acceleration[0], linear_acceleration[1], linear_acceleration[2], dt))

        return
