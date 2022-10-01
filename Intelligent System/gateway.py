import json
import socket
from threading import Timer
from threading import Thread
from utils import Port
import request_pb2
from threading import Lock

lock = Lock()


objects_lookup = {
    "ac": request_pb2.AC,
    "treadmill": request_pb2.Treadmill,
    "lamp": request_pb2.Lamp,
}

intelligent_objects = {
    "lamp": [], 
    "treadmill": [], 
    "ac":[]
}

multicast_group = ('225.0.0.250', 5007)
MULTICAST_TTL = 2

multcast_sock = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
multcast_sock.setsockopt(
    socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

TCP_IP = 'localhost'
TCP_PORT = 3500
TCP_PORT_CLIENT = 3501

msg = {
    "ip": 'localhost',
    "port": TCP_PORT
}

def parseMessage(msgType, stringMessage):

        #msgType (AC, TredMill, Lamp)
        #stringMessage mensagem sezializada (string)
        obj_type = objects_lookup[msgType]
        message = obj_type()
        message.ParseFromString(stringMessage)
        return message

def update_object(conn, index, type):

    while conn is not None:
        message = conn.recv(1024)
        obj = parseMessage(type, message)
        print("Valor do index: ",index)
        intelligent_objects[type][index]["obj"] = obj

def wait_identifier(conn):

    response = json.loads(conn.recv(1024).decode('utf-8'))
    value = {"conn":conn, "obj": None, }

    
    obj_list = intelligent_objects[response["type"]]
    obj_list.append(value)
    index = len(obj_list) - 1
    Thread(target = update_object, args = (conn, index, response["type"])).start()
    print(response)

def send_identify_notice(sock, ip, port):
    m_g = (ip, port)
    Timer(5.0, send_identify_notice, args=(sock, ip, port)).start()
    sock.sendto(bytes(json.dumps(msg), 'utf-8'), m_g)

def listen_objects(sock):
    while True:
        conn, addr = sock.accept()
        tr = Thread(target=wait_identifier, args=(conn,))
        tr.start()


def build_response():

    response = request_pb2.Response()

    for lamp in intelligent_objects["lamp"]:
        response.lamps.append(lamp["obj"])

    for treadmill in intelligent_objects["treadmill"]:
        response.treadmills.append(treadmill["obj"])
        
    for ac in intelligent_objects["ac"]:
        response.acs.append(ac["obj"])

    return response.SerializeToString()

def wait_command(conn):
    while conn is not None:
        cmd = conn.recv(1024)
        request = request_pb2.Request()
        request.ParseFromString(cmd)

        if request.cmd == "getall":
            conn.sendall(build_response())

        #print(request)
        #print(f"{request.cmd}, {request.id_obj}, {request.args}")

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((TCP_IP, TCP_PORT))
tcp_sock.listen(1)

tcp_sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock_client.bind((TCP_IP, TCP_PORT_CLIENT))
tcp_sock_client.listen(1)

send_identify_notice(multcast_sock, multicast_group[0], multicast_group[1])

Thread(target=listen_objects, args=(tcp_sock,)).start()

conn, addr = tcp_sock_client.accept()
tr = Thread(target=wait_command, args=(conn,))
tr.start()


























    #Thread(target=waiting_messages, args=(s, connected))

# while True:
#     response = sock.recv(1024).decode('utf-8')

# print(response)

# sock.close()
# tcp_sock.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("localhost", 6789))
# s.listen(1)


# lock = Lock()

# while True:
#     conn, addr = s.accept()
#     data_b = conn.recv(1024)
