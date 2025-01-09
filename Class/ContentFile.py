from Class.Stock import Stock
from Class.Optimize import Optimize
from Class.Process import Process


class ContentFile:
    def __init__(self):
        self.stock = Stock()
        self.process = Process()
        self.optimize = Optimize()
