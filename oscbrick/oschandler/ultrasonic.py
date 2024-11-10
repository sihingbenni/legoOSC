from pybricks.ev3devices import  UltrasonicSensor

from oscbrick.oscsender import Sender, construct_path
from oscbrick.utilities import run_in_thread, string_to_port, port_to_string


def get_handler():
    return UltrasonicHandler()


class UltrasonicHandler:

    ultrasonic_sensors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'ultrasonic' and len(path) >= 3:
            port = string_to_port(path[1])
            if port:
                self.create_default_ultrasonic_sensor(port)
                if len(path) == 3 and len(args) == 0:
                    if path[2] == 'distance':
                        run_in_thread(self.distance, port)
                    elif path[2] == 'others':
                        run_in_thread(self.others, port)
                elif len(path) == 4 and len(args) == 0 and path[2] == 'distance' and path[3] == 'silent':
                        run_in_thread(self.distance, port, True)

    def create_default_ultrasonic_sensor(self, port):
        if port not in self.ultrasonic_sensors:
            self.ultrasonic_sensors[port] = UltrasonicSensor(port)

    def distance(self, port, silent=False):
        distance = self.ultrasonic_sensors[port].distance(silent)
        Sender.send(construct_path("ultrasonic", port_to_string(port), "distance", "is"), int(distance))

    def others(self, port):
        others = self.ultrasonic_sensors[port].presence()
        Sender.send(construct_path("ultrasonic", port_to_string(port), "others", "exist"), bool(others))