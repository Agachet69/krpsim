from typing import List
from Class.Item import Item
from Class.Node import Node
from Class.Process import Process


class Object():
    def __init__(self, result: Item, needs: List[Item], depth: int):
        self.result: Item = result
        self.needs: List[Item] = needs
        self.depth: int = depth
        
class RoadMapItem():
    def __init__(self, process: Process, multiplicator):
        self.process: Process = process
        self.multiplicator = multiplicator

class RouteStockRequirements():
    
    def __init__(self, route: Node):
        self.route: Node = route
        self.requirements: List[Object] = []
        self.road_map: List[RoadMapItem] = []
    
    
    def add_require_stock(self, result: Item, needs: List[Item], depth: int):
        self.requirements.append(Object(result, needs, depth))
    
    def add_road_map_item(self, process: Process, multiplicator: int):
        self.road_map.append(RoadMapItem(process, multiplicator))