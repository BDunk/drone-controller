
import time
from drone import Drone

# NOTE: this controller waits 30 seconds, rises for 5 seconds at low rate, then proceeds down 10 seconds, and repeats

# Other controllers will either take input from a remote control via sensors,
# or streams of positions from an iphone app, or be fully autonomous :-)

class TestFlightController (object):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control
        self.current_state = "WAIT"
        self.enter_state_time = time.time()
        self.exit_state_time = self.enter_state_time + 30

    def process_actions(self):

        time_now = time.time()

        if (time_now < self.enter_state_time):
            # over cautious code that handles clock changes
            # i.e. handles time going backwards
            self.enter_state_time = time_now
            self.exit_state_time = time_now

        if (time_now < self.exit_state_time):
            # nothing to do yet
            return

        #proceed to next state:
        self.enter_state_time = self.exit_state_time

        # TODO: proper declarative state machine...
        if self.current_state == "WAIT":
            self.current_state = "RISE"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.rise_at_rate(10)

        if self.current_state == "RISE":
            self.current_state = "DROP"
            self.exit_state_time = self.enter_state_time + 10
            self.drone_to_control.rise_at_rate(-10)

        if self.current_state == "DROP":
            self.current_state = "WAIT"
            self.exit_state_time = self.enter_state_time + 30
            self.drone_to_control.rise_at_rate(0)










