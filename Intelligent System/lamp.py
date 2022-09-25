import request_pb2
import socket
from threading import Thread
from threading import Lock


MCAST_GRP = 'localhost'
MCAST_PORT = 6789


class Lamp:
    def __init__(self, color):
        self.lamp = request_pb2.Lamp()
        self.lamp.type = "Lamp"
        self.lamp.color = color
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((MCAST_GRP, MCAST_PORT))
        Thread(target=self.wait_for_call, args=()).start()

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

    def notify_presence(self):
        msg = "Sou uma lâmpada inteligente"
        self.sock.sendto(bytes(msg, 'utf-8'), (MCAST_GRP, MCAST_PORT))

    def wait_for_call(self):
        while True:
            cmd = self.sock.recv(1024).decode('utf-8')
            if (cmd == "Identifique-se"):
                print("ok")
