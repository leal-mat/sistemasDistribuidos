import request_pb2


class Request:
    def __init__(self, cmd, id_obj, args):
        self.request = request_pb2.Request()
        self.request.cmd = cmd
        self.request.id_obj = id_obj
        self.request.args = args

    def get(self):
        return self.request

    # def add_lamp(self, lamp):
    #     self.response.lamps.append(lamp)

    # def add_treadmill(self, treadmill):
    #     self.response.treadmills.append(treadmill)

    # def add_ac(self, ac):
    #     self.response.acs.append(ac)
