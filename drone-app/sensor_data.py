import logging

from position_sensor_driver import PositionSensorDriver

logger = logging.getLogger()
logger.setLevel(logging.INFO)



class SensorData(object):

    def __init__(self):
        self.chip=PositionSensorDriver()

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

        self.dt=0

    def set_debug_logging(self,should_debug_log: bool):

        self.is_debug_logging = should_debug_log
        if (should_debug_log):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)


    # what are the scaling factors we want to use in this function?
    # my assumption based on an overview of what we saw before was that it gave gyro numbers
    # that had odd bounds, and we likely want it radian
    def updating_quantities(self):
        #assigns [ax,ay,az],[rax,ray,yaz],[t]
        available_batches = self.chip.numFIFOBatches()
        self.linear_acceleration,self.angular_acceleration, self.dt = self.chip.readFIFO(available_batches)

        if (self.is_debug_logging):
            logger.debug(
                'Time {}, linear {}, angular {}'.format(
                    self.dt,
                    self.linear_acceleration,
                    self.angular_acceleration
                )
            )

        if True:
            #early exit for first test
            return



        # updates linear position using the velocity it believes it was travelling
        # over the period of time since acceleration was last updates
        # then updates velocity using acceleration it has just read
        # this part needs to have the everloving shit optimized out of it
        delta_linear_position = [v_component * self.dt for v_component in self.linear_velocity]

        self.linear_position = [sum(p_component) for p_component in zip(self.linear_position, delta_linear_position)]

        delta_linear_velocity = [a_component * self.dt for a_component in self.linear_acceleration]

        self.linear_velocity = [sum(v_component) for v_component in zip(self.linear_velocity, delta_linear_velocity)]


        # same function as lines above, but updating rotation
        delta_angular_position = [v_component * self.dt for v_component in self.angular_velocity]

        self.angular_position = [sum(p_component) for p_component in zip(self.angular_position, delta_angular_position)]

        delta_angular_velocity = [a_component * self.dt for a_component in self.angular_acceleration]

        self.angular_velocity = [sum(v_component) for v_component in zip(self.angular_velocity, delta_angular_velocity)]


