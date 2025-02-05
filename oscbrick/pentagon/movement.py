from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from oscbrick.oschandler.motor import MotorHandler
from oscbrick.pentagon.scanner import get_color, get_distance


class RobotController:
    STANDARD_DRIVE_DISTANCE = 300
    ALIGN_TIME = 2000
    WAIT_TIME = 250
    PUSH_AWAY=30

    def __init__(self):
        self.robot = None
        self.motor_left = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
        self.motor_right = Motor(Port.D)
        self.motor_handler = MotorHandler()

        self.init_robot()

        self.skip_next_instruction = False
        self.looking_direction = self.LookingDirection()

    def init_robot(self):
        self.robot = DriveBase(self.motor_left, self.motor_right, wheel_diameter=56, axle_track=47.7)
        self.robot.settings(80, 150, 90, 270)

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
        self.init_robot()
        self.looking_direction.turn_right()
        print("Turning right!")
        self.robot.stop()
        self.robot.turn(90)

    def turn_left(self):
        self.init_robot()
        self.looking_direction.turn_left()
        print("Turning left!")
        self.robot.stop()
        self.robot.turn(-90)

    def turn_around(self):
        self.init_robot()
        self.looking_direction.turn_around()
        print("Turning around!")
        self.robot.stop()
        self.robot.turn(180)

    def spin(self):
        self.init_robot()
        print("You spin my head right round right round")
        self.robot.stop()
        self.robot.turn(360)

    def drive_forward(self, distance: int, is_check: bool = True, next_instruction: str = None):
        self.init_robot()
        self.robot.straight(distance)

        if is_check:
            wait(self.WAIT_TIME)
            self.check_alignment(next_instruction)

    def align_forwards(self):
        self.init_robot()
        print("Align Forwards")
        self.robot.stop()
        self.robot.drive(50, 0)
        wait(self.ALIGN_TIME)
        self.robot.stop()
        wait(self.WAIT_TIME)
        self.drive_forward(-self.PUSH_AWAY, False)

    def align_backwards(self):
        self.init_robot()
        print("Align Backwards")
        self.robot.stop()
        self.robot.drive(-50, 0)
        wait(self.ALIGN_TIME)
        self.robot.stop()
        wait(self.WAIT_TIME)
        self.drive_forward(self.PUSH_AWAY, False)
    
    def _get_consistent_distance(self, direction_string: str):
        distance_1 = get_distance()
        print("Distance {}-1: {}".format(direction_string, distance_1))
        wait(self.WAIT_TIME)
        distance_2 = get_distance()
        wait(self.WAIT_TIME)
        print("Distance {}-2: {}".format(direction_string, distance_2))
        if distance_1 != distance_2:
            print("Distance values are inconsistent, rescanning...")
            return get_distance()
        return distance_1

    def scan(self, check_alignment: bool = True):
        motor_neck = Motor(Port.B)
        color = get_color()

        # Ausgangsposition: Mitte
        wait(self.WAIT_TIME)
        m_distance = self._get_consistent_distance("m")
        motor_neck.hold()
        print("Distance m: {}".format(m_distance))

        wait(self.WAIT_TIME)
        # nach links gucken
        motor_neck.run_angle(rotation_angle=-107, speed=200)
        motor_neck.hold()
        wait(self.WAIT_TIME)
        l_distance = self._get_consistent_distance("l")
        print("Distance l: {}".format(l_distance))
        wait(self.WAIT_TIME)

        # nach hinten gucken
        motor_neck.run_angle(rotation_angle=-77, speed=200)
        motor_neck.hold()
        h_distance = self._get_consistent_distance("h")
        print("Distance h: {}".format(h_distance))

        # nach rechts gucken
        motor_neck.run_angle(rotation_angle=-77, speed=200)
        motor_neck.hold()
        r_distance = self._get_consistent_distance("r")
        print("Distance r: {}".format(r_distance))

        # Zurück in die Ausgangsposition
        motor_neck.run_target(target_angle=0, speed=200)

        result = {
            "distance_m": m_distance,
            "distance_l": l_distance,
            "distance_h": h_distance,
            "distance_r": r_distance,
            "color": color
        }

        if check_alignment:
            self.check_alignment(scan_result=result)
        print(result)
        return result

    def check_alignment(self, next_instruction: str = "", scan_result: dict = None):
        self.init_robot()

        if scan_result is None:
            scan_result = self.scan(False)

        print("Checking Alignment")
        print(scan_result)

        if scan_result.get("distance_m") < 140:
            self.align_forwards()
            wait(self.ALIGN_TIME)

        if scan_result.get("distance_r") < 140:
            self.turn_left()
            wait(self.WAIT_TIME)
            self.align_backwards()
            if next_instruction != "turn_left":
                wait(self.WAIT_TIME)
                self.turn_right()
            else:
                self.skip_next_instruction = True

        elif scan_result.get("distance_l") < 140:
            self.turn_right()
            wait(self.WAIT_TIME)
            self.align_backwards()
            if next_instruction != "turn_right":
                wait(self.WAIT_TIME)
                self.turn_left()
            else:
                self.skip_next_instruction = True

    def drive_according_to_list(self, instructions):
        self.init_robot()
        print("Driving according to instruction list")
        for idx, instruction in enumerate(instructions):
            print("Step: {}: {}".format(idx + 1, instruction))

            if self.skip_next_instruction:
                self.skip_next_instruction = False
                print("Skipping step: '{}' because it was already fulfilled".format(instruction))
                continue

            if instruction == "drive_forward":
                self.drive_forward(self.STANDARD_DRIVE_DISTANCE, True)

            elif instruction == "turn_around":
                self.turn_around()

            elif instruction == "turn_left":
                self.turn_left()

            elif instruction == "turn_right":
                self.turn_right()

            wait(self.WAIT_TIME)
