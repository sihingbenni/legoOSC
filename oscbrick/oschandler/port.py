from oscbrick.config import Config


def get_handler():
    return Port()


class Port:
    def handle(self, path, types_of_args, args):
        if len(path) == 2 and path[0] == 'port' and len(args) == 1:
            if path[1] == 'incoming':
                Config.set_port(int(args[0]))
            elif path[1] == 'target':
                Config.set_target_port(int(args[0]))