from time import sleep

from oscbrick.config import Config, Topic
from oscbrick.oscudp import OSCUdp
from oscbrick.osctcp import OSCTcp

from pybricks.parameters import Button
from pybricks.media.ev3dev import Font
from pybricks.hubs import EV3Brick


EV3 = EV3Brick()

FONT = Font(size=15, bold=True)


class OSCBrick:

    osc_server = OSCUdp()
    osc_tcp = OSCTcp()

    def __init__(self):
        Config.register(self)

        self.show_info()

        self.osc_server.start()
        self.osc_tcp.start()

        EV3.speaker.beep()
        while Button.CENTER not in EV3.buttons.pressed():
            sleep(0.1)

        self.osc_server.stop()
        self.osc_tcp.stop()

        EV3.speaker.beep(frequency=100, duration=500)

    def config_changed(self, topic):
        self.show_info()
        if Topic.PORT == topic:
            self.osc_server.stop()

            self.osc_server = OSCUdp()
            self.osc_server.start()


    def show_info(self):
        EV3.screen.clear()
        EV3.screen.set_font(FONT)
        EV3.screen.print('Brick:')
        EV3.screen.print(' ' + Config.name())
        EV3.screen.print(' ' + Config.ip())
        EV3.screen.print(' UDP:' + str(Config.port()) + " TCP:" + str(Config.tcp_port()))
        EV3.screen.print('to:')
        EV3.screen.print(' ' + Config.target_ip() + ':' + str(Config.target_port()))


    
    