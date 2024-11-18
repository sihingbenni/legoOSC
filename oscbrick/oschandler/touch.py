from time import sleep
from pybricks.ev3devices import TouchSensor

from oscbrick.oscsender import Sender, construct_path
from oscbrick.utilities import run_in_thread, string_to_port, port_to_string


def get_handler():
    return TouchHandler()


class TouchHandler:

    touch_sensors = dict()

    def handle(self, path, types_of_args, args):
        if path[0] == 'touch' and len(path) >= 2 and len(args) == 0:
            port = string_to_port(path[1])
            if port:
                self.create_default_touch_sensor(port)
                if len(path) == 2:
                    run_in_thread(self.touch, port)
                elif len(path) >= 3 and path[2] == 'onchange':
                    if path[3] == 'stop':
                        self.stop_polling(port)
                    elif path[3] == 'start':
                        run_in_thread(self.start_polling, port)


    def create_default_touch_sensor(self, port):
        if port not in self.touch_sensors:
            self.touch_sensors[port] = TouchSensor(port)

    def touch(self, port):
        pressed = self.touch_sensors[port].pressed()
        Sender.send(construct_path("touch", port_to_string(port), "pressed"), bool(pressed))


    touch_polling = dict()
    def start_polling(self, port):
        if port not in self.touch_polling:
            self.touch_polling[port] = True
            old_pressed = None
            while(self.touch_polling[port]):
                pressed = self.touch_sensors[port].pressed()
                if pressed != old_pressed:
                    Sender.send(construct_path("touch", port_to_string(port),"changed", "pressed"), bool(pressed))
                old_pressed = pressed
                sleep(0.01)
            del self.touch_polling[port]

    def stop_polling(self, port):
        if port in self.touch_polling:
            self.touch_polling[port] = False
