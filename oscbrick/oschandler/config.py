from oscbrick.config import Config

def get_handler():
    return ConfigHandler()


class ConfigHandler:
    def handle(self, path, types_of_args, args):
        if len(path) == 2 and path[0] == 'config':
            if   path[1] == 'save':
                Config.save()
            elif path[1] == 'load':
                Config.load()
            elif path[1] == 'reset':
                Config.reset()
