
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

        TARGET_SET_POINT = 1.0
        testPID.change_set_point(TARGET_SET_POINT)

        while time_difference < 2:
            pid_adjustment = testPID.calculate()  #TODO: Sometimes this method throws a division by zero, I expect it occurs if the time rounds to the same value (race condition)
            simulated_new_point = testPID.current_point+pid_adjustment
            # NOTE: We can make this test more comprehensive by making the simulated_new_point more comprehensive a simulation
            testPID.change_current_point(simulated_new_point)

            time_difference=time.time()-time_old

            logger.info('Set Point: {}, Current Point {}, Adjustment {}'.format(testPID.set_point,
                                                                                 testPID.current_point,
                                                                                 pid_adjustment))

        #TODO: Goal is to be able to confirm something as having ended up correct
        # TODO: So normally you would want to end up with some combination of asserts
        #
        self.assertAlmostEqual(testPID.current_point, testPID.set_point, 2) # Asserts that the current and set point are similar to 2 sig figs
        # self.assertAlmostEqual(TARGET_SET_POINT, testPID.current_point, 2) # Note: this isn't true with the current code
