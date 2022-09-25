import request_pb2
import socket
from threading import Thread
from threading import Lock


MCAST_GRP = 'localhost'
MCAST_PORT = 6789


class Treadmill:
    def __init__(self):
        self.treadmill = request_pb2.Treadmill()
        self.treadmill.type = "Treadmill"
        self.treadmill.dist = 0.0
        self.treadmill.vel = 0.0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((MCAST_GRP, MCAST_PORT))
        Thread(target=self.wait_for_call, args=()).start()

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

    def notify_presence(self):
        msg = "Sou uma esteira inteligente"
        self.sock.sendto(bytes(msg, 'utf-8'), (MCAST_GRP, MCAST_PORT))

    def wait_for_call(self):
        while True:
            cmd = self.sock.recv(1024).decode('utf-8')
            if (cmd == "Identifique-se"):
                print("ok")
