from oscbrick.oscbrick import EV3
from oscbrick.utilities import string_to_color


def get_handler():
    return LightHandler()


class LightHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'light':
            if len(path) == 1 and len(args) == 1:
                EV3.light.on(string_to_color(args[0]))
            elif len(path) == 2 and path[1] == "off":
                EV3.light.off()
