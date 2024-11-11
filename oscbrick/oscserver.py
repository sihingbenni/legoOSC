import socket
import threading
from time import sleep

from oscbrick.config import Config
from oscbrick.oscbasehandler import OSCBaseHandler

from uosc.server import handle_osc


class OSCServer:
    MAX_DGRAM_SIZE = 60000

    _running = False
    _server_thread = None
    _stopped = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(0.1)

    def start(self):
        print("Listening for OSC messages on " + str(Config.ip()) + ":" + str(Config.port()) + ".")
        self.sock.bind(("", Config.port()))

        self._running = True
        self._server_thread = threading.Thread(target=self._run, args=())
        self._server_thread.start()

    def _run(self):
        try:
            self._stopped = False
            while self._running:
                try:
                    data, caddr = self.sock.recvfrom(self.MAX_DGRAM_SIZE)
                    print("RECV", len(data), data)
                    handle_osc(data, caddr, dispatch=OSCBaseHandler().handle)
                except OSError:
                    pass
        finally:
            self.sock.close()
        self._stopped = True

    def stop(self):
        self._running = False