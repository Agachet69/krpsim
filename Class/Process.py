from typing import List

from Class.Item import Item


class Process:
    def __init__(self):
        self.process = {}

    def add_process(self, name: str, needs, results, delay: int):
        if name in self.process:
            print("process already exist.")
        else:
            needs = []
            results = []
            for item in needs:
                need = Item(item.need, item.quantity)
                needs.append(need)

            for result in results:
                needs.append({"result": result.result, "quantity": result.quantity})

            self.stocks[name] = {
                "needs": needs,
                "result": results,
                "delay": delay,
            }
