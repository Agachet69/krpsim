from typing import List

from Class.Item import Item


class Process:
    def __init__(self, name: str, needs: List[Item], results: List[Item], delay: int):
        self.name: str = name
        self.needs: List[Item] = needs
        self.results: List[Item] = results
        self.delay: int = delay