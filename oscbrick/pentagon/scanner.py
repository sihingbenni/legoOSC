from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

colorSensor = ColorSensor(Port.S3)
distanceSensor = UltrasonicSensor(Port.S2)


def get_distance() -> int:
    return distanceSensor.distance()


def get_color() -> Color:
    return colorSensor.color()
