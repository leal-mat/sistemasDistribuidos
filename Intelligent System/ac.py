import request_pb2
import socket
from threading import Thread
from utils import Port
from threading import Lock
import json
from intelligent_obj import IntelligentObj

MCAST_GRP = TCP_IP = 'localhost'
MCAST_PORT = 6789


class AC(IntelligentObj):

    def __init__(self):
        self.ac = request_pb2.AC()
        self.ac.type = "AC"
        self.ac.temp = -1
        super().__init__()
        self.type = "AC"

    def turn_on(self):
        self.ac.status = True

    def turn_off(self):
        self.ac.status = False

    def change_temp(self, temp):
        self.ac.temp = temp

    def get(self):
        return self.ac

    def to_str(self):
        print(self.ac.status)
        print(self.ac.type)
        print(self.ac.temp)
