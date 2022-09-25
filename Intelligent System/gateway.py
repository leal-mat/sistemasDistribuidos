import socket
from threading import Thread
from threading import Lock

MCAST_GRP = 'localhost'
MCAST_PORT = 6789
msg = 'Identifique-se'

intelligent_objects = dict()

intelligent_objects["Lamp"] = []
intelligent_objects["Treadmill"] = []
intelligent_objects["AC"] = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
# sock.sendto(bytes(msg, 'utf-8'), (MCAST_GRP, MCAST_PORT))

while True:
    print(sock.recv(1024).decode('utf-8'))

sock.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("localhost", 6789))
# s.listen(1)


# lock = Lock()

# while True:
#     conn, addr = s.accept()
#     data_b = conn.recv(1024)
