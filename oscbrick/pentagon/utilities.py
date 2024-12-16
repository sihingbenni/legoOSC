from threading import Thread


def run_in_thread(function, *arguments):
    server_thread = Thread(target=function, args=arguments)
    server_thread.start()
