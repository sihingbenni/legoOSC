from oscbrick.config import Config
from oscbrick.utilities import get_modules_in_folder
from oscbrick.oscsender import Sender, construct_path_without_name, construct_path


class OSCBaseHandler(object):
    ### <Singleton>
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OSCBaseHandler, cls).__new__(cls)
            cls._instance._init()
        return cls._instance
    ### </Singleton>

    _sub_handler_set = set()

    def _init(self):
        for handler_module in get_modules_in_folder("oscbrick/oschandler", "oscbrick.oschandler"):
            try:
                self._sub_handler_set.add(handler_module.get_handler())
            except:
                print("Can not load handler from module " + str(handler_module))

    def handle(self, timetag, message):
        split_path = str(message[0]).split('/')
        target = split_path[1]
        if len(split_path) >= 3 and (target == Config.name() or target == Config.ip()):
            for sub_handler in self._sub_handler_set:
                try:
                    sub_handler.handle(split_path[2:], message[1], message[2])
                except Exception as e:
                    print('Could not handle ' + str(message) + ' with ' + str(sub_handler) + ':' + str(e))
                    Sender.send(construct_path('error'), str(message) + ': ' + str(e))
        elif len(split_path) == 3 and split_path[1] == 'oscbrick' and split_path[2] == "identify":
            Sender.send(construct_path_without_name(Config.name()), Config.ip())
