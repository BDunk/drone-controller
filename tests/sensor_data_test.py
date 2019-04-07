from unittest import TestCase
import time


from ..drone-app.sensor_data import SensorData, SensorDataManager


class PositionSensorDriverHelper:

    def __init__(self):
        self.return_accel = None


    def set_acceleration_returns(self, return_accel):
        self.return_accel = return_accel

    def numFIFOBatches(self):
        return len(self.return_accel)

    def readRawAcceleration(self, fifo_batches):
        return self.return_accel, self.return_accel, 1.0




class TestSensorData(TestCase, SensorDataManager):

    def setUp(self):
        self.mock_sensor = PositionSensorDriverHelper()
        self.is_calibration_complete = False

    def calibration_complete(self):

        self.is_calibration_complete = True


    def test_calibrate(self):

        #Set up the sensor_data, point it to our mock driver
        sensor_data = SensorData(self, self.mock_sensor)

        #set up the drive to return accelerations that average to 2
        calibration_data_average_2 = [
            [1,2,5],
            [3,0,-3],
        ]

        self.mock_sensor.set_acceleration_returns(calibration_data_average_2)

        # put setup data into calibration mode
        sensor_data.start_calibration()


        # wait for the calibration to complete (set in callback)
        while self.is_calibration_complete:
            time.sleep(0.1) # NOTE: to complete faster, can use freeze time and force specific times...
            sensor_data.process_sensor()

        # should be calibrated, switch to reading
        sensor_data.start_reading()

        # test inputs should be adjusted by calibration
        test_data = [
            [1,1,1],
        ]

        self.mock_sensor.set_acceleration_returns(test_data)

        # get the test data once
        sensor_data.process_sensor()


        linear_accel = sensor_data.get_linear_acceleration()
        angular_accel = sensor_data.get_angular_acceleration()

        for ii in range(3):
            self.assertAlmostEqual(-1, linear_accel[ii], msg='calibration should be close to -1 ')
            self.assertAlmostEqual(-1, angular_accel, msg='angular shoudl be close to -1')



