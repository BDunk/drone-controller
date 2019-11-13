from drone import Drone, DroneControllerInterface
import time


class TestMotorController (DroneControllerInterface):

    def __init__(self, drone_to_control: Drone):
        self.drone_to_control = drone_to_control
        self.current_state = "WAIT"
        self.enter_state_time = time.time()
        self.exit_state_time = self.enter_state_time + 10000

    def process_actions(self):

        time_now = time.time()

        if time_now < self.enter_state_time:
            # over cautious code that handles clock changes
            # i.e. handles time going backwards
            self.enter_state_time = time_now
            self.exit_state_time = time_now

        if time_now < self.exit_state_time:
            # nothing to do yet
            return True

        # proceed to next state:
        self.enter_state_time = self.exit_state_time

        # TODO: proper declarative state machine...
        if self.current_state == "WAIT":
            self.current_state = "FL"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.direct_motor_test(0.0, 0.0, 0.0, 0.5)
            return True

        if self.current_state == "FL":
            self.current_state = "FR"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.direct_motor_test(0.0, 0.0, 0.0, 0.5)
            return True

        if self.current_state == "FR":
            self.current_state = "BR"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.direct_motor_test(0.0, 0.0, 0.0, 0.5)
            return True

        if self.current_state == "BR":
            self.current_state = "BL"
            self.exit_state_time = self.enter_state_time + 5
            self.drone_to_control.direct_motor_test(0.0, 0.0, 0.0, 0.5)
            return True

        if self.current_state == "BL":
            self.current_state = "DONE"
            self.drone_to_control.direct_motor_test(0.0, 0.0, 0.0, 0.0)
            return False

        return True

    def ready(self):
        # Exit the wait mode when ready called
        self.exit_state_time = time.time()

        return

