from threading import Thread

from oscbrick.oscbrick import EV3
from oscbrick.config import Config


def get_handler():
    return BeepHandler()


class BeepHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'beep':
            if len(path) == 1:
                if len(args) == 0:
                    server_thread = Thread(target=self.beep, args=())
                    server_thread.start()
                elif len(args) == 1 and str(types_of_args) == 'i':
                    server_thread = Thread(target=self.beep, args=(500,int(args[0])))
                    server_thread.start()
                elif len(args) == 2 and str(types_of_args) == 'ii':
                    server_thread = Thread(target=self.beep, args=(int(args[1]),int(args[0])))
                    server_thread.start()
            if len(path) == 2 and path[1] == "volume":
                if len(args) == 1:
                    EV3.speaker.set_volume(int(args[0]), 'Beep')

    def beep(self, frequency=500, duration=100):
        EV3.speaker.beep(frequency, duration)