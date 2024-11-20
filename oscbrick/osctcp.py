import socket
import threading

from oscbrick.config import Config
from oscbrick.oscbasehandler import OSCBaseHandler
from oscbrick.oscsender import Sender
from uosc.server import handle_osc
from uosc.client import create_message


class OSCTcp:
    MAX_DGRAM_SIZE = 60000

    _running = False
    _server_thread = None
    _stopped = True

    _conn = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.settimeout(3)
        Sender.register(self.send)

    def start(self):
        print("Listening for OSC connection on " + str(Config.ip()) + ":" + str(Config.tcp_port()) + ".")
        self.sock.bind((str(Config.ip()), Config.tcp_port()))

        self._running = True
        self._server_thread = threading.Thread(target=self._run, args=())
        self._server_thread.start()

    def _run(self):
        self._stopped = False
        while self._running:
            try:
                self.sock.listen(1)
                self._conn, addr = self.sock.accept()

                if self._conn:
                    self._conn.settimeout(0.1)
                    print("Connected by ", addr)
                    while self._running:
                        try:
                            data = self._conn.readline() #recv(1024)
                            if data and len(data) > 1:
                                handle_osc(data, addr, dispatch=OSCBaseHandler().handle)
                            else:
                                break
                        except OSError:
                            pass
                    self._conn.close()
                    self._conn = None
                    print("Disconnected by ", addr)
            except:
                pass
        self._stopped = True
        self.sock.close()

    def send(self, path, *arguments):
        if self._conn:
            self._conn.write(create_message(path, *arguments) + b'\n')

    def stop(self):
        self._running = False