from typing import List
from Class.Item import Item
from Class.Stock import Stock
from Class.Process import Process


class ContentFile:


    def __init__(self):
        self.stock_list: List[Stock] = []
        self.process_list: List[Process] = []
        self.optimize_list = []
        

    def get_ressources_process(self):
        return [process for process in self.process_list if process.type == "ressources"]

    def add_stock(self, item: Item):
        self.stock_list.append(Stock(item.name, item.quantity))

    def add_optimize(self, item):
        for i in item:
            self.optimize_list.append(i)
    def add_process(self, name, needs, results, delay):
        self.process_list.append(Process(name, needs, results, delay))
        
    def is_ressource_in_stock(self, process: Process):
        for need in process.needs:
            if not self.is_item_in_stock(need):
                return False
                    
        return True

    def is_item_in_stock(self, item: Item):
        if stock := next((stock for stock in self.stock_list if stock.name == item.name), None):
            if stock.quantity >= item.quantity:
                return True
        return False

    def run_process(self, process: Process):
        
        if not self.is_ressource_in_stock(process):
            raise Exception(f"Cannot run the process: {process.name} due to stock quantity.")
        
        
        for need in process.needs:
            stock = next((stock for stock in self.stock_list if stock.name == need.name))
            stock.remove(need.quantity)
        for result in process.results:
            if stock := next((stock for stock in self.stock_list if stock.name == result.name), None):
                stock.add(result.quantity)
            else:
                self.stock_list.append(Stock(result.name, result.quantity))
        

    def display_stock(self):
        name_width = max(max(len(obj.name) for obj in self.stock_list), len("Name"))
        quantity_width = max(max(len(str(obj.quantity)) for obj in self.stock_list), len("Quantity"))
        
        print(f"{'-' * name_width}-+-{'-' * quantity_width}")
        print(f"{'Name':<{name_width}} | {'Quantity':>{quantity_width}}")
        print(f"{'-' * name_width}-+-{'-' * quantity_width}")
        
        for obj in self.stock_list:
            print(f"{obj.name:<{name_width}} | {obj.quantity:>{quantity_width}}")
        print(f"{'-' * name_width}-+-{'-' * quantity_width}")
        