
from motor_matrix import MotorMatrix
from position_sensor import PositionSensor




class Drone (object):

    #TODO: set constant to conservative value, affects the set point targeted when passing a percent.
    MAXIMUM_RISE_RATE_METERS_PER_SECOND = 1234


    def __init__(self):
        self.motor_matrix = MotorMatrix()
        self.position_sensor = PositionSensor()




    def start(self):
        self.motor_matrix.start_your_engines()


    def process_sensors(self):

        # TODO: read sensors, update motion calculations, adjust motor matrix

        # This is the magic of stability control and responding to instructions
        raise NotImplementedError

    def get_orientattion(self):
        #does this make most sense as two angles from gravity?
        raise NotImplemented

    def get_acceleration(self):
        #either relative to drone, or relative to magnetic pole or whatever
        raise NotImplemented

    def rise_at_rate(self, rise_percent):
        #check velocity, if velocity is not at desired rate, increase motor rate
        #check velocity, if it is changing in the wrong way, counter that
        raise NotImplementedError()


    # Note: this interface structure is likely to result in awkward movements (or I suppose we could use superposition),
    # imagine rotating in place than warlking forward rather than turning and walking smoothly
    # alternate model would be something like "desired new position" or "desired new vector"
    def forward_at_rate(self, forward_percent):

        raise NotImplementedError()


    def cleanup(self):
        self.motor_matrix.cleanup()
