import request_pb2


class Response:
    def __init__(self):
        self.response = request_pb2.Response()

    def add_lamp(self, lamp):
        self.response.lamps.append(lamp)

    def add_treadmill(self, treadmill):
        self.response.treadmills.append(treadmill)

    def add_ac(self, ac):
        self.response.acs.append(ac)

    def get(self):
        return self.response
