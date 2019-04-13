
from unittest import TestCase
import time
import logging
import sys

from drone_app.PID import PID





logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


class TestSensorData(TestCase):


    def test_change_impulse(self):
        testPID=PID()

        time_old=time.time()
        time_difference = time.time() - time_old

        testPID.change_set_point(1)

        while time_difference < 10:
            pid_adjustment = testPID.calculate()
            simulated_new_point = testPID.current_point-pid_adjustment
            # NOTE: We can make this test more comprehensive by making the simulated_new_point more comprehensive a simulation
            testPID.change_current_point(simulated_new_point)

            time_difference=time.time()-time_old

            logger.info('Set Point: {}, Current Point {}, Adjustment {}'.format(testPID.set_point,
                                                                                 testPID.current_point,
                                                                                 pid_adjustment))

        #TODO: Goal is to be able to confirm something as having ended up correct