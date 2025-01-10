from typing import List, Literal, Union

from Class.Item import Item


class Process:
    def __init__(self, name: str, needs: List[Item], results: List[Item], delay: int, type = "normal"):
        self.name: str = name
        self.needs: List[Item] = needs
        self.results: List[Item] = results
        self.delay: int = delay
        self.type: Union[Literal["normal"], Literal["ressources"]] = type ##### Le type ressource sont pour les processs qui n'ont seulement besoin de chose provenant du stock initial (comme l'argent)
        