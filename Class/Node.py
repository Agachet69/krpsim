from typing import List
from Class.Process import Process
from Class.TerminalColor import TerminalColor


class Node:
    def __init__(self, process: Process, name_exist: str):
        self.process: Process = process
        self.children: List[Node] = []
        self.name_exist: str = name_exist

    def add_child(self, child):
        self.children.append(child)

    def display(self, prefix=""):
        print(f"{TerminalColor.red + prefix}/{TerminalColor.white + self.process.name}" if prefix else self.process.name)
        for child in self.children:
            child.display(f"{prefix}/{self.process.name}" if prefix else self.process.name)