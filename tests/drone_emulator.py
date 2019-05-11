
import math
import time
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


class FakeMotor:

    def __init__(self, ):
        self.percent_speed = 0.0
        self.actual_speed = 0
        self.last_update_time = time.time()

    def start(self):

        pass

    def stop(self):

        pass

    def update_speed(self, percent_speed: float):

        self.percent_speed = percent_speed
        time_now = time.time()
        if (time_now-self.last_update_time) > 0.05:
            self.actual_speed = 0.9 * self.actual_speed + 0.1 * self.percent_speed
            self.last_update_time = time_now


    def get_speed(self):
        return self.percent_speed




class DroneEmulator:

    def __init__(self):

        self.start_sample_time = None
        self.last_num_fifo_time = None

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



    MOCK_SAMPLE_RATE_PER_SECOND = 200

    def numFIFOBatches(self):

        if self.start_sample_time is None:
            #indicates not initialized
            return 0

        old_last_fifo = self.last_num_fifo_time
        new_fifo_time = time.time()

        # by continuously counting back to the original sample time,
        # this code avoid drift that would occur with summing delta times
        old_sample_count = int((old_last_fifo - self.start_sample_time) * DroneEmulator.MOCK_SAMPLE_RATE_PER_SECOND)
        new_sample_count = int((new_fifo_time - self.start_sample_time) * DroneEmulator.MOCK_SAMPLE_RATE_PER_SECOND)

        if new_sample_count > old_sample_count:
            self.last_num_fifo_time = new_fifo_time
            return new_sample_count - old_sample_count

        #still in the same bucket
        return 0

    def readRawAcceleration(self, fifo_batches):


        self.increment_angles()


        average_force_normalized = (self.fl.percent_speed + self.bl.percent_speed + self.fr.percent_speed +self.br.percent_speed) / 400

        vertical_component = math.cos(self.angle_forward) * math.cos(self.angle_right) * average_force_normalized


        forward_component = math.sin(self.angle_forward) * average_force_normalized

        right_component = math.sin(self.angle_right) * average_force_normalized


        adjusted_vertical_component = vertical_component - 0.3  # Assumes motors must be effectively 40% vertical to stay in the air

        #Assume mapping to g's as a fraction of a g

        linear_accel = (forward_component, right_component, adjusted_vertical_component)

        #logger.info("Current accel force {}".format(linear_accel))

        return linear_accel, (0,0,0), (1.0/DroneEmulator.MOCK_SAMPLE_RATE_PER_SECOND) * fifo_batches

    def flushFIFO(self):
        self.start_sample_time = time.time()
        self.last_num_fifo_time = self.start_sample_time
        return