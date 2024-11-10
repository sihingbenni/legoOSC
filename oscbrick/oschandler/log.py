from time import time

from oscbrick.oscsender import Sender, construct_path


def get_handler():
    return LogHandler()


class LogHandler:

    enabled = False

    def handle(self, path, types_of_args, args):
        if path[0] == 'log' and len(args) == 1:
            self.enabled = bool(args[0])

        if self.enabled:
            seconds = int(time())
            message = str(int(seconds/60)%60) + ":" + str(seconds%60) + ":" + str(path) + " ," + types_of_args + ", " + str(args)
            print(message)
            Sender.send(construct_path('log', 'received'), message)
