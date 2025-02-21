from typing import List, Literal, Union
from Class.RunningProcess import RunningProcess
from Class.Item import Item
from Class.Stock import Stock
from Class.Process import Process
import copy

from Class.TerminalColor import TerminalColor

class ContentFile:

    def __init__(self):
        self.mode: Union[Literal["normal"], Literal["test"]] = "normal"
        
        self.stock_list: List[Stock] = []
        self.process_list: List[Process] = []
        self.optimize_list: List[Union[Literal["time"], str]] = []
        
        self.running_process_list: List[RunningProcess] = []

        self.total_delay = 0

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
            if need.quantity != 0 and not self.is_item_in_stock(need):
                return False

        return True

    def is_item_in_stock(self, item: Item):
        if stock := next((stock for stock in self.stock_list if stock.name == item.name), None):
            if stock.quantity >= item.quantity:
                return True
        return False
    
    def update_process(self, time: int):
        to_pop = []
        print("Number runnning process:", len(self.running_process_list))
        for index, running in enumerate(self.running_process_list):
            if running.end_time == time:
                for result in running.process.results:
                    if stock := next((stock for stock in self.stock_list if stock.name == result.name), None):
                        stock.add(result.quantity)
                    else:
                        self.stock_list.append(Stock(result.name, result.quantity))
                running.process.display()
                to_pop.append(index)
        to_pop.reverse()
        for index in to_pop:
            self.running_process_list.pop(index)
                    

    def run_process(self, process: Process, process_from: Process, time: int):
        if self.mode == 'normal':
            print(TerminalColor.green + "Running process: ", end="")
            process.display()
        
        if not self.is_ressource_in_stock(process):
            raise Exception(f"Cannot run the process: {process.name} due to stock quantity.")

        for need in process.needs:
            if need.quantity != 0:
                stock = next((stock for stock in self.stock_list if stock.name == need.name))
                stock.remove(need.quantity)
            
        self.running_process_list.append(RunningProcess(process, process_from, time))
            
        # for result in process.results:
        #     if stock := next((stock for stock in self.stock_list if stock.name == result.name), None):
        #         stock.add(result.quantity)
        #     else:
        #         self.stock_list.append(Stock(result.name, result.quantity))

    def display_stock(self):
        name_width = max(max(len(obj.name) for obj in self.stock_list), len("Name"))
        quantity_width = max(max(len(str(obj.quantity)) for obj in self.stock_list), len("Quantity"))

        print(f"{'-' * name_width}-+-{'-' * quantity_width}")
        print(f"{'Name':<{name_width}} | {'Quantity':>{quantity_width}}")
        print(f"{'-' * name_width}-+-{'-' * quantity_width}")

        for obj in self.stock_list:
            print(f"{obj.name:<{name_width}} | {obj.quantity:>{quantity_width}}")
        print(f"{'-' * name_width}-+-{'-' * quantity_width}")

    def deep_copy(self):
        return copy.deepcopy(self)
