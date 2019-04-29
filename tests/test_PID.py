
from unittest import TestCase
import logging
import sys
import csv

from drone_app.PID import PID





logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


class TestSensorData(TestCase):



    #Extension of the TestCase class, called once per test in this class
    def setUp(self):
        self.pid_response_handle = open('pid_response.csv', 'w')
        self.pid_response_writer = csv.writer(self.pid_response_handle)
        self.pid_response_writer.writerow(['timestamp','value_at_timestamp'])


    def tearDown(self):
        if self.pid_response_handle:
            self.pid_response_writer = None
            self.pid_response_handle.close()
            self.pid_response_handle = None



    MOCK_SAMPLE_RATE = 200
    def test_change_impulse(self):
        testPID=PID(0.01,0,0)
        #1.85,0,0 & 1.85,0,0.0001

        TARGET_SET_POINT = 1.0
        testPID.change_set_point(TARGET_SET_POINT)
        simulated_new_point = 0

        counter = 0
        while abs((testPID.current_point - testPID.set_point) / testPID.set_point) > 0.0001:
            counter += 1
            pid_adjustment = testPID.calculate(simulated_new_point, 1.0/TestSensorData.MOCK_SAMPLE_RATE)
            simulated_new_point = testPID.current_point+pid_adjustment


            # I really want to make a graph of this and I really just don't know how to interact with files like that
           # logger.info('Set Point: {}, Current Point {}, Adjustment {},Time {}'.format(testPID.set_point,
            #                                                                     testPID.current_point,
            #                                                                     pid_adjustment,
            #                                                                     counter/TestSensorData.MOCK_SAMPLE_RATE))
            self.pid_response_writer.writerow([counter/TestSensorData.MOCK_SAMPLE_RATE , testPID.current_point])

        self.assertAlmostEqual(testPID.current_point, testPID.set_point, 2) # Asserts that the current and set point are similar to 2 sig figs


