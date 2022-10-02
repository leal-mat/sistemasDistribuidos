import json
import socket
from threading import Timer
from threading import Thread
from utils import Port
import request_pb2
from threading import Lock
from copy import deepcopy

lock = Lock()





class GateWay:

    def __init__(self, multicast_group):

        self.multicast_group  = multicast_group
        self.multcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multcast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        self.TCP_IP = 'localhost'
        self.TCP_PORT = 3500
        self.TCP_PORT_CLIENT = 3501

        self.objects_lookup = {
            "ac": request_pb2.AC,
            "treadmill": request_pb2.Treadmill,
            "lamp": request_pb2.Lamp,
        }

        self.responses = {
            "ac": request_pb2.ResponseAC,
            "treadmill": request_pb2.ResponseTreadmill,
            "lamp": request_pb2.ResponseLamp,
        }

        self.intelligent_objs = {
            "lamp": dict(), 
            "treadmill": dict(), 
            "ac": dict(),
        }

        self.client_conn = None


        self.conn_dict = dict()

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind((self.TCP_IP, self.TCP_PORT))
        self.tcp_sock.listen(1)

        self.tcp_sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock_client.bind((self.TCP_IP, self.TCP_PORT_CLIENT))
        self.tcp_sock_client.listen(1)

        self.send_identify_notice(self.multcast_sock, self.multicast_group[0], self.multicast_group[1])

        Thread(target=self.listen_objects, args=(self.tcp_sock,)).start()

        print("Antes do accept")
        self.client_conn, addr = self.tcp_sock_client.accept()
        print("Apos o accept")
        tr = Thread(target=self.wait_command, args=(self.client_conn,))
        tr.start()

    def parseMessage(self, msgType, stringMessage):

        #msgType (AC, TredMill, Lamp)
        #stringMessage mensagem sezializada (string)
        obj_type = self.objects_lookup[msgType]
        message = obj_type()
        message.ParseFromString(stringMessage)
        return message

    def update_object(self, conn, type):
        while conn is not None:
            message = conn.recv(1024)
            obj = self.parseMessage(type, message)
            with lock:
                self.conn_dict[obj.id] = conn
                self.intelligent_objs[type][obj.id] = obj
            if self.client_conn is not None:
                response = request_pb2.ResponseSingleObject()
                response.id_obj = obj.id
                if type == "lamp":
                    response.objL.CopyFrom(obj)
                if type == "treadmill":
                    response.objT.CopyFrom(obj)
                if type == "ac":
                    response.objA.CopyFrom(obj)

                self.client_conn.sendall(response.SerializeToString())

    def wait_identifier(self, conn):

        response = json.loads(conn.recv(1024).decode('utf-8'))
        Thread(target = self.update_object, args = (conn, response["type"])).start()
        print(response)


    def send_identify_notice(self, sock, ip, port):

        msg = {
            "ip": 'localhost',
            "port": self.TCP_PORT
        }

        m_g = (ip, port)
        Timer(5.0, self.send_identify_notice, args=(sock, ip, port)).start()
        sock.sendto(bytes(json.dumps(msg), 'utf-8'), m_g)


    def listen_objects(self, sock):
        while True:
            conn, addr = sock.accept()
            tr = Thread(target=self.wait_identifier, args=(conn,))
            tr.start()

    def build_response(self):

        response = request_pb2.Response()
        
        with lock:
            # lamp_keys = self.intelligent_objs["lamp"].keys()
            # treadmill_keys = self.intelligent_objs["treadmill"].keys()
            # ac_keys = self.intelligent_objs["ac"].keys()

            # for lamp in list(lamp_keys):
            #     response.lamps.append(self.intelligent_objs["lamp"].pop(lamp))

            # for treadmill in list(treadmill_keys):
            #     response.treadmills.append(self.intelligent_objs["treadmill"].pop(treadmill))

            # for ac in list(ac_keys):
            #     response.acs.append(self.intelligent_objs["ac"].pop(ac))

            

            for lamp in self.intelligent_objs["lamp"].values():
                response.lamps.append(lamp)

            for treadmill in self.intelligent_objs["treadmill"].values():
                response.treadmills.append(treadmill)
            
            for ac in self.intelligent_objs["ac"].values():
                response.acs.append(ac)

        return response.SerializeToString()

    def wait_command(self, conn):
        print("Antes while")
        print(conn)
        while conn is not None:
            print("Antes receber")
            cmd = conn.recv(1024)
            request = request_pb2.Request()
            request.ParseFromString(cmd)
            print(request.cmd)
            if request.cmd == "getall":
                conn.sendall(self.build_response())
            else:
                print("ELSE")
                with lock:
                    conn_tcp = self.conn_dict[request.id_obj]
                conn_tcp.sendall(cmd)

multicast_group = ('225.0.0.250', 5007)
gatway = GateWay(multicast_group)
# objects_lookup = {
#     "ac": request_pb2.AC,
#     "treadmill": request_pb2.Treadmill,
#     "lamp": request_pb2.Lamp,
# }

# intelligent_objs = {
#     "lamp": dict(), 
#     "treadmill": dict(), 
#     "ac": dict(),
# }

# conn_dict = dict()


# multicast_group = ('225.0.0.250', 5007)
# MULTICAST_TTL = 2

# multcast_sock = socket.socket(
#     socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# multcast_sock.setsockopt(
#     socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

# TCP_IP = 'localhost'
# TCP_PORT = 3500
# TCP_PORT_CLIENT = 3501

# msg = {
#     "ip": 'localhost',
#     "port": TCP_PORT
# }

# def parseMessage(msgType, stringMessage):

#         #msgType (AC, TredMill, Lamp)
#         #stringMessage mensagem sezializada (string)
#         obj_type = objects_lookup[msgType]
#         message = obj_type()
#         message.ParseFromString(stringMessage)
#         return message

# def update_object(conn, type):
#     while conn is not None:
#         message = conn.recv(1024)
#         obj = parseMessage(type, message)
#         with lock:
#             conn_dict[obj.id] = conn
#             intelligent_objs[type][obj.id] = obj

# def wait_identifier(conn):

#     response = json.loads(conn.recv(1024).decode('utf-8'))
#     #value = {"conn":conn, "obj": None, }

#     #(type, ip, port)
#     #obj_dict = intelligent_objects[response["type"]]
#     #obj_dict[id_obj] = value
#     #obj_dict.append(value)
#     #obj_dict[]
#     #index = len(obj_dict) - 1
#     Thread(target = update_object, args = (conn, response["type"])).start()
#     print(response)

# def send_identify_notice(sock, ip, port):
#     m_g = (ip, port)
#     Timer(5.0, send_identify_notice, args=(sock, ip, port)).start()
#     sock.sendto(bytes(json.dumps(msg), 'utf-8'), m_g)

# def listen_objects(sock):
#     while True:
#         conn, addr = sock.accept()
#         tr = Thread(target=wait_identifier, args=(conn,))
#         tr.start()


# def build_response():

#     response = request_pb2.Response()
    
#     with lock:
#         lamp_keys = intelligent_objs["lamp"].keys()
#         treadmill_keys = intelligent_objs["treadmill"].keys()
#         ac_keys = intelligent_objs["ac"].keys()

#         for lamp in list(lamp_keys):
#             response.lamps.append(intelligent_objs["lamp"].pop(lamp))

#         for treadmill in list(treadmill_keys):
#             response.treadmills.append(intelligent_objs["treadmill"].pop(treadmill))

#         for ac in list(ac_keys):
#             response.acs.append(intelligent_objs["ac"].pop(ac))

#     # for lamp in intelligent_objs["lamp"].values():
#     #     response.lamps.append(lamp["obj"])

#     # for treadmill in intelligent_objs["treadmill"].values():
#     #     response.treadmills.append(treadmill["obj"])
        
#     # for ac in intelligent_objs["ac"].values():
#     #     response.acs.append(ac["obj"])

#     return response.SerializeToString()

# def wait_command(conn):
#     print("Antes while")
#     print(conn)
#     while conn is not None:
#         print("Antes receber")
#         cmd = conn.recv(1024)
#         request = request_pb2.Request()
#         request.ParseFromString(cmd)
#         print(request.cmd)
#         if request.cmd == "getall":
#             conn.sendall(build_response())
#         else:
#             print("ELSE")
#             with lock:
#                 conn_tcp = conn_dict[request.id_obj]

#             #while 
#             conn_tcp.sendall(cmd)
#             #conn.sendall()
#         #print(request)
#         #print(f"{request.cmd}, {request.id_obj}, {request.args}")

# tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_sock.bind((TCP_IP, TCP_PORT))
# tcp_sock.listen(1)

# tcp_sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_sock_client.bind((TCP_IP, TCP_PORT_CLIENT))
# tcp_sock_client.listen(1)

# send_identify_notice(multcast_sock, multicast_group[0], multicast_group[1])

# Thread(target=listen_objects, args=(tcp_sock,)).start()

# conn, addr = tcp_sock_client.accept()
# tr = Thread(target=wait_command, args=(conn,))
# tr.start()


























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
