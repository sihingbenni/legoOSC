from threading import Thread

from oscbrick.oscbrick import EV3
from oscbrick.config import Config

from pentagon.movement import turn_left, turn_right, turn_around, drive_forward, drive_according_to_list

STANDARD_DRIVE_DISTANCE = 300

def get_handler():
    return PentagonControlHandler()


class PentagonControlHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'pentagon':
            # Drive
            if len(path) > 1 and path[1] == 'drive':
                if len(path) > 2 and path[2] == 'forward':
                    if len(args) == 0:
                        drive_forward(STANDARD_DRIVE_DISTANCE)
                    elif len(args) == 1 and str(types_of_args) == 'i':
                        drive_forward(int(args[0]))
                    pass
                elif len(path) > 2 and path[2] == 'backward':
                    if len(args) == 0:
                        drive_forward(-STANDARD_DRIVE_DISTANCE)
                    elif len(args) == 1 and str(types_of_args) == 'i':
                        drive_forward(-int(args[0]))
                    pass
                pass
            elif len(path) > 1 and path[1] == 'turn':
                if len(path) > 2 and path[2] == 'left':
                    turn_left()
                elif len(path) > 2 and path[2] == 'right':
                    turn_right()
                elif len(path) > 2 and path[2] == 'around':
                    turn_around()
                pass

            elif len(path) > 1 and path[1] == 'runList':
                if len(args) > 0:
                    drive_according_to_list(args)
                pass

