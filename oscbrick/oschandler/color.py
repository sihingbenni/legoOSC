from pybricks.ev3devices import ColorSensor

from oscbrick.oscbrick import EV3
from oscbrick.oscsender import Sender, construct_path
from oscbrick.utilities import string_to_color, run_in_thread, string_to_port, port_to_string, color_to_string


def get_handler():
    return ColorHandler()


class ColorHandler:

    color_sensors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'color' and len(path) >= 2:
            port = string_to_port(path[1])
            if port:
                self.create_default_color_sensor(port)
                if len(path) == 2 and len(args) == 0:
                    run_in_thread(self.color, port)
                elif len(path) == 3 and len(args) == 0:
                    if path[2] == 'ambient':
                        run_in_thread(self.ambient, port)
                    elif path[2] == 'reflection':
                        run_in_thread(self.reflection, port)
                    elif path[2] == 'rgb':
                        run_in_thread(self.rgb, port)

    def create_default_color_sensor(self, port):
        if port not in self.color_sensors:
            self.color_sensors[port] = ColorSensor(port)

    def color(self, port):
        color = self.color_sensors[port].color()
        Sender.send(construct_path("color", port_to_string(port), "is"), color_to_string(color))

    def ambient(self, port):
        ambient = self.color_sensors[port].ambient()
        Sender.send(construct_path("color", port_to_string(port), "ambient", "is"), int(ambient))

    def reflection(self, port):
        reflection = self.color_sensors[port].reflection()
        Sender.send(construct_path("color", port_to_string(port), "reflection", "is"), int(reflection))

    def rgb(self, port):
        rgb = self.color_sensors[port].rgb()
        Sender.send(construct_path("color", port_to_string(port), "rgb", "is"), int(rgb[0]), int(rgb[1]), int(rgb[2]))