from position_sensor import MPU6050

class SensorData(object):

#[x,y,z]

def __init__(self):
    self.chip=MPU6050()

    self.linear_acceleration = [0,0,0]
    self.linear_velocity = [0,0,0]
    self.linear_position = [0,0,0]

    self.angular_acceleration = [0,0,0]
    self.angular_velocity = [0,0,0]
    self.angular_position = [0,0,0]

    self.dt=0

def updating_quantities(self):

    # this doesn't work i think
    self.linear_acceleration,self.angular_acceleration, self.dt = readFIFO(self.chip,numFIFOBatches(self.chip))

    self.linear_velocity=
    self.linear_position

    self.angular_velocity
    self.angular_position

    pass
