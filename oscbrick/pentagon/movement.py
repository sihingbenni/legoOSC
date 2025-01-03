from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from oscbrick.oschandler.motor import MotorHandler
from oscbrick.pentagon.scanner import get_color, get_distance
from oscbrick.utilities import run_in_thread


class RobotController:
    STANDARD_DRIVE_DISTANCE = 300

    def __init__(self):
        self.motor_left = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.motor_right = Motor(Port.D)
        self.motor_neck = Motor(Port.B)
        self.motor_handler = MotorHandler()

        self.initRobot()

        self.skip_next_instruction = False
        self.looking_direction = self.LookingDirection()

    def initRobot(self):
        self.robot = DriveBase(self.motor_left, self.motor_right, wheel_diameter=56, axle_track=47.7)
        self.robot.settings(100, 50, 90, 180)

    class LookingDirection:
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]

        def __init__(self, direction: str = None):
            self.current_direction = direction if direction else "NORTH"

        def turn_right(self):
            idx_next = (self.directions.index(self.current_direction) + 1) % len(self.directions)
            self.current_direction = self.directions[idx_next]

        def turn_left(self):
            idx_next = (self.directions.index(self.current_direction) - 1) % len(self.directions)
            self.current_direction = self.directions[idx_next]

        def turn_around(self):
            idx_next = (self.directions.index(self.current_direction) + 2) % len(self.directions)
            self.current_direction = self.directions[idx_next]

    def turn_right(self):
        self.initRobot()
        self.looking_direction.turn_right()
        print("Turning right!")
        self.robot.stop()
        self.robot.turn(90)

    def turn_left(self):
        self.initRobot()
        self.looking_direction.turn_left()
        print("Turning left!")
        self.robot.stop()
        self.robot.turn(-90)

    def turn_around(self):
        self.initRobot()
        self.looking_direction.turn_around()
        print("Turning around!")
        self.robot.stop()
        self.robot.turn(180)

    def spin(self):
        self.initRobot()
        print("You spin my head right round right round")
        self.robot.stop()
        self.robot.turn(360)

    def drive_forward(self, distance: int, is_check: bool = True, next_instruction: str = None):
        self.initRobot()
        self.robot.stop()
        self.robot.straight(distance)
        
        if is_check:
            wait(1000)
            self.check_alignment(next_instruction)

    def align_forwards(self):
        self.initRobot()

        print("Align Forwards")
        self.robot.stop()

        run_in_thread(self.motor_right.run_until_stalled, 100, Stop.BRAKE, 22)
        run_in_thread(self.motor_left.run_until_stalled, 100, Stop.BRAKE, 22)
        wait(1000)
        while (self.motor_right.speed() > 0 or self.motor_left.speed() > 0):
            pass
        wait(1000)
        self.drive_forward(-40, False)

    def align_backwards(self):
        self.initRobot()
        print("Align Backwards")
        self.robot.stop()

        run_in_thread(self.motor_right.run_until_stalled, -100, Stop.BRAKE, 23)
        run_in_thread(self.motor_left.run_until_stalled, -100, Stop.BRAKE, 223)
        wait(1000)
        while (self.motor_right.speed() > 0 or self.motor_left.speed() > 0):
            pass
        wait(1000)
        self.drive_forward(40, False)

    def align_neck(self, is_right: bool = True):
        self.initRobot()
        self.robot.stop()
        print("Aligning the neck")
        self.motor_neck.reset_angle(0)
        if is_right:
            self.motor_neck.run_until_stalled(-200, Stop.BRAKE, 40)
        else:
            self.motor_neck.run_until_stalled(200, Stop.BRAKE, 40)
        self.motor_neck.reset_angle(0)
    
    def _get_consistent_distance(self):
        distance_1 = get_distance()
        print("Distance 1: {}".format(distance_1))
        wait(1000)
        distance_2 = get_distance()
        wait(1000)
        print("Distance 2: {}".format(distance_2))
        if distance_1 != distance_2:
            print("Distance values are inconsistent, rescanning...")
            return get_distance()
        return distance_1

    def scan(self):
        color = get_color()

        self.align_neck(True)
        wait(500)
        r_distance = self._get_consistent_distance()
        print("Distance r: {}".format(r_distance))

        self.motor_neck.run_angle(200, 115)
        wait(500)
        m_distance = self._get_consistent_distance()
        print("Distance m: {}".format(m_distance))



        self.align_neck(False)
        l_distance = self._get_consistent_distance()
        print("Distance l: {}".format(l_distance))


        result = {
            "distance_r": r_distance,
            "distance_m": m_distance,
            "distance_l": l_distance,
            "color": color
        }

        print(result)
        return result

    def check_alignment(self, next_instruction: str = ""):
        self.initRobot()
        scan_result = self.scan()
        print("Checking Alignment")
        print(scan_result)

        if scan_result.get("distance_m") < 140:
            self.align_forwards()
            wait(2000)

        if scan_result.get("distance_r") < 140:
            self.turn_left()
            wait(1000)
            self.align_backwards()
            if next_instruction != "turn_left":
                wait(1000)
                self.turn_right()
            else:
                self.skip_next_instruction = True

        elif scan_result.get("distance_l") < 140:
            self.turn_right()
            wait(1000)
            self.align_backwards()
            if next_instruction != "turn_right":
                wait(1000)
                self.turn_left()
            else:
                self.skip_next_instruction = True

    def drive_according_to_list(self, instructions):
        self.initRobot()
        print("Driving according to instruction list")
        for idx, instruction in enumerate(instructions):
            print("Step: {}: {}".format(idx + 1, instruction))

            if self.skip_next_instruction:
                self.skip_next_instruction = False
                print("Skipping step: '{}' because it was already fulfilled".format(instruction))
                continue

            if instruction == "drive_forward":
                self.drive_forward(self.STANDARD_DRIVE_DISTANCE)

            elif instruction == "turn_around":
                self.turn_around()

            elif instruction == "turn_left":
                self.turn_left()

            elif instruction == "turn_right":
                self.turn_right()

            wait(1000)
