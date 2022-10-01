import socket
import request_pb2


TCP_IP = 'localhost'
TCP_PORT = 3501

first_connenct = request_pb2.Request()
first_connenct.cmd = "getall"
first_connenct.id_obj = "all"

def print_response(response):

    #response = request_pb2.Response()
    print("Printando")
    for lamp in response.lamps:
        print(lamp.id,  lamp.color, lamp.status)
        #response.lamps.append(lamp["obj"])

    for treadmill in response.treadmills:
        print(treadmill.id, treadmill.vel, treadmill.status)
        #response.treadmill.append(treadmill["obj"])
        
    for ac in response.acs:
        print(ac.id, ac.temp, ac.status)
        #response.ac.append(ac["obj"])

    #return response.SerializeToString()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(first_connenct.SerializeToString())

available_objects = s.recv(1024)

response = request_pb2.Response()
response.ParseFromString(available_objects)
#print(response)
print_response(response)





#print(available_objects)
# msg = input()
# s.sendall(bytes(msg, 'utf-8'))
# data = s.recv(1024).decode('utf-8')
#s.close()
#print('FROM SERVER: {s}'.format(s=repr(data)))
