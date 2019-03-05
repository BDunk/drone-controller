
import RPi.GPIO as GPIO







class Motor (object):
    """
    motor objects represent our physical motors. they have these properties:
    FrontOrBack: front or back position
    LeftOrRight: left or right position
    PinOut: GPIO.PWM object for output to motor
    PropellerDirection: clockwise/counterclockwise rotation
    PercentSpeed: represents the percentage of the length of pulse between min and max for our escs, can only be 0.0-100.0
    """
    #I don't think we really need all of these properties, but I got excited

    MAX_WIDTH_MILLIS = 2
    MIN_WIDTH_MILLIS = 1
    PULSE_PERIOD = 20
    RANGE_MILLIS = MAX_WIDTH_MILLIS - MIN_WIDTH_MILLIS

    def __init__(self, FrontOrBack, LeftOrRight, Pinout, PropellerDirection, PercentSpeed):
        self.FrontOrBack = FrontOrBack
        self.LeftOrRight = LeftOrRight
        self.Pinout = GPIO.PWM()
        self.PropellerDirection = PropellerDirection
        self.PercentSpeed = PercentSpeed



    #TODO: we should consider whether we care about our ESCs ability to brake and move in reverse
    #should this update separate from changing the value for speed?
    def update_speed(self):
        self.Pinout.ChangeDutyCycle(duty_cycle_from_percent(self.PercentSpeed))


    @classmethod
    def duty_cycle_from_percent(cls, percent_speed: float):
        # needs despaghettification
        # 100*(MIN_WIDTH_MILLIS+(percent_speed/100)*(MAX_WIDTH_MILLIS-MIN_WIDTH_MILLIS))/PULSE_PERIOD
        # actual length= min+(speed/100)*(max-min)
        # decimal duty cycle = actual length/period
        # percent duty cycle = 100 *decimal duty cycle

        bounded_percent_speed = min(100.0, max(0.0, percent_speed))
        bounded_ratio_speed = bounded_percent_speed/100.0

        desired_pulse_width = Motor.MIN_WIDTH_MILLIS + bounded_ratio_speed * Motor.RANGE_MILLIS

        duty_cycle_percent =  (desired_pulse_width/Motor.PULSE_PERIOD) * 100.0

        return duty_cycle_percent

