import request_pb2
import socket
import json
from threading import Thread
from threading import Lock
from intelligent_obj import IntelligentObj

MCAST_GRP = TCP_IP = 'localhost'
MCAST_PORT = 6789


class Treadmill(IntelligentObj):
    def __init__(self):
        self.treadmill = request_pb2.Treadmill()
        self.treadmill.type = "Treadmill"
        self.treadmill.dist = 0.0
        self.treadmill.vel = 0.0
        super().__init__()
        self.type = "Treadmill"

    def turn_on(self):
        self.treadmill.status = True

    def turn_off(self):
        self.treadmill.status = False

    def increase_vel(self):
        self.treadmill.vel += 5
        self.treadmill.vel = 40.0 if self.treadmill.vel > 40.0 else self.treadmill.vel

    def decrease_vel(self):
        self.treadmill.vel -= 5
        self.treadmill.vel = 0.0 if self.treadmill.vel < 0.0 else self.treadmill.vel

    def get(self):
        return self.treadmill

    def to_str(self):
        print(self.treadmill.status)
        print(self.treadmill.type)
        print(self.treadmill.dist)
        print(self.treadmill.vel)
