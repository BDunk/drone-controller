from tests.drone_emulator import DroneEmulator
from drone_app.drone import DroneControllerInterface, Drone
from unittest import TestCase
from drone_app.motor_matrix import MotorDefinition
import time
import logging
import sys
import csv
import math

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.WARNING)


class TestLateral(TestCase, DroneControllerInterface):



    #Extension of the TestCase class, called once per test in this class
    def setUp(self):

        self.is_ready = False


    def tearDown(self):
        pass


    def ready(self):
        self.is_ready = True
        return

    def record_state(self, drone_emulator):

        self.drone_response_writer.writerow([
            time.time() - self.start_time_test,
            drone_emulator.angle_forward,
            drone_emulator.angle_right,
            drone_emulator.fl.actual_speed,
            drone_emulator.fr.actual_speed,
            drone_emulator.br.actual_speed,
            drone_emulator.bl.actual_speed,
            drone_emulator.fl.percent_speed,
            drone_emulator.fr.percent_speed,
            drone_emulator.br.percent_speed,
            drone_emulator.bl.percent_speed,
        ])

    def test_wind_strike(self):

        self.start_time_test = time.time()

        self.drone_response_handle = open('drone_lateral.csv', 'w')
        self.drone_response_writer = csv.writer(self.drone_response_handle)
        self.drone_response_writer.writerow(['timestamp', 'frontAngle', 'rightAngle', 'flActual', 'frActual', 'brActual', 'blActual',
                                             'flDemand', 'frDemand', 'brDemand', 'blDemand'])


        drone_emulator = DroneEmulator()

        motor_definition = MotorDefinition(drone_emulator.fl, drone_emulator.fr, drone_emulator.bl, drone_emulator.br)

        drone = Drone(drone_emulator, motor_definition)

        drone.start(self)

        while True:
            time.sleep(1/1000)
            drone.process_sensors()
            if (self.is_ready):
                break
            self.record_state(drone_emulator)

        start_hover = time.time()

        drone.rise_at_rate(0)

        while True:
            time.sleep(1/1000)
            time_now = time.time()
            drone.process_sensors()
            if (time_now - start_hover) > 10:
                break
            self.record_state(drone_emulator)

        #fake dropping the front:

        drone_emulator.angle_forward = (20/360) * 2 * math.pi

        start_recover_front_drop = time.time()

        while True:
            time.sleep(1/1000)
            time_now = time.time()
            drone.process_sensors()
            if (time_now - start_recover_front_drop) > 30:
                break
            self.record_state(drone_emulator)

        #fake dropping the left:
        # drone_emulator.angle_right = (-20/360) * 2 * math.pi
        #
        # start_recover_left_drop = time.time()
        #
        # while True:
        #     time.sleep(1 / 1000)
        #     time_now = time.time()
        #     drone.process_sensors()
        #     if (time_now - start_recover_left_drop) > 5:
        #         break
        #     self.record_state(drone_emulator)


        self.drone_response_writer = None
        self.drone_response_handle.close()
        self.drone_response_handle = None

        self.assertAlmostEqual(60, drone_emulator.fl.actual_speed, places=2)
        self.assertAlmostEqual(60, drone_emulator.fr.actual_speed, places=2)
        self.assertAlmostEqual(60, drone_emulator.bl.actual_speed, places=2)
        self.assertAlmostEqual(60, drone_emulator.br.actual_speed, places=2)

