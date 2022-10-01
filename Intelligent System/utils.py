class Port(object):
    port = 3499

    @staticmethod
    def get_port():
        Port.port += 1
        print(Port.port)
        return Port.port
