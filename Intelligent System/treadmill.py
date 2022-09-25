import request_pb2


class Treadmill:
    def __init__(self):
        self.treadmill = request_pb2.Treadmill()
        self.treadmill.type = "Treadmill"
        self.treadmill.dist = 0.0
        self.treadmill.vel = 0.0

    def turn_on(self):
        self.treadmill.status = True

    def turn_off(self):
        self.treadmill.status = False

    def increase_vel(self):
        self.treadmill.vel += 5
        self.treadmill.vel = 40.0 if self.treadmill.vel > 40.0 else self.treadmill.vel

    def decrease_vel(self):
        self.treadmill.vel -= 5
        self.treadmill.vel = 0.0 if self.treadmill.vel < 0.0 else self.treadmill.vel

    def get(self):
        return self.treadmill

    def to_str(self):
        print(self.treadmill.status)
        print(self.treadmill.type)
        print(self.treadmill.dist)
        print(self.treadmill.vel)


tr = Treadmill()

tr.to_str()
