from uosc.client import Client, create_message

from oscbrick.config import Config, Topic


def construct_path(*parts):
    return "/" + Config.name() + "/" + "/".join(parts)

def construct_path_without_name(*parts):
    return "/" + "/".join(parts)


class _OSCSender:
    osc_client = None

    def __init__(self):
        self._set_client()
        Config.register(self)

    def config_changed(self, topic):
        if topic == Topic.TARGET_IP or topic == Topic.TARGET_PORT:
            self.osc_client.close()
            self._set_client()

    def _set_client(self):
        self.osc_client = Client(Config.target_ip(), Config.target_port())

    def send(self, path, *arguments):
        self.osc_client.send(path, *arguments)


Sender = _OSCSender()