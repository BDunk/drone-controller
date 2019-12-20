import logging

import time
from drone import Drone, DroneControllerInterface


logger = logging.getLogger()

logger.setLevel(logging.WARNING)

# NOTE: this controller waits 30 seconds, rises for 5 seconds at low rate, then proceeds down 10 seconds, and repeats

# Other controllers will either take input from a remote control via sensors,
# or streams of positions from an iphone app, or be fully autonomous :-)

class TestFlightController (object):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control
        self.current_state = "WAIT"
        self.enter_state_time = time.time()
        self.exit_state_time = self.enter_state_time + 8


    def process_actions(self):

        time_now = time.time()

        if (time_now < self.exit_state_time):
            # nothing to do yet
            return True


        #proceed to next state:
        self.enter_state_time = self.exit_state_time

        # TODO: proper declarative state machine...
        if self.current_state == "WAIT":
            self.current_state = "RISE"
            self.exit_state_time = self.enter_state_time + 3
            self.drone_to_control.rise_at_rate(0.1)
            logger.critical("Going from Wait to Rise")
            return True

        if self.current_state == "RISE":
            self.current_state = "HOVER"
            self.exit_state_time = self.enter_state_time + 10
            self.drone_to_control.rise_at_rate(0.0)
            logger.critical("Going from Rise to Hover")
            return True

        if self.current_state == "HOVER":
            self.current_state = "DROP"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.rise_at_rate(-0.1)
            logger.critical("Going from Hover to Drop")
            return True

        if self.current_state == "DROP":
            self.current_state = "DONE"
            self.exit_state_time = self.enter_state_time + 1
            self.drone_to_control.rise_at_rate(0)
            logger.critical("Going from Drop to Done")
            return True

        if self.current_state == "DONE":
            return False


    def ready(self):

        logger.critical("Test Flight Ready")
        return








