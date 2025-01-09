from typing import List
from Class.Process import Process


class Node:
    def __init__(self, process: Process):
        self.process: Process = process
        self.childrens: List[Node] = []

    def add_child(self, child):
        self.childrens.append(child)