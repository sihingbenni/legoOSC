
from oscbrick.oscbrick import EV3

SAY = False


def log_and_say(string: str):
    print(string)
    if SAY:
        EV3.speaker.say(string)
