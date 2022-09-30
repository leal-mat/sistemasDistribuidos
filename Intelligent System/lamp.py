import request_pb2
import socket
import json
from threading import Thread
from threading import Lock
from intelligent_obj import IntelligentObj


MCAST_GRP = TCP_IP = 'localhost'
MCAST_PORT = 6789


class Lamp(IntelligentObj):
    def __init__(self, color):
        self.lamp = request_pb2.Lamp()
        self.lamp.type = "Lamp"
        self.lamp.color = color
        super().__init__()
        self.type = "Lamp"

    def turn_on(self):
        self.lamp.status = True

    def turn_off(self):
        self.lamp.status = False

    def change_color(self, color):
        self.lamp.color = color

    def get(self):
        return self.lamp

    def to_str(self):
        print(self.lamp.status)
        print(self.lamp.type)
        print(self.lamp.color)
