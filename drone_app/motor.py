

#TODO: conditionally import rpi.gpio based on environment or make gpio availble
#import os
#os.uname()
try:
    import RPi.GPIO as GPIO
except ImportError:
    from gpio_mock import gpio_mock as GPIO






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

    MAX_WIDTH_MILLIS = 2.0
    MIN_WIDTH_MILLIS = 1.0
    PULSE_PERIOD_MILLIS = 20.0
    PULSE_FREQUENCY = 1/(PULSE_PERIOD_MILLIS/1000)
    VARIABLE_RANGE_MILLIS = MAX_WIDTH_MILLIS - MIN_WIDTH_MILLIS


    def __init__(self, gpio_number):

        self.percent_speed = 0.0
        self.gpio_number = gpio_number
        self.pwm_controller = None

    def start(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_number, GPIO.OUT)

        self.pwm_controller = GPIO.PWM(self.gpio_number, Motor.PULSE_FREQUENCY)
        duty_cycle_for_zero = Motor.duty_cycle_from_percent(0.0)
        self.pwm_controller.start(duty_cycle_for_zero)

    def stop(self):
        self.pwm_controller.stop()

    @classmethod
    def cleanup_all_motors(cls):
        GPIO.cleanup()

    def update_speed(self, percent_speed: float):
        self.percent_speed = percent_speed
        pwm_controller = self.pwm_controller
        duty_cycle_for_speed = Motor.duty_cycle_from_percent(self.percent_speed)
        pwm_controller.ChangeDutyCycle(duty_cycle_for_speed)

    def get_speed(self):
        return self.percent_speed

    @classmethod
    def duty_cycle_from_percent(cls, percent_speed: float):
        # needs despaghettification
        # 100*(MIN_WIDTH_MILLIS+(percent_speed/100)*(MAX_WIDTH_MILLIS-MIN_WIDTH_MILLIS))/PULSE_PERIOD
        # actual length= min+(speed/100)*(max-min)
        # decimal duty cycle = actual length/period
        # percent duty cycle = 100 *decimal duty cycle

        bounded_percent_speed = min(100.0, max(0.0, percent_speed))
        bounded_ratio_speed = bounded_percent_speed/100.0

        desired_pulse_width = Motor.MIN_WIDTH_MILLIS + bounded_ratio_speed * Motor.VARIABLE_RANGE_MILLIS

        duty_cycle_percent = (desired_pulse_width/Motor.PULSE_PERIOD_MILLIS) * 100.0

        return duty_cycle_percent



