import os
from os.path import dirname, join
import glob
from threading import Thread

from pybricks.parameters import Port, Stop, Color

def get_ip():
    return os.popen('hostname -I').read().strip().split(" ")[0] # Thanks micropython!


def load_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def get_modules_in_folder(folder, modulebase):
    handler = glob.glob(join(folder, "*.py"))
    modules = []
    for file in handler:
        if not file.endswith('__init__.py'):
            try:
                modules.append(load_module(modulebase + "." + file.split('/')[-1].split('.')[0]))  # be evil!
            except Exception as e:
                print("Error importing handler: " + str(e))
    return modules


def port_to_string(port):
    return str(port).split('.')[-1].lower()


def string_to_port(port):
    port = str(port).upper()
    if port == 'A':
        return Port.A
    elif port == 'B':
        return Port.B
    elif port == 'C':
        return Port.C
    elif port == 'D':
        return Port.D
    elif port == 'S1':
        return Port.S1
    elif port == 'S2':
        return Port.S2
    elif port == 'S3':
        return Port.S3
    elif port == 'S4':
        return Port.S4
    return None

def string_to_ports(ports_string):
    ports = []
    for c in ports_string:
        print(c)
        ports.append(string_to_port(c))
    return ports


def string_to_color(color):
    color = str(color).upper()
    if color == 'BLACK':
        return Color.BLACK
    elif color == 'BLUE':
        return Color.BLUE
    elif color == 'GREEN':
        return Color.GREEN
    elif color == 'YELLOW':
        return Color.YELLOW
    elif color == 'RED':
        return Color.RED
    elif color == 'WHITE':
        return Color.WHITE
    elif color == 'BROWN':
        return Color.BROWN
    elif color == 'ORANGE':
        return Color.ORANGE
    elif color == 'PURPLE':
        return Color.PURPLE
    return None


def color_to_string(color):
    if type(color) is Color:
        return str(color).split('.')[-1].lower()
    else:
        return "none"

def string_to_stop(stop):
    stop = str(stop).lower()
    if stop == 'coast':
        return Stop.COAST
    elif stop == 'brake':
        return Stop.BRAKE
    elif stop == 'hold':
        return Stop.HOLD
    return None


def run_in_thread(function, *arguments):
    server_thread = Thread(target=function, args=arguments)
    server_thread.start()