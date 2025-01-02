from threading import Thread

from oscbrick.oscbrick import EV3
from oscbrick.config import Config
from oscbrick.oscsender import Sender, construct_path

from pybricks.parameters import Color

from oscbrick.pentagon.movement import turn_left, turn_right, turn_around, drive_forward, drive_according_to_list, \
    STANDARD_DRIVE_DISTANCE, scan

from oscbrick.utilities import run_in_thread


def get_handler():
    return PentagonControlHandler()


class PentagonControlHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'pentagon':
            print("Handling pentagon control")
            # Drive
            if len(path) > 1 and path[1] == 'drive':
                print("pentagon drive")
                if len(path) > 2 and path[2] == 'forward':
                    print("pentagon drive forward")
                    if len(args) == 0:
                        run_in_thread(drive_forward, STANDARD_DRIVE_DISTANCE)
                        Sender.send(construct_path('pentagon', 'response', 'drive', 'forward', 'done'))
                    elif len(args) == 1 and str(types_of_args) == 'i':
                        run_in_thread(drive_forward, int(args[0]))
                        Sender.send(construct_path('pentagon', 'response', 'drive', 'forward', 'done'))
                    pass
                elif len(path) > 2 and path[2] == 'backward':
                    print("pentagon drive backward")
                    if len(args) == 0:
                        run_in_thread(drive_forward, -STANDARD_DRIVE_DISTANCE)
                        Sender.send(construct_path('pentagon', 'response', 'drive', 'backward', 'done'))
                    elif len(args) == 1 and str(types_of_args) == 'i':
                        run_in_thread(drive_forward, -int(args[0]))
                        Sender.send(construct_path('pentagon', 'response', 'drive', 'backward', 'done'))
                    pass
                pass
            elif len(path) > 1 and path[1] == 'turn':
                print("pentagon turn")
                if len(path) > 2 and path[2] == 'left':
                    print("pentagon turn left")
                    run_in_thread(turn_left)
                    Sender.send(construct_path('pentagon', 'response', 'turn', 'left', 'done'))
                elif len(path) > 2 and path[2] == 'right':
                    print("pentagon turn right")
                    run_in_thread(turn_right)
                    Sender.send(construct_path('pentagon', 'response', 'turn', 'right', 'done'))
                elif len(path) > 2 and path[2] == 'around':
                    print("pentagon turn around")
                    run_in_thread(turn_around)
                    Sender.send(construct_path('pentagon', 'response', 'turn', 'around', 'done'))
                pass
            elif len(path) > 1 and path[1] == 'scan':
                print("pentagon scan")

                try:
                    result = scan()
                    Sender.send(construct_path('pentagon', 'response', 'scan', 'done'), result.get("distance_r"),
                            result.get("distance_m"), result.get("distance_l"), str(result.get("color")))
                except:
                    print("ERROR")
                    return
                
            elif len(path) > 1 and path[1] == 'runList':
                print("pentagon runList")
                if len(args) > 0:
                    run_in_thread(drive_according_to_list,args)
                    Sender.send(construct_path('pentagon', 'response', 'runList', 'done'))
                pass
