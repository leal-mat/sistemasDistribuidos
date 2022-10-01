import request_pb2
from intelligent_obj import IntelligentObj
import time

MCAST_GRP = TCP_IP = 'localhost'
MCAST_PORT = 6789


class AC(IntelligentObj):

    def __init__(self):
        ac = request_pb2.AC()
        ac.type = "AC"
        ac.temp = -1
        super().__init__("ac", ac)

    def turn_on(self):
        self.obj.status = True
        self.send_status()

    def turn_off(self):
        self.obj.status = False
        self.send_status()

    def change_temp(self, temp):
        self.obj.temp = temp
        self.send_status()

    def to_str(self):
        print(self.obj.status)
        print(self.obj.type)
        print(self.obj.temp)

    # def notify_presence(self, ip, port):
    #     super().notify_presence(ip, port)
    #     time.sleep(0.5)
    #     self.send_status()