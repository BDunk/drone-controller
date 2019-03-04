

import time
import RPi.GPIO as GPIO

MAX_WIDTH_MILLIS = 2
MIN_WIDTH_MILLIS = 1
PULSE_PERIOD =20

def duty_cycle_from_percent(percent_speed:float): #make ridiculous sub calculations for the memes?
    duty_cycle_input = 100*(MIN_WIDTH_MILLIS+(percent_speed/100)*(MAX_WIDTH_MILLIS-MIN_WIDTH_MILLIS))/PULSE_PERIOD

    if(duty_cycle_input>100*MAX_WIDTH_MILLIS/PULSE_PERIOD):
        duty_cycle_input=100*MAX_WIDTH_MILLIS/PULSE_PERIOD
    
    elif(duty_cycle_input<100*MIN_WIDTH_MILLIS/PULSE_PERIOD):
        100 * MIN_WIDTH_MILLIS / PULSE_PERIOD

    return duty_cycle_input

#write a class for motor with pin to initialize, its position, it's direction, etc. Make function that changes the speed of the motor



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)

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






# 20 ms pulses
# 1 ms 0% to 2 ms 100%
# 20% spead of pulse is 1.2 ms
# 80% speed  of pulse is 1.8 ms
# duty cycle = 1.2/20 = 6%   1.8/20 = 9%
