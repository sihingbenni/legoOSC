from oscbrick.config import Config


def construct_path(*parts):
    return "/" + Config.name() + "/" + "/".join(parts)


def construct_path_without_name(*parts):
    return "/" + "/".join(parts)


class _Sender:
    sender = []

    def register(self, function):
        self.sender.append(function)

    def send(self, path, *arguments):
        for f in self.sender:
            f(path, *arguments)


Sender = _Sender()
