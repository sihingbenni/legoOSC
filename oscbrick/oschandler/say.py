from threading import Thread

from oscbrick.oscbrick import EV3
from oscbrick.utilities import run_in_thread


def get_handler():
    return SayHandler()


class SayHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'say':
            if len(path) == 1 and len(args) == 1:
                run_in_thread(self.say, str(args[0]))
            elif len(path) == 2:
                if path[1] == "volume" and len(args) == 1:
                    EV3.speaker.set_volume(int(args[0]), 'PCM')
                elif path[1] == "language" and len(args) == 1:
                    EV3.speaker.set_speech_options(language=str(args[0]))
                elif path[1] == "voice" and len(args) == 1:
                    EV3.speaker.set_speech_options(voice=str(args[0]))
                elif path[1] == "speed" and len(args) == 1:
                    EV3.speaker.set_speech_options(speed=int(args[0]))
                elif path[1] == "pitch" and len(args) == 1:
                    EV3.speaker.set_speech_options(pitch=int(args[0]))

    def say(self, text):
        EV3.speaker.say(text)