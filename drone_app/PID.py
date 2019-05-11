import time

class PID:

    def __init__(self,proportional, integral,derivative):
        self.output=0

        self.proportional_gain=proportional
        self.integral_gain=integral
        self.derivative_gain=derivative

        #last error used to calculate derivative
        self.last_error_term=0

        #accumulator used to calculate integral
        self.integral_term=0

        self.set_point=0
        self.current_point=0


    def change_set_point(self,new_setpoint):

        self.set_point=new_setpoint

    #TODO: use property getter
    def get_set_point(self):
        return self.set_point

    def calculate(self, new_current_point, dt):

        self.current_point = new_current_point

        PID_dt=dt


        #calculates error
        error=self.set_point-self.current_point

        #calculates difference in error since last time
        delta_error=error-self.last_error_term
        #calculates derivative term
        derivative_term=delta_error/PID_dt

        #calculates integral term
        self.integral_term=self.integral_term+(PID_dt*error)

        #records current error for next loop
        self.last_error_term=error

        #calculates motor_output using PID equation
        self.output= (self.proportional_gain * error) + (self.integral_gain * self.integral_term) + (self.derivative_gain * derivative_term)

        return self.output





    #TODO: Decide on what PID controls
    #I assume it is going to be controlling velocities

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
