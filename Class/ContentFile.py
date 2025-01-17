from typing import List
from Class.Item import Item
from Class.Stock import Stock
from Class.Process import Process


class ContentFile:


    def __init__(self):
        self.stock_list: List[Stock] = []
        self.process_list: List[Process] = []
        self.optimize_list = []



    def add_stock(self, item: Item):
        self.stock_list.append(Stock(item.name, item.quantity))

    def add_optimize(self, item):
        for i in item:
            self.optimize_list.append(i)
    def add_process(self, name, needs, results, delay):
        self.process_list.append(Process(name, needs, results, delay))
        
    def is_process_only_using_thing_in_stock(self, process: Process):
        
        if all([True if (need.name in [stock.name for stock in self.stock_list]) else False for need in process.needs]):
            return True
        
        return False
