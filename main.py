import argparse
from typing import List
from Class.Node import Node
from Class.Item import Item
from Class.Stock import Stock
from Class.ContentFile import ContentFile
from Class.TerminalColor import TerminalColor


# LE FILE RECRE VA ETRE UN PEU RELOU A METRE EN PLACE JE EPNSE? MAIS PEU ETRE PAS NECESAIRE DE SE CASSER LA TETE DESSUS POUR LE MOMENT


def parse_args():
    parser = argparse.ArgumentParser(
        description="Give us a file and select a valid delay."
    )
    parser.add_argument(
        "path", type=str, help="Path to the configuration file with stocks and process."
    )
    parser.add_argument(
        "delay",
        type=float,
        help="Delay of the waiting time the program will not have to exceed.",
    )
    return parser.parse_args()


def parse_stock_line(line: str):
    name, quantity = line.strip().split(":")
    return Item(name, int(quantity))


def parse_process_line(line: str):
    process_name = line[:line.index(":")]

    rest = line[line.index(":") + 1:]


    needs_line = rest[1:rest.index(")")].split(";")
    needs = []
    results = []

    for need in needs_line:
        name, quantity = need.split(":")
        needs.append(Item(name, int(quantity)))

    if rest[rest.index(")")+2][0] != "(":
        pass
    else:
        rest = rest[rest.index(")")+2:]
        
        
        results_line = rest[1:rest.index(")")].split(";")

        for result in results_line:
            name, quantity = result.split(":")
            results.append(Item(name, int(quantity)))

    delay = int(rest[rest.index(")")+2:])

    return process_name, needs, results, delay



def parse_optimize_line(line: str):
    optimized_values = line.strip()[line.index(":") + 2 : -1]
    return optimized_values.split(";")


def parse_file(path):
    content_file = ContentFile()

    with open(path, "r") as file:
        for line in file:
            if not line.startswith("#"):
                if line == "\n":
                    continue

                name = line[: line.index(":")]

                if name == "optimize":
                    content_file.add_optimize(parse_optimize_line(line))
                else:
                    if line[line.index(":") + 1 :][0] == "(":
                        content_file.add_process(*parse_process_line(line))
                    else:
                        content_file.add_stock(parse_stock_line(line))
            if not line:
                raise ValueError(f"The file is empty.")
            
    # code pour ajouter le type des process
    
    for process in content_file.process_list:
        if all([True if (need.name in [stock.name for stock in content_file.stock_list]) else False for need in process.needs]):
            process.type = "ressources"
    

    return content_file

def find_route(node: Node, content_file: ContentFile):
    if all([True if need.name in [stock.name for stock in content_file.stock_list] else False for need in node.process.needs]):
        return
    else:
        for need in node.process.needs:
            if need.name not in [stock.name for stock in content_file.stock_list]:
                processes = [process for process in content_file.process_list if (need.name in [result.name for result in process.results])]
                
                if buy_process := next((process for process in processes if process.type == "ressources"), None):
                    # new_node = Node(buy_process)
                    # node.add_child(new_node)

                    # find_route(new_node, content_file, i+1)
                    pass
                else:
                    for process in processes:
                        new_node = Node(process)
                        node.add_child(new_node)

                        find_route(new_node, content_file)
                        

def run_route(node: Node, content_file: ContentFile):
    while not content_file.is_ressource_in_stock(node.process):
        ressources_process = content_file.get_ressources_process()
        
        for need in node.process.needs:
            if content_file.is_item_in_stock(need):
                continue
            elif len(ressource_process := [process for process in ressources_process if (need.name in [result.name for result in process.results])]) > 0:
                print('oui')
                for process in ressource_process:
                    if content_file.is_ressource_in_stock(process):
                        content_file.run_process(process)
                        return
            else:
                child = next((child for child in node.children if need.name in [result.name for result in child.process.results]))
                                
                run_route(child, content_file)
                
    content_file.run_process(node.process)

def find_best_route(routes: List[Node], content_file: ContentFile):
    
    score = []
    
    for optimize in content_file.optimize_list:
        if optimize != "time":
            for route in routes:
                test_content_file = content_file.deep_copy()
                
                try:
                    run_route(route, test_content_file)
                    stock = next((stock for stock in test_content_file.stock_list if stock.name == optimize))
                    score = stock.quantity
                except Exception:
                    score = 0
            
            # score.append({route.process.name: next((result.quantity for result in route.process.results if result.name == optimize), 0) for route in routes})
        # score.append()
        
        
        
    
    
    

    
                    
def main():
    args = parse_args()

    content_file = parse_file(args.path)


    main_nodes = []
    for optimize in content_file.optimize_list:
        if optimize != 'time':

            for process in content_file.process_list:
                if len([True for result in process.results if result.name == optimize]) > 0:
                    main_nodes.append(Node(process))
    

    # buy_beurre_process = next((process for process in content_file.process_list if process.name == "buy_beurre"))
    
    
    for i, _ in enumerate(main_nodes):
        find_route(main_nodes[i], content_file)
    
    
    for process in content_file.process_list:
        process.display()
    print(TerminalColor.green)
    
    for i, node in enumerate(main_nodes):
        print(TerminalColor.green + f"Route {i + 1} :", TerminalColor.white)
        node.display()
        print(TerminalColor.white)
    
    
    
    # main_nodes[0].display()
    
    
    # find_best_route(main_nodes, content_file)

    # while (1):    
    run_route(main_nodes[0], content_file)
    
    
    content_file.display_stock()
    
    
    
    
    
    
    
    # run_route(main_nodes[0], content_file)
    # content_file.display_stock()
    # print("Delay total from process:", content_file.total_delay)
    
    # find_best_route(main_nodes, content_file)
    
    
    
    # print(main_nodes[0].children)



if __name__ == "__main__":
    main()
