from oscbrick.config import Config

def get_handler():
    return Target()


class Target:
    def handle(self, path, types_of_args, args):
        if len(path) == 1 and path[0] == 'target' and len(args) == 1:
            Config.set_target_ip(str(args[0]))
