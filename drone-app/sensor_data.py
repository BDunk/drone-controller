import logging
import math

from position_sensor_driver import PositionSensorDriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)



class SensorData(object):

    MODE_UNINITIALIZED=0
    MODE_CALIBRATING=1
    MODE_READING=2
    MODE_DEBUG=3


    def __init__(self):
        self.acceleration_position_unit = PositionSensorDriver()

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

        self.offsets=[0,0,0]

        self.mode=SensorData.MODE_UNINITIALIZED

        self.linear_scaling = 9.8

        self.angular_max=2*math.pi

        self.angular_min=0

        self.angular_scaling=2*math.pi/(self.angular_max-self.angular_min)


        self.acceleration_position_unit.flushFIFO()

    def set_debug_logging(self,should_debug_log: bool):

        self.is_debug_logging = should_debug_log
        if (should_debug_log):
            logger.setLevel(logging.DEBUG)
            self.acceleration_log = open("./accel.csv", "a+")
            self.acceleration_log.write('ax, ay, az, dt\n')
        else:
            logger.setLevel(logging.INFO)



    # what are the scaling factors we want to use in this function?
    # my assumption based on an overview of what we saw before was that it gave gyro numbers
    # that had odd bounds, and we likely want it radian
    def updating_quantities(self):
        #assigns [ax,ay,az],[rax,ray,yaz],[t]
        acceleration_position_unit = self.acceleration_position_unit
        available_batches = acceleration_position_unit.numFIFOBatches()

        if (available_batches <= 0):
            return
        
        linear_acceleration,angular_acceleration, dt = acceleration_position_unit.readFIFO(available_batches)


        # updates linear position using the velocity it believes it was travelling
        # over the period of time since acceleration was last updates
        # then updates velocity using acceleration it has just read

        #this needs to be updated to represent an earth frame rather than a drone frame
        if self.mode == SensorData.MODE_READING:
            self.process_read(linear_acceleration,angular_acceleration,dt)

        if self.mode==SensorData.MODE_DEBUG:
            self.process_debug(linear_acceleration,angular_acceleration,dt)

        if self.mode==SensorData.MODE_CALIBRATING:
            self.process_calibrate(linear_acceleration,angular_acceleration,dt)




    def process_calibrate(self, linear_acceleration, angular_acceleration,dt):
        return

    def process_read(self, linear_acceleration, angular_acceleration,dt):
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
        self.acceleration_log.write('{}, {}, {}, {}\n'.format(linear_acceleration[0], linear_acceleration[1], linear_acceleration[2], dt))