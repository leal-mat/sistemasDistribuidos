class Expression:
    def __init__(self, op: str, n1: float, n2: float):
        self.op = op
        self.n1 = n1
        self.n2 = n2

    def calc(self):
        if self.op == "+":
            return self.sum()

        if self.op == "-":
            return self.subtract()

        if self.op == "/":
            return self.div()

        if self.op == "*":
            return self.mul()

    def sum(self):
        return self.n1 + self.n2

    def subtract(self):
        return self.n1 - self.n2

    def mul(self):
        return self.n1 * self.n2

    def div(self):
        if self.n2 == 0:
            return "NaN"
        return self.n1 / self.n2
