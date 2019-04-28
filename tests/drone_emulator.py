
import math





class FakeMotor:

    def __init__(self, ):
        self.percent_speed = 0.0
        self.actual_speed=0

    def start(self):

        pass

    def stop(self):

        pass


    #Todo: adjust rate of change for time as opposed to loops to avoid system clock speed affecting acceleration
    def update_speed(self, percent_speed: float):
        self.percent_speed = percent_speed
        self.actual_speed = 0.9 * self.actual_speed + 0.1 * self.percent_speed

    def get_speed(self):
        return self.percent_speed




class DroneEmulator:

    def __init__(self):

        self.fl = FakeMotor()
        self.fr = FakeMotor()
        self.bl = FakeMotor()
        self.br = FakeMotor()

        self.angle_forward = 0.0
        self.angle_right = 0.0

        return


    def increment_angles(self):
        left_side = self.fl.percent_speed + self.bl.percent_speed
        right_side = self.fr.percent_speed + self.br.percent_speed

        delta_translate_normalized = (left_side - right_side) / 200

        self.angle_right += math.pi * 1/100 * delta_translate_normalized


        front_side = self.fl.percent_speed + self.fr.percent_speed
        back_side = self.bl.percent_speed + self.br.percent_speed

        delta_forward_normalized = (back_side - front_side) / 200

        self.angle_forward += math.pi * 1/100 * delta_forward_normalized





    def numFIFOBatches(self):
        return 1

    def readRawAcceleration(self, fifo_batches):


        self.increment_angles()


        average_force_normalized = (self.fl.percent_speed + self.bl.percent_speed + self.fr.percent_speed +self.br.percent_speed) / 400

        vertical_component = math.cos(self.angle_forward) * math.cos(self.angle_right) * average_force_normalized

        forward_component = math.sin(self.angle_forward) * average_force_normalized

        right_component = math.sin(self.angle_right) * average_force_normalized


        adjusted_vertical_component = vertical_component - 0.6  # Assumes motors must be effectively 60% vertical to stay in the air

        #Assume mapping to g's as a fraction of a g

        linear_accel = (forward_component, right_component, adjusted_vertical_component)



        number_of_points = len(self.return_accel)

        return linear_accel, (0,0,0), 1.0

    def flushFIFO(self):
        return