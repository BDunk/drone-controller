

import time

from motor import Motor



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)  # channel=12 frequency=50Hz
p.start(0)
#oh sweet jesus i don't even know if this is something I can do, but I've already made unreadable spaghetti
#should there be a Motor function that creates a pin object?
m = Motor('Front','Left',p,'clockwise',0)

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
