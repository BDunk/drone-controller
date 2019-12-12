import logging
from RPIO import PWM

logger = logging.getLogger()

logger.setLevel(logging.INFO)

servo = PWM.Servo()

class Motor (object):
    """
    motor objects represent our physical motors. they have these properties:
    They are initialized with the gpio pin number.
    They rely on the fact that the direction is configured at the ESC/wiring level
    Each motor should be started and stopped before and after use in order to emit a pulse stream
    After all motors are stopped the cleanup_all_motors class method should be called

    Their speed can be updated with affects internal state and the motor, speed is retrieved from state.
     (speed is in percent)
    """

    MAX_WIDTH_MICROS = 2000
    MIN_WIDTH_MICROS = 1000
    PULSE_PERIOD_MILLIS = 20.0
    PULSE_FREQUENCY = 1/(PULSE_PERIOD_MILLIS/1000)
    VARIABLE_RANGE_MICROS = MAX_WIDTH_MICROS - MIN_WIDTH_MICROS


    def __init__(self, gpio_number):

        self.percent_speed = 0.0
        self.gpio_number = gpio_number
        self.pwm_controller = None

    def start(self):

        servo.set_servo(self.gpio_number, Motor.MIN_WIDTH_MICROS)

    def stop(self):
        servo.stop_servo(self.gpio_number)

    @classmethod
    def cleanup_all_motors(cls):
        PWM.cleanup()

    def update_speed(self, percent_speed: float):
        self.percent_speed = percent_speed
        micros_for_speed = Motor.micros_from_percent(self.percent_speed)
        logger.info('percent {} micros {} for motor {} '.format(percent_speed, micros_for_speed, self.gpio_number))
        servo.set_servo(self.gpio_number, micros_for_speed)

    def get_speed(self):
        return self.percent_speed

    @classmethod
    def micros_from_percent(cls, percent_speed: float):

        bounded_percent_speed = min(100.0, max(0.0, percent_speed))
        bounded_ratio_speed = bounded_percent_speed/100.0

        desired_pulse_width = Motor.MIN_WIDTH_MICROS + bounded_ratio_speed * Motor.VARIABLE_RANGE_MICROS

        return desired_pulse_width




