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

        self.client_conn, addr = self.tcp_sock_client.accept()
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
        try:
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
        except:
            conn.close()
            conn = None
            print("Connection Closed")

    def wait_identifier(self, conn):

        try:
            response = json.loads(conn.recv(1024).decode('utf-8'))
            Thread(target = self.update_object, args = (conn, response["type"])).start()
            print(response)
        except:
            conn.close()
            conn = None
            print("Connection Closed")


    def send_identify_notice(self, sock, ip, port):

        msg = {
            "ip": 'localhost',
            "port": self.TCP_PORT
        }

        m_g = (ip, port)
        Timer(5.0, self.send_identify_notice, args=(sock, ip, port)).start()
        sock.sendto(bytes(json.dumps(msg), 'utf-8'), m_g)


    def listen_objects(self, sock):
        try: 
            while True:
                conn, addr = sock.accept()
                tr = Thread(target=self.wait_identifier, args=(conn,))
                tr.start()
        except:
            conn.close()
            conn = None
            print("Connection Closed")

    def build_response(self):

        response = request_pb2.Response()
        
        with lock:
            for lamp in self.intelligent_objs["lamp"].values():
                response.lamps.append(lamp)

            for treadmill in self.intelligent_objs["treadmill"].values():
                response.treadmills.append(treadmill)
            
            for ac in self.intelligent_objs["ac"].values():
                response.acs.append(ac)

        return response.SerializeToString()

    def wait_command(self, conn):
        try:
            while conn is not None:
                cmd = conn.recv(1024)
                request = request_pb2.Request()
                request.ParseFromString(cmd)
                print(request.cmd)
                if request.cmd == "getall":
                    conn.sendall(self.build_response())
                else:
                    with lock:
                        conn_tcp = self.conn_dict[request.id_obj]
                    conn_tcp.sendall(cmd)
        except:
            conn.close()
            conn = None
            print("Connection Closed")

multicast_group = ('225.0.0.250', 5007)
gatway = GateWay(multicast_group)