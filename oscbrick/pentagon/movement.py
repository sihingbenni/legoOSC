from pybricks.tools import wait
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.robotics import DriveBase

from oscbrick.pentagon.scanner import get_color, get_distance
from oscbrick.utilities import run_in_thread

STANDARD_DRIVE_DISTANCE = 300

class LookingDirection:
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]

    def __init__(self, direction: str = None):
        if direction:
            self.current_direction = direction
        else:
            self.current_direction = "NORTH"

    def turn_right(self):
        directions = self.directions
        idx_next = (directions.index(self.current_direction) + 1) % len(directions)
        self.current_direction = directions[idx_next]

    def turn_left(self):
        directions = self.directions
        idx_next = (directions.index(self.current_direction) - 1) % len(directions)
        self.current_direction = directions[idx_next]

    def turn_around(self):
        directions = self.directions
        idx_next = (directions.index(self.current_direction) + 2) % len(directions)
        self.current_direction = directions[idx_next]


motor_left = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
motor_right = Motor(Port.D)

motor_neck = Motor(Port.B)

looking_direction = LookingDirection()
skip_next_instruction = False

robot = DriveBase(motor_left, motor_right, wheel_diameter=56, axle_track=47.7)
print("Base Settings:", robot.settings())
robot.settings(100, 50, 90, 180)
print("New Settings:", robot.settings())

base_speed = 100


def turn_right():
    looking_direction.turn_right()
    print("Turning right!")
    robot.stop()
    robot.turn(90)


def turn_left():
    looking_direction.turn_left()
    print("Turning left!")
    robot.stop()
    robot.turn(-90)


def turn_around():
    looking_direction.turn_around()
    print("Turning around!")
    robot.stop()
    robot.turn(180)


def spin():
    print("You spin my head right round right round")
    robot.stop()
    robot.turn(360)


def drive_forward(distance: int, is_check: bool = True, next_instruction: str = None):
    robot.stop()
    robot.straight(distance)
    if is_check:
        wait(1000)
        # check_alignment(next_instruction)


def align_forwards():
    print("Align Forwards")
    robot.stop()

    run_in_thread(motor_right.run_until_stalled, 100, Stop.BRAKE, 22)
    run_in_thread(motor_left.run_until_stalled, 100, Stop.BRAKE, 22)
    wait(1000)
    while (motor_right.speed() > 0 or motor_left.speed() > 0):
        pass
    wait(1000)
    drive_forward(-40, False)


def align_backwards():
    print("Align Backwards")
    robot.stop()

    run_in_thread(motor_right.run_until_stalled, -100, Stop.BRAKE, 23)
    run_in_thread(motor_left.run_until_stalled, -100, Stop.BRAKE, 23)
    wait(1000)
    while (motor_right.speed() < 0 or motor_left.speed() < 0):
        pass
    wait(1000)
    drive_forward(40, False)


def align_neck(isRight: bool = True):
    robot.stop()
    print("aligning the neck")
    motor_neck.reset_angle(0)
    if isRight:
        motor_neck.run_until_stalled(-200, Stop.COAST, 40)
    else:
        motor_neck.run_until_stalled(200, Stop.COAST, 40)
    motor_neck.reset_angle(0)


def scan() -> dict[str, int | Color]:
    color = get_color()

    align_neck(True)
    # Scan right
    r_distance = get_distance()
    wait(1000)
    # Turn left (to middle) and scan
    motor_neck.run_angle(200, 105)
    wait(1000)
    m_distance = get_distance()
    wait(1000)
    # Turn left (to left)
    align_neck(False)
    l_distance = get_distance()

    result = {"distance_r": r_distance, "distance_m": m_distance, "distance_l": l_distance, "color": color}

    print(result)

    return result


def check_alignment(next_instruction: str = ""):
    global skip_next_instruction
    scan_result = scan()
    print("Checking Alignment")
    print(scan_result)

    print("Alignment checker: The next instruction is {}".format(next_instruction))

    # always align to the front if possible
    if scan_result.get("distance_m") < 140:
        align_forwards()
        wait(2000)

    if scan_result.get("distance_r") < 140:
        turn_left()
        wait(1000)
        align_backwards()

        if next_instruction != "turn_left":
            wait(1000)
            turn_right()
        else:
            print("test")
            skip_next_instruction = True

    elif scan_result.get("distance_l") < 140:
        turn_right()
        wait(1000)
        align_backwards()

        if next_instruction != "turn_right":
            wait(1000)
            turn_left()
        else:
            skip_next_instruction = True


def drive_according_to_list(instructions: dict[str]):
    global skip_next_instruction

    print("Driving according to instruction list {}".format(instructions))
    for idx, instruction in enumerate(instructions):
        print("Step: {} of {}: {}".format(idx + 1, len(instructions), instruction))

        if skip_next_instruction:
            skip_next_instruction = False
            print("Skipping step: '{}' because it was already fulfilled".format(instruction))
            continue

        next_instruction = None

        if idx + 1 < len(instructions):
            next_instruction = instructions[idx + 1]

        if instruction == "drive_forward":
            drive_forward(STANDARD_DRIVE_DISTANCE, next_instruction=next_instruction)

        if instruction == "turn_around":
            turn_around()

        if instruction == "turn_left":
            turn_left()

        if instruction == "turn_right":
            turn_right()

        # wait 1s after each procedure
        wait(1000)
