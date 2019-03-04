

import time
import RPi.GPIO as GPIO

MAX_WIDTH_MILLIS = 2
MIN_WIDTH_MILLIS = 1
PULSE_PERIOD =20

def duty_cycle_from_percent(percent_speed:float):
    duty_cycle_input = 100*(MIN_WIDTH_MILLIS+(percent_speed/100)*(MAX_WIDTH_MILLIS-MIN_WIDTH_MILLIS))/PULSE_PERIOD

    if(duty_cycle_input>100*MAX_WIDTH_MILLIS/PULSE_PERIOD):
        duty_cycle_input=100*MAX_WIDTH_MILLIS/PULSE_PERIOD

    elif(duty_cycle_input<100*MIN_WIDTH_MILLIS/PULSE_PERIOD):
        100 * MIN_WIDTH_MILLIS / PULSE_PERIOD

    return duty_cycle_input


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

    def __init__(self, FrontOrBack, LeftOrRight, Pinout, PropellerDirection, PercentSpeed):
        self.FrontOrBack = FrontOrBack
        self.LeftOrRight = LeftOrRight
        self.Pinout = GPIO.PWM()
        self.PropellerDirection = PropellerDirection
        self.PercentSpeed = PercentSpeed



    #we should consider whether we care about our ESCs ability to brake and move in reverse
    #should this update separate from changing the value for speed?
    def update_speed(self):
        self.Pinout.ChangeDutyCycle(duty_cycle_from_percent(self.PercentSpeed))



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
#oh sweet jesus i don't even know if this is something I can do, but I've already made unreadable spaghetti
#should there be a Motor function that creates a pin object?
m=Motor('Front','Left',p,'clockwise',0)

p.ChangeDutyCycle(5)
time.sleep(60)

print("Done Init")
#try:
#    while True:
#        for dc in range(60, 90, 1):
#            p.ChangeDutyCycle(dc/10.0)
#            time.sleep(0.1)
#        for dc in range(90, 60, -1):
#            p.ChangeDutyCycle(dc/10.0)
#            time.sleep(0.1)
#except KeyboardInterrupt:
#    pass
#print("cleaning up")
p.stop()
GPIO.cleanup()



#needs despaghettification
#100*(MIN_WIDTH_MILLIS+(percent_speed/100)*(MAX_WIDTH_MILLIS-MIN_WIDTH_MILLIS))/PULSE_PERIOD
#actual length= min+(speed/100)*(max-min)
#decimal duty cycle = actual length/period
#percent duty cycle = 100 *decimal duty cycle

# 20 ms pulses
# 1 ms 0% to 2 ms 100%
# 20% spead of pulse is 1.2 ms
# 80% speed  of pulse is 1.8 ms
# duty cycle = 1.2/20 = 6%   1.8/20 = 9%
