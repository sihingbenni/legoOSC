
SAY = False


def log_and_say(string: str):
    print(string)
    if SAY:
        ev3.speaker.say(string)
