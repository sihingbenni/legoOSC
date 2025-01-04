from threading import Thread
from oscbrick.oscsender import Sender, construct_path

from oscbrick.pentagon.movement import RobotController  # Importiere die Klasse

def get_handler():
    return PentagonControlHandler()


class PentagonControlHandler:
    def __init__(self):
        self.robot_controller = RobotController()  # Instanz der RobotController-Klasse

    def handle(self, path, types_of_args, args):
        if path[0] == 'pentagon':
            print("Handling pentagon control")
            try:
                # Drive
                if len(path) > 1 and path[1] == 'drive':
                    print("pentagon drive")
                    if len(path) > 2 and path[2] == 'forward':
                        print("pentagon drive forward")
                        try:
                            if len(args) == 0:
                                self.robot_controller.drive_forward(self.robot_controller.STANDARD_DRIVE_DISTANCE, False)
                                Sender.send(construct_path('pentagon', 'response', 'drive', 'forward', 'done'))
                            elif len(args) == 1 and str(types_of_args) == 'i':
                                self.robot_controller.drive_forward(int(args[0]), False)
                                Sender.send(construct_path('pentagon', 'response', 'drive', 'forward', 'done'))
                        except Exception as e:
                            print("Drive Forward Error: {0}".format(e))
                            Sender.send(construct_path('pentagon', 'response', 'drive', 'forward', 'error'))

                    elif len(path) > 2 and path[2] == 'backward':
                        print("pentagon drive backward")
                        try:
                            if len(args) == 0:
                                self.robot_controller.drive_forward(-self.robot_controller.STANDARD_DRIVE_DISTANCE, False)
                                Sender.send(construct_path('pentagon', 'response', 'drive', 'backward', 'done'))
                            elif len(args) == 1 and str(types_of_args) == 'i':
                                self.robot_controller.drive_forward(-int(args[0]), False)
                                Sender.send(construct_path('pentagon', 'response', 'drive', 'backward', 'done'))
                        except Exception as e:
                            print("Drive Backward Error: {0}".format(e))
                            Sender.send(construct_path('pentagon', 'response', 'drive', 'backward', 'error'))

                elif len(path) > 1 and path[1] == 'turn':
                    print("pentagon turn")
                    if len(path) > 2 and path[2] == 'left':
                        print("pentagon turn left")
                        try:
                            self.robot_controller.turn_left()
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'left', 'done'))
                        except Exception as e:
                            print("Turn Left Error: {0}".format(e))
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'left', 'error'))

                    elif len(path) > 2 and path[2] == 'right':
                        print("pentagon turn right")
                        try:
                            self.robot_controller.turn_right()
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'right', 'done'))
                        except Exception as e:
                            print("Turn Right Error: {0}".format(e))
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'right', 'error'))

                    elif len(path) > 2 and path[2] == 'around':
                        print("pentagon turn around")
                        try:
                            self.robot_controller.turn_around()
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'around', 'done'))
                        except Exception as e:
                            print("Turn Around Error: {0}".format(e))
                            Sender.send(construct_path('pentagon', 'response', 'turn', 'around', 'error'))

                elif len(path) > 1 and path[1] == 'scan':
                    print("pentagon scan")
                    try:
                        result = self.robot_controller.scan(check_alignment=False)
                        Sender.send(construct_path('pentagon', 'response', 'scan', 'done'),
                                    result.get("distance_r"),
                                    result.get("distance_m"),
                                    result.get("distance_l"),
                                    result.get("distance_h"),
                                    str(result.get("color"))
                        )
                    except Exception as e:
                        print("Scan Error: {0}".format(e))
                        Sender.send(construct_path('pentagon', 'response', 'scan', 'error'))

                elif len(path) > 1 and path[1] == 'scan+align':
                    print("pentagon scan + alignment")
                    try:
                        result = self.robot_controller.scan(check_alignment=True)
                        Sender.send(construct_path('pentagon', 'response', 'scan', 'done'),
                                    result.get("distance_r"),
                                    result.get("distance_m"),
                                    result.get("distance_l"),
                                    result.get("distance_h"),
                                    str(result.get("color"))
                        )
                    except Exception as e:
                        print("Scan Error: {0}".format(e))
                        Sender.send(construct_path('pentagon', 'response', 'scan', 'error'))

                elif len(path) > 1 and path[1] == 'runList':
                    print("pentagon runList")
                    try:
                        if len(args) > 0:
                            self.robot_controller.drive_according_to_list(args)
                            Sender.send(construct_path('pentagon', 'response', 'runList', 'done'))
                    except Exception as e:
                        print("RunList Error: {0}".format(e))
                        Sender.send(construct_path('pentagon', 'response', 'runList', 'error'))

            except Exception as e:
                print("Unhandled Error: {0}".format(e))
                Sender.send(construct_path('pentagon', 'response', 'error'))
