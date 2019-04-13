import PID from PID
import time

testPID=PID()

time_old=time.time()

testPID.change_set_point(1)

while time_difference < 10:
    
    testPID.change_current_point(testPID.current_point-testPID.calculate())

    time_difference=time.time()-time_old