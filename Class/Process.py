from typing import List, Literal, Union

from Class.TerminalColor import TerminalColor
from Class.Item import Item


class Process:
    def __init__(self, name: str, needs: List[Item], results: List[Item], delay: int, type = "normal"):
        self.name: str = name
        self.needs: List[Item] = needs
        self.results: List[Item] = results
        self.delay: int = delay
        self.type: Union[Literal["normal"], Literal["ressources"]] = type ##### Le type ressource sont pour les processs qui n'ont seulement besoin de chose provenant du stock initial (comme l'argent)

    def create_item(self, item: Item) -> bool:
        if result := next((result for result in self.results if result.name == item.name), None):
            return True
        return False

    def display(self):
        print(TerminalColor.yellow + self.name, TerminalColor.red + "(" + " | ".join([need.name + " " + str(need.quantity) for need in self.needs]) + ")", TerminalColor.green + "(" + " | ".join([result.name + " " + str(result.quantity) for result in self.results]) + ") " + TerminalColor.blue + str(self.delay), end="")
        
        if self.type == "ressources":
            print(TerminalColor.magenta + " [RESSOURCE]", end="")
        
        print()