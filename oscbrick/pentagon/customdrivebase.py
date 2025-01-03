import math

class CustomDriveBase:
    def __init__(self, motor_handler, motor_left_port, motor_right_port, wheel_diameter, axle_track):
        self.motor_handler = motor_handler
        self.motor_left_port = motor_left_port
        self.motor_right_port = motor_right_port
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.wheel_circumference = math.pi * wheel_diameter

    def drive_straight(self, distance_mm, speed=100):
        angle = (distance_mm / self.wheel_circumference) * 360
        self.motor_handler.motor_run_target(self.motor_left_port, speed, angle)
        self.motor_handler.motor_run_target(self.motor_right_port, speed, angle)

    def turn(self, angle_deg, speed=100):
        turn_circumference = math.pi * self.axle_track
        distance_per_wheel = (turn_circumference * angle_deg) / 360
        wheel_rotation_angle = (distance_per_wheel / self.wheel_circumference) * 360

        self.motor_handler.motor_run_target(self.motor_left_port, speed, wheel_rotation_angle)
        self.motor_handler.motor_run_target(self.motor_right_port, speed, -wheel_rotation_angle)

    def stop(self):
        self.motor_handler.motor_stop(self.motor_left_port)
        self.motor_handler.motor_stop(self.motor_right_port)
