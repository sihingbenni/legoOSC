from time import sleep

from oscbrick.config import Config
from oscbrick.oscserver import OSCServer

from pybricks.parameters import Button
from pybricks.media.ev3dev import Font
from pybricks.hubs import EV3Brick

EV3 = EV3Brick()

FONT = Font(size=19, bold=True)


class OSCBrick:

    oscserver = OSCServer()

    def __init__(self):
        Config.register(self)

        self.show_info()

        self.oscserver.start()

        EV3.speaker.beep()
        while Button.CENTER not in EV3.buttons.pressed():
            sleep(0.1)

        self.oscserver.stop()
        EV3.speaker.beep(frequency=100, duration=500)

    def config_changed(self, topic):
        self.show_info()

    def show_info(self):
        EV3.screen.clear()
        EV3.screen.set_font(FONT)
        EV3.screen.print('Brick:')
        EV3.screen.print(' ' + Config.name())
        EV3.screen.print(' ' + Config.ip() + ':' + str(Config.port()))
        EV3.screen.print('to:')
        EV3.screen.print(' ' + Config.target_ip() + ':' + str(Config.target_port()))


    
    