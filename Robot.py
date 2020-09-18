"""Define class and functions needed for each robot toy"""
import os
from uart_drivers import send_uart_command, read_uart_command
from DIP_drivers import import_reference_images

# BUUID for toy Robots
robot_1_addr = [0x01, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_2_addr = [0x02, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_3_addr = [0x03, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_4_addr = [0x04, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_5_addr = [0x05, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_6_addr = [0x06, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_7_addr = [0x07, 0x90, 0x70, 0xCA, 0xEA, 0x89]
robot_8_addr = [0x08, 0x90, 0x70, 0xCA, 0xEA, 0x89]

# Status for Toy Robots
CONNECTED = 1
NOT_CONNECTED = 0
IDLE = 2


class ToyRobot:
    def __init__(self, name, buuid):
        self.name = name
        self.buuid = buuid
        self.center_pos = (0, 0)
        self.status = NOT_CONNECTED
        self.conIDX = 0

    def connect_robot(self):
        return

    def send_command(self):
        return

    def read_status(self):
        return

    def locate_robot_in_field(self):
        return


class RobotsHandler:
    def __init__(self):
        self.swarm = []

    def locate_ball_in_field(self):
        return

    def calc_distance_between_robots(self):
        return

    def calc_distance_between_robot_n_ball(self):
        return

    def calc_distance_between_robot_n_goal(self):
        return


if __name__ == '__main__':
    print("Done")
