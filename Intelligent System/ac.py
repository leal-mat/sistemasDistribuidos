import request_pb2
import socket
from threading import Thread
from threading import Lock
import json

MCAST_GRP = 'localhost'
MCAST_PORT = 6789


class AC:

    def __init__(self):
        self.ac = request_pb2.AC()
        self.ac.type = "AC"
        self.ac.temp = -1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((MCAST_GRP, MCAST_PORT))
        Thread(target=self.wait_for_call, args=()).start()

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

    def notify_presence(self, ip, port):
        print("entrou no notify presence")
        id = {"type": "AC", "ip": MCAST_GRP, "port": MCAST_PORT}

        self.sock_tcp.connect((ip, port))
        self.sock_tcp.sendall(bytes(json.dumps(id), "utf-8"))
        #self.sock.sendto(bytes("testando", "utf-8"), (MCAST_GRP, MCAST_PORT))

        #self.sock.sendto(id.SerializeToString(), (MCAST_GRP, MCAST_PORT))

    def wait_for_call(self):
        while True:
            cmd = json.loads(self.sock.recv(1024).decode('utf-8'))
            self.notify_presence(cmd["ip"], cmd["port"])
