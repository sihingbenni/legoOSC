from pybricks.ev3devices import InfraredSensor

from oscbrick.oscsender import Sender, construct_path
from oscbrick.utilities import run_in_thread, string_to_port, port_to_string


def get_handler():
    return InfraredHandler()


class InfraredHandler:

    infrared_sensors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'infrared' and len(path) >= 3:
            port = string_to_port(path[1])
            print("Hallo")
            if port:
                self.create_default_infrared_sensor(port)
                print("Hallo2")
                if path[2] == 'distance' and len(args) == 0:
                    print("Hallo3")
                    run_in_thread(self.distance, port)

    def create_default_infrared_sensor(self, port):
        if port not in self.infrared_sensors:
            self.infrared_sensors[port] = InfraredSensor(port)

    def distance(self, port):
        pressed = self.infrared_sensors[port].distance()
        Sender.send(construct_path("infrared", port_to_string(port), "distance", "is"), int(pressed))