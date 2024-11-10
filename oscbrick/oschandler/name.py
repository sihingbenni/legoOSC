from oscbrick.config import Config
from oscbrick.oscsender import Sender, construct_path_without_name


def get_handler():
    return NameHandler()


class NameHandler:
    def handle(self, path, types_of_args, args):
        if path[0] == 'name' and len(path) == 1:
            if len(args) == 0:
                Sender.send(construct_path_without_name(Config.ip(), "name", "current"), Config.name())
            elif len(args) == 1 and str(args[0]) != Config.name():
                old_name = Config.name()
                Config.set_name(str(args[0]))
                Sender.send(construct_path_without_name(old_name, "name", "changed"), Config.name())
