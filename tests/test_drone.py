from tests.drone_emulator import DroneEmulator
from unittest import TestCase
import time
import logging
import sys
import csv






logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


class TestSensorData(TestCase):



    #Extension of the TestCase class, called once per test in this class
    def setUp(self):
        self.pid_response_handle = open('pid_response.csv', 'w')
        self.pid_response_writer = csv.writer(self.pid_response_handle)
        #self.pid_response_writer.writerow(['timestamp','value_at_timestamp'])


    def tearDown(self):
        if self.pid_response_handle:
            self.pid_response_writer = None
            self.pid_response_handle.close()
            self.pid_response_handle = None




    def test_drone_steady_rise(self):

        #Istantiate a drone
        #Either: swap motors and sensor OR Pass in simulated override
        # give drone instructions to rise, then stop

        # graph results
        # assert motors approximately 60%

        pass
