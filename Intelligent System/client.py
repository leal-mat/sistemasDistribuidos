import socket
import request_pb2
from threading import Thread
from threading import Lock
lock = Lock()

TCP_IP = 'localhost'
TCP_PORT = 3501

first_connenct = request_pb2.Request()
first_connenct.cmd = "getall"
first_connenct.id_obj = "all"

intelligent_objects = dict()

def update_object_dict(sock):

    while sock is not None:
        data = sock.recv(1024)
        response = request_pb2.ResponseSingleObject()
        response.ParseFromString(data)

        obj = None

        if response.HasField("objL"):
            obj = response.objL

        if response.HasField("objT"):
            obj = response.objT

        if response.HasField("objA"):
            obj = response.objA

        with lock:
            intelligent_objects[response.id_obj] = obj


def print_response(response):
    #response = request_pb2.Response()
    print("Printando")

    objs = [*response.lamps , *response.treadmills , *response.acs]
    for obj in objs:
        intelligent_objects[obj.id] = obj
        print(f"[{obj.id}] -> {obj.type}")
        #response.lamps.append(lamp["obj"])

    #return response.SerializeToString()


def print_cmds(obj):
    print(f"is On: {obj.status}")

    print(obj.type)
    if obj.type == "Lamp":
        print(f"Color: {obj.color}")
        print("Commands: ")
        for cmd in obj.cmds:
            print(f" - {cmd}")
    if obj.type == "Treadmill":
        print(f"Velocity: {obj.vel}")
        print(f"Distance: {obj.dist}")
        print("Commands: ")
        for cmd in obj.cmds:
            print(f" - {cmd}")
    if obj.type == "AC":
        print(f"Temperature: {obj.temp}")
        print("Commands: ")
        for cmd in obj.cmds:
            print(f" - {cmd}")

    # for cmd in obj.cmds:
    #     print(f'   - {cmd}')



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(first_connenct.SerializeToString())

available_objects = s.recv(1024)


response = request_pb2.Response()
response.ParseFromString(available_objects)

Thread(target=update_object_dict, args=(s,)).start()

while True:
    print_response(response)
    obj_id = input("\nEntre qual objeto você deseja operar: ")

    obj = intelligent_objects[obj_id]
    print_cmds(obj)

    print("Ex: cmd#agr1,agr2,agr3...")
    cmd_with_args = input("Escreva o comando com os argumentos \nou 0 para voltar à seleção de dispositivos: ")

    f_split = cmd_with_args.split("#")
    cmd = f_split[0]
    args = f_split[1].split(",") if len(f_split) == 2 else []

    request = request_pb2.Request()
    request.cmd = cmd
    request.id_obj = obj_id
    request.type = obj.type.lower()
    for arg in args:
        request.args.append(arg)
    
    s.sendall(request.SerializeToString())

    print(cmd, args)



#print(available_objects)
# msg = input()
# s.sendall(bytes(msg, 'utf-8'))
# data = s.recv(1024).decode('utf-8')
#s.close()
#print('FROM SERVER: {s}'.format(s=repr(data)))
