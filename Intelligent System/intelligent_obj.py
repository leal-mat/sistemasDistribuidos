import request_pb2
import socket
from threading import Thread
from utils import Port
from threading import Lock
import struct
import json

MCAST_ADDR = ('225.0.0.250', 5007)
TCP_IP = '127.0.0.1'
MCAST_PORT = 6789

# multicast_group = '225.0.0.250'
# server_address = ('', 10000)


class IntelligentObj:
    def __init__(self):
        self.type = ""
        self.mcast_sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.bind((TCP_IP, 0))
        self.connected = False
        Thread(target=self.wait_for_call, args=()).start()

    def notify_presence(self, ip, port):
        print("entrou no notify presence - ", self.type)
        TCP_PORT = self.sock_tcp.getsockname()[1]
        id = {"type": self.type, "ip": TCP_IP, "port": TCP_PORT}

        if not self.connected:
            self.sock_tcp.connect((ip, port))
            self.sock_tcp.sendall(bytes(json.dumps(id), "utf-8"))
            self.connected = True

    def wait_for_call(self):

        self.mcast_sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("--->>>PRINTANDO ADDR: ", MCAST_ADDR)
        self.mcast_sock.bind(MCAST_ADDR)

        mreq = struct.pack('4sl', socket.inet_aton(
            MCAST_ADDR[0]), socket.INADDR_ANY)
        self.mcast_sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            print("Waiting: ", self.type)
            data = self.mcast_sock.recv(10240)
            cmd = json.loads(data.decode('utf-8'))
            print(cmd)
            self.notify_presence(cmd["ip"], cmd["port"])
            # cmd = json.loads(self.sock.recv(1024).decode('utf-8'))
            # self.notify_presence(cmd["ip"], cmd["port"])
