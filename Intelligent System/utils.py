class Port(object):
    port = 2999

    @staticmethod
    def get_port():
        Port.port += 1
        print(Port.port)
        return Port.port
