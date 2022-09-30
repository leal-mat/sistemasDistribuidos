import json
import socket
from threading import Timer
from threading import Thread

from utils import Port

import struct
import sys

multicast_group = ('225.0.0.250', 5007)
MULTICAST_TTL = 2

multcast_sock = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
multcast_sock.setsockopt(
    socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)


# sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock1.settimeout(0.2)
# ttl = struct.pack('b', 1)
# sock1.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


def wait_identifier(conn):
    response = conn.recv(1024).decode('utf-8')
    print(response)


TCP_IP = 'localhost'
TCP_PORT = Port.get_port()


msg = {
    "ip": 'localhost',
    "port": TCP_PORT
}


def send_identify_notice(sock, ip, port):
    m_g = (ip, port)
    Timer(5.0, send_identify_notice, args=(sock, ip, port)).start()
    sock.sendto(bytes(json.dumps(msg), 'utf-8'), m_g)
    #sock.sendto(bytes(json.dumps(msg), 'utf-8'), (ip, port))

# intelligent_objects = dict()

# intelligent_objects["Lamp"] = []
# intelligent_objects["Treadmill"] = []
# intelligent_objects["AC"] = []


sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((TCP_IP, TCP_PORT))
sock_tcp.listen(1)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.bind((MCAST_GRP, MCAST_PORT))

send_identify_notice(multcast_sock, multicast_group[0], multicast_group[1])
print("depois da chamda send id")

while True:
    conn, addr = sock_tcp.accept()
    tr = Thread(target=wait_identifier, args=(conn,))
    tr.start()
    #Thread(target=waiting_messages, args=(s, connected))

# while True:
#     response = sock.recv(1024).decode('utf-8')

# print(response)

# sock.close()
# sock_tcp.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("localhost", 6789))
# s.listen(1)


# lock = Lock()

# while True:
#     conn, addr = s.accept()
#     data_b = conn.recv(1024)
