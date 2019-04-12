
from motor_matrix import MotorMatrix
from sensor_data import SensorData, SensorDataManager



class DroneControllerInterface:

    def ready(self):
        raise NotImplementedError



class Drone (SensorDataManager):

    #TODO: set constant to conservative value, affects the set point targeted when passing a percent.
    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 1234

    MODE_STOPPED = 0
    MODE_SENSOR_LOG = 1
    MODE_ACTIVE = 2



    def __init__(self):

        self.mode = Drone.MODE_STOPPED
        self.motor_matrix = MotorMatrix()
        self.sensor_data = SensorData(self)




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

    def right_at_rate(self, right_percent):

        raise NotImplementedError()

    def yaw_right_at(self, yaw_right_percent):
        raise NotImplementedError


    def PID(self):

    # PID Equation:
    # MV(t)=Kp*e(t)+Ki*I+Kd*(de/dt)
    #
    # MV is the Movable Variable (Motor Output)
    # Kp is Gain on Proportional Term
    # e(t)=(SP-PV(t)) or error
    # SP is the desired Setpoint
    # PV(t) is the current point as a function of time
    # Ki is Gain on Integral Term
    # I= integral of e(tau) from 0 to t
    # t is the instantaneous time
    # tau is the variable of integration
    # Kd is Gain on Derivative Term

    # Tuning Methods:

    # Gradient Descent: Pro: Automatic, good. Con: Implementation, Local minimums :(

    # Ziegler Nichols: Probably can't work, since we need this system to work before the drone #works and it would need to go up and down a bunch of times (Model with force sensor and #one motor?)
    # Heuristic goes like this:
    # Set integral and derivative gains to zero. Increase Proportional gain til it starts to #oscillate.
    # Set proportional as 60% of that, integral as 1.2 times it, divided by oscillation period, #set derivative as 3/40* it* oscillation period

    # Manual:

    # Effects of increasing a parameter independently[21][22]
    # Parameter	Rise time	Overshoot	Settling time	Steady-state error	#Stability
    # K_{p}		Decrease	Increase	Small change	Decrease		#Degrade
    # K_{i}		Decrease	Increase	Increase	Eliminate		#Degrade
    # K_{d}		Minor change	Decrease	Decrease	No effect in theory	#Improve if K_{d} is small
    #
    #
    #
    # Relevant Secondary Steps:
    # Integral Windup - If the integral term is contantly "on" a big change in setpoint will #make the drone overshoot really bad. If it only starts acting once it gets a bit closer #to setpoint, then it won't overshoot as badly, but will still be very precise
    #
    # I really really want us to try to write a feed-forward control. I think we need to figure #out percent speed in relation to percent duty cycle and store that. Or have it work it #out while it flies.
    # Feed forward can cause like order of magnitude shifts in PID effectiveness
    #
    #
    # Not Relevant but Interesting:
    # Deadband is the idea of making a larger band of acceptable values to prevent wear and #tear on things like valves

    # Symmetry poses an interesting issue in that PID is symmetrical, but it's possible outputs #might not be (if you don't have A/C, you can only heat)
    # This is sometimes solved by damping the impact of the integral term, as it attempts to #essentially overshoot.

    def cleanup(self):
        self.motor_matrix.cleanup()
