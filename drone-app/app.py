

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(14, GPIO.OUT)

p = GPIO.PWM(14, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while True:
        for dc in range(60, 90, 1):
            p.ChangeDutyCycle(dc/10.0)
            time.sleep(0.5)
        for dc in range(90, 60, -1):
            p.ChangeDutyCycle(dc/10.0)
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()




# 20 ms pulses
# 1 ms 0% to 2 ms 100%
# 20% spead of pulse is 1.2 ms
# 80% speed  of pulse is 1.8 ms
# duty cycle = 1.2/20 = 6%   1.8/20 = 9%
