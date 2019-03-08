from position_sensor import PositionSensor

class SensorData(object):
#drone has position relative to an absolute from north+ gravity

#drone has 6 accelerations, 6 velocities, and 6 positions (3 linear, 3 rotational each)
#we will use the 3 linear accelerations to track a velocity (inverse sample frequency*acceleration)
#we will use the 3 angular accelerations to track the position of gravity

#this gives us full info about the drone from its starting position
    pass
