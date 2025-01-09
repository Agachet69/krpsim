from typing import List
from Class.Process import Process


class Node:
    def __init__(self, process: Process):
        self.process: Process = process
        self.children: List[Node] = []

    def add_child(self, child):
        self.children.append(child)

    def display(self, prefix=""):
        path = f"{prefix}/{self.process.name}" if prefix else self.process.name
        print(path)
        for child in self.children:
            child.display(path)