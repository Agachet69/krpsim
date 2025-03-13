from typing import List
from Class.Item import Item
from Class.Node import Node
from Class.RouteStockRequirements import RouteStockRequirements
from Class.TerminalColor import TerminalColor
from Class.Stock import Stock
from Class.ContentFile import ContentFile
from Class.Process import Process
import random
import copy

def find_optmize_process(
    processes: List[Process],
    optimize_target: str,
    already_exist_node: dict,
    target_nodes: List[Node],
):
    for process in processes:
        for result in process.results:
            if result.name == optimize_target:
                new_main = Node(process, process.name, None)
                target_nodes.append(new_main)
                already_exist_node[new_main.name_exist] = True


def find_target_childs(
    stock_list: List[Stock],
    processes: List[Process],
    parent: Node,
    already_exist_node: dict,
    target_nodes: List[Node],
):
    
    stock = {}
    for stock_item in stock_list:
        stock[stock_item.name] = stock_item.quantity
    
    process_child: Process = []
    same_target_process = 0
    for target in parent.process.needs:

        if stock.get(target.name) and target.quantity <= stock.get(target.name):
            continue

        same_target_process = 0
        for process in processes:
            for result in process.results:

                if result.name == target.name:

                    if parent.process.name == process.name:
                        continue

                    name_exist = f"{parent.name_exist} - {process.name}"
                    if (already_exist_node.get(name_exist) is True):
                        continue
                    already_exist_node[name_exist] = True
                    # print(name_exist)

                    new_child = Node(process, name_exist, parent)

                    # print(parent.name_exist)
                    if same_target_process > 0:
                        parent_copy = copy.deepcopy(parent)
                        parent_copy.children.pop()
                        parent_copy.children.append(new_child)
                        target_nodes.append(parent_copy)

                    else:
                        parent.children.append(new_child)
                    same_target_process += 1
                    for need in process.needs:
                        find_target_childs(
                            stock_list,
                            processes,
                            new_child,
                            already_exist_node,
                            target_nodes,
                        )


def temporary_run(
    route: Node, requirements: RouteStockRequirements, stock_list: List[Stock]
):
    stock = {}
    need: List[Item] = []
    result: List[Item] = []
    time = 0

    for stock_item in stock_list:
        stock[stock_item.name] = stock_item.quantity

    print(TerminalColor.white)
    route.display()
    print(TerminalColor.green)
    for requirement in requirements.requirements:
        for need in requirement.needs:
            print(need.name)
            print(need.quantity)
        print()
        # route = route.children[0]
    # need.append(route.process)
    # for child in self.children:
    #     child.display(f"{prefix}/{self.process.name}" if prefix else self.process.name)


def genetic_algorithm(
    # stocks,
    processes,
    # optimization,
    population_size,
    # generations=20,
    # mutation_rate=0.1,
):
    """Algorithme génétique pour optimiser l'ordre des processus."""
    population = [
        random.sample([p["name"] for p in processes], len(processes))
        for _ in range(population_size)
    ]
    for individual in population:
        print(individual)
    print()


processes = [
    {"name": "my process1"},
    {"name": "my process2"},
    {"name": "my process3"},
    {"name": "my process4"},
    {"name": "my process5"},
    {"name": "my process6"},
    {"name": "my process7"},
    {"name": "my process8"},
    {"name": "my process9"},
    {"name": "my process10"},
    {"name": "my process11"},
    {"name": "my process12"},
    {"name": "my process13"},
    {"name": "my process14"},
    {"name": "my process15"},
    {"name": "my process16"},
    {"name": "my process17"},
]

# genetic_algorithm(processes, population_size=10)
