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
    stock_list: List[Stock],
    processes: List[Process],
    optimize_target: str,
    parent: Node,
    already_exist_node: dict,
    target_nodes,
):
    for process in processes:
        for result in process.results:
            if result.name == optimize_target:
                new_main = Node(process, process.name)
                target_nodes.append(new_main)
                already_exist_node[new_main.name_exist] = True


def find_target_childs(
    stock_list: List[Stock],
    processes: List[Process],
    target: str,
    parent: Node,
    already_exist_node: dict,
):
    process_child: Process = []
    for process in processes:
        for result in process.results:
            if result.name == target:
                parent_copy = copy.deepcopy(parent)
                name_exist = f'{parent_copy.name_exist} - {process.name}'
                if (already_exist_node.get(name_exist)):
                    new_child = Node(process, name_exist)

                    parent_copy.children.append(process)
                    for need in process.needs:
                        find_target_childs(stock_list, processes, need, process)
                
    # if all(
    #     [
    #         True
    #         if need.name in [stock.name for stock in content_file.stock_list]
    #         else False
    #         for need in node.process.needs
    #     ]
    # ):
    #     return
    # if node.process.type == "ressources":
    #     return
    # else:
    #     for need in node.process.needs:
    #         if need.name not in [stock.name for stock in content_file.stock_list]:
    #             processes = [
    #                 process
    #                 for process in content_file.process_list
    #                 if (
    #                     need.name
    #                     in [
    #                         result.name
    #                         for result in process.results
    #                         if result.quantity > 0
    #                     ]
    #                 )
    #             ]

    #             if buy_process := next(
    #                 (process for process in processes if process.type == "ressources"),
    #                 None,
    #             ):
    #                 new_node = Node(buy_process)
    #                 node.add_child(new_node)
    #                 return
    #                 # find_route(new_node, content_file)

    #             else:
    #                 for process in processes:
    #                     new_node = Node(process)
    #                     node.add_child(new_node)

    #                     find_route(new_node, content_file)


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
