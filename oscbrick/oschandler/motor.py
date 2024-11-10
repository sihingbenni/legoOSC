from threading import Thread

from pybricks.ev3devices import Motor
from pybricks.parameters import Stop

from oscbrick.utilities import string_to_ports, port_to_string, string_to_stop, run_in_thread
from oscbrick.oscsender import Sender, construct_path


def get_handler():
    return MotorHandler()


class MotorHandler:

    motors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'motor' and len(path) >= 3:
            ports = string_to_ports(path[1])
            for i, port in enumerate(ports):
                if port:
                    if path[2] == 'configure':
                        # Todo
                        pass
                    else:
                        self.create_default_motor(port)
                        if path[2] == 'stop':
                            run_in_thread(self.motor_stop, port)
                        elif path[2] == 'brake':
                            run_in_thread(self.motor_brake, port)
                        elif path[2] == 'hold':
                            run_in_thread(self.motor_hold, port)
                        elif path[2] == 'angle' and len(path) == 3:
                            if len(args) == 0:
                                run_in_thread(self.send_motor_angle, port)
                            elif len(args) == 1:
                                run_in_thread(self.set_motor_angle, port, args[0])
                        elif path[2] == 'run':
                            self.handle_run(path, types_of_args, args, port)
                        elif path[2] == 'multirun':
                            if len(path) == 4 and path[3] == 'target':
                                if len(args) == len(ports)+1:
                                    run_in_thread(self.motor_run_target, port, int(args[0]), int(args[1+i]))
                                elif len(args) == len(ports)+2:
                                    then = string_to_stop(args[len(ports)+1])
                                    if then:
                                        run_in_thread(self.motor_run_target, port, int(args[0]), int(args[1+i]), then )

    def handle_run(self, path, types_of_args, args, port):
        if len(path) == 3 and len(args) == 1:
            run_in_thread(self.motor_run, port, int(args[0]))
        elif len(path) == 4 and path[3] == 'until_stalled':
            if len(args) == 1:
                run_in_thread(self.motor_run_until_stalled, port, int(args[0]))
            elif len(args) == 3:
                then = string_to_stop(args[1])
                limit = max(0, min(100, int(args[2])))
                if then:
                    run_in_thread(self.motor_run_until_stalled, port, int(args[0]), then, limit)
        elif len(path) == 4 and path[3] == 'target':
            if len(args) == 2:
                run_in_thread(self.motor_run_target, port, int(args[0]), int(args[1]))
            elif len(args) == 3:
                then = string_to_stop(args[2])
                if then:
                    run_in_thread(self.motor_run_target, port, int(args[0]), int(args[1]), then )

    def create_default_motor(self, port):
        if port not in self.motors:
            self.motors[port] = Motor(port)

    def send_motor_angle(self, port):
        Sender.send(construct_path("motor", port_to_string(port), "angle", "at"), self.motors[port].angle())

    def set_motor_angle(self, port, angle):
        self.motors[port].reset_angle(angle)
        self.send_motor_angle(port)

    def motor_stop(self, port):
        self.motors[port].stop()

    def motor_brake(self, port):
        self.motors[port].brake()

    def motor_hold(self, port):
        self.motors[port].hold()

    def motor_run(self, port, speed):
        self.motors[port].run(speed)

    def motor_run_until_stalled(self, port, speed, then=Stop.COAST, duty_limit=None):
        degree_stalled = self.motors[port].run_until_stalled(speed, then, duty_limit)
        Sender.send(construct_path("motor", port_to_string(port), "stalled"), degree_stalled)

    def motor_run_target(self, port, speed, angle, then=Stop.COAST):
        self.motors[port].run_target(speed, angle, then)
        Sender.send(construct_path("motor", port_to_string(port), "reached", "target"), angle)
