import request_pb2
from intelligent_obj import IntelligentObj
import time
from threading import Thread

MCAST_GRP = TCP_IP = 'localhost'
MCAST_PORT = 6789


class AC(IntelligentObj):

    def __init__(self):
        ac = request_pb2.AC()
        ac.type = "AC"
        ac.temp = -1
        super().__init__("ac", ac)
        commands_map = { "turn_on":self.turn_on, "turn_off":self.turn_off,"change_temp":self.change_temp }
        self.fill_cmd_list(commands_map.keys())
        Thread(target=self.wait_for_command, args=(commands_map,)).start()

    def turn_on(self):
        self.obj.status = True
        self.send_status()

    def turn_off(self):
        self.obj.status = False
        self.send_status()

    def change_temp(self, temp):

        temp_bck = self.obj.temp

        try:
            temp_bck = int(temp)
        except:
            print("Invalid Temperature")
            
        self.obj.temp = temp_bck
        self.send_status()

    def to_str(self):
        print(self.obj.status)
        print(self.obj.type)
        print(self.obj.temp)

    # def notify_presence(self, ip, port):
    #     super().notify_presence(ip, port)
    #     time.sleep(0.5)
    #     self.send_status()