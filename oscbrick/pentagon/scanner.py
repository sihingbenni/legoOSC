from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

colorSensor = ColorSensor(Port.S1)
distanceSensor = UltrasonicSensor(Port.S4)


def get_distance() -> int:
    return distanceSensor.distance()


def get_color() -> Color:
    return colorSensor.color()
