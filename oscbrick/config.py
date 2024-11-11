import os.path
import json

from oscbrick.utilities import get_ip


class Topic:
    NAME = 'name'
    PORT = 'port'
    TARGET_IP = 'target_ip'
    TARGET_PORT = 'target_port'

def get_all_topics():
    topics = Topic()
    return tuple(attr for attr in dir(topics) if not callable(getattr(topics, attr)) and not attr.startswith("__"))


class _Config(object):
    ### <Singleton>
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_Config, cls).__new__(cls)
            cls._instance._init()
        return cls._instance
    ### </Singleton>

    _listeners = []
    def register(self, listener):
        self._listeners.append(listener)
    def _changed(self, *topic):
        for listener in self._listeners:
            try:
                listener.config_changed(*topic)
            except Exception as e:
                print("Could not inform listener " + str(listener) + " on config change " + str(topic) + ":" + str(e))

    # Configfilename
    CONFIG_FILE = 'oscbrickconfig.cfg'

    _osc_brick_config = dict()

    def _init(self):
        self.load()

    def load(self):
        if os.path.exists(self.CONFIG_FILE):
            config_file = open(self.CONFIG_FILE, 'r')
            self._osc_brick_config = json.loads(config_file.read())
            config_file.close()
            self._changed(get_all_topics())

    def save(self):
        config_file = open(self.CONFIG_FILE, 'w')
        config_file.write(json.dumps(self._osc_brick_config))
        config_file.close()

    def reset(self):
        self._osc_brick_config = dict()
        self._changed(get_all_topics())

    def name(self):
        if 'name' in self._osc_brick_config:
            return self._osc_brick_config['name']
        else:
            return "OSCBrick@" + get_ip()

    def set_name(self, name):
        self._osc_brick_config['name'] = name
        self._changed(Topic.NAME)

    def ip(self):
        return get_ip()

    def port(self):
        if 'port' in self._osc_brick_config:
            return self._osc_brick_config['port']
        else:
            return 9001

    def set_port(self, port):
        self._osc_brick_config['port'] = port
        self._changed(Topic.PORT)

    def target_ip(self):
        if 'target_ip' in self._osc_brick_config:
            return self._osc_brick_config['target_ip']
        else:
            return get_ip()[:get_ip().rfind('.') + 1] + '255'

    def set_target_ip(self, target_ip):
        self._osc_brick_config['target_ip'] = target_ip
        self._changed(Topic.TARGET_IP)

    def target_port(self):
        if 'target_port' in self._osc_brick_config:
            return self._osc_brick_config['target_port']
        else:
            return 9001

    def set_target_port(self, target_port):
        self._osc_brick_config['target_port'] = target_port
        self._changed(Topic.TARGET_PORT)


Config = _Config()