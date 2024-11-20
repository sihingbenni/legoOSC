from pybricks.ev3devices import GyroSensor

from oscbrick.oscsender import Sender, construct_path
from oscbrick.utilities import run_in_thread, string_to_port, port_to_string


def get_handler():
    return GyroscopeHandler()


class GyroscopeHandler:

    gyroscope_sensors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'gyroscope' and len(path) == 3:
            port = string_to_port(path[1])
            if port:
                self.create_default_gyroscope_sensor(port)
                if len(args) == 0:
                    if path[2] == 'speed':
                        run_in_thread(self.speed, port)
                    elif path[2] == 'angle':
                        run_in_thread(self.angle, port)
                elif len(args) == 1 and path[2] == 'angle':
                        run_in_thread(self.set_angle, port, int(args[0]))

    def create_default_gyroscope_sensor(self, port):
        if port not in self.gyroscope_sensors:
            self.gyroscope_sensors[port] = GyroSensor(port)

    def speed(self, port):
        speed = self.gyroscope_sensors[port].speed()
        Sender.send(construct_path("gyroscope", port_to_string(port), "speed", "is"), int(speed))

    def angle(self, port):
        angle = self.gyroscope_sensors[port].angle()
        Sender.send(construct_path("gyroscope", port_to_string(port), "angle", "is"), int(angle))

    def set_angle(self, port, angle):
        self.gyroscope_sensors[port].reset_angle(angle)
        Sender.send(construct_path("gyroscope", port_to_string(port), "angle", "is"), int(angle))

