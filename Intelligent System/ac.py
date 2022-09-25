import request_pb2


class AC:
    def __init__(self):
        self.ac = request_pb2.AC()
        self.ac.type = "AC"
        self.ac.temp = -1

    def turn_on(self):
        self.ac.status = True

    def turn_off(self):
        self.ac.status = False

    def change_temp(self, temp):
        self.ac.temp = temp

    def get(self):
        return self.ac

    def to_str(self):
        print(self.ac.status)
        print(self.ac.type)
        print(self.ac.temp)


ac = AC()

ac.turn_on()
ac.to_str()
