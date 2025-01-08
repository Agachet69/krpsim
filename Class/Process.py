from typing import List

from Class.Item import Item

class Process:
    def __init__(self, name: str, needs: List[Item], productes: List[Item]):
        self.name = name
        self.needs = needs
        self.productes = productes
