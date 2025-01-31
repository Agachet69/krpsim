from Class.ContentFile import ContentFile
from Class.Node import Node
from Class.RouteStockRequirements import RouteStockRequirements
from typing import List

def read_childrens(node: Node):
    print(node.process.name)
    for child in node.children:
        read_childrens(child)

def run_simplexe(content_file: ContentFile, route_requirements: RouteStockRequirements):
    all_process = []
    all_optimize = []
    for optimize in content_file.optimize_list:
        # print(optimize)
        all_optimize.append(optimize)
    print()
    # for process in content_file.process_list:
        # if process
        # all_process.append(process)
        # print(process.results[0].name)
    print()
    # for node in node_list.requirements:
        # if len(node.road_map):
        #  print(node.road_map)
        # for need in node.needs:
    # route_requirements.route.display()
    # child = route_requirements.route.children
    read_childrens(route_requirements.route)
    # print(route_requirements.route.children)
        
        #     route_requirements = route_requirements.route.children

