import json
import socket
from threading import Timer
from threading import Lock
import struct

TCP_IP = 'localhost'
TCP_PORT = 3000

msg = {
    "ip": 'localhost',
    "port": 3000
}


def send_identify_notice(sock, ip, port):
    Timer(5.0, send_identify_notice, args=(sock, ip, port)).start()
    print("Mandei 1")
    sock.sendto(bytes(json.dumps(msg), 'utf-8'), (ip, port))


MCAST_GRP = 'localhost'
MCAST_PORT = 6789


intelligent_objects = dict()

intelligent_objects["Lamp"] = []
intelligent_objects["Treadmill"] = []
intelligent_objects["AC"] = []


sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((TCP_IP, TCP_PORT))
sock_tcp.listen(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))


#sock.sendto(bytes(msg, 'utf-8'), (MCAST_GRP, MCAST_PORT))
send_identify_notice(sock, MCAST_GRP, MCAST_PORT)
#Thread(target=send_identify_notice, args=(sock, MCAST_GRP, MCAST_PORT)).start()
print("depois da chamda send id")

conn, addr = sock_tcp.accept()
response = conn.recv(1024).decode('utf-8')
print(response)
# while True:
#     response = sock.recv(1024).decode('utf-8')

# print(response)

sock.close()
sock_tcp.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("localhost", 6789))
# s.listen(1)


# lock = Lock()

# while True:
#     conn, addr = s.accept()
#     data_b = conn.recv(1024)
