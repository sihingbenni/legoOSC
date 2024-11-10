from oscbrick.config import Config

def get_handler():
    return ErrorTest()


class ErrorTest:
    def handle(self, path, types_of_args, args):
        if path[0] == 'error' and path[0] == 'test':
            raise Exception("Dummy exception")