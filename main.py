import argparse
from Class.Node import Node
from Class.Item import Item
from Class.Stock import Stock
from Class.ContentFile import ContentFile

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
    return Item(name, quantity)


def parse_process_line(line: str):
    process_name = line[:line.index(":")]

    rest = line[line.index(":") + 1:]


    needs_line = rest[1:rest.index(")")].split(";")
    needs = []

    for need in needs_line:
        name, quantity = need.split(":")
        needs.append(Item(name, quantity))

    rest = rest[rest.index(")")+2:]
    
    results_line = rest[1:rest.index(")")].split(";")
    results = []

    for result in results_line:
        name, quantity = result.split(":")
        results.append(Item(name, quantity))

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

    return content_file

def find_route(node: Node, content_file: ContentFile, i):
    if all([True if need.name in [stock.name for stock in content_file.stock_list] else False for need in node.process.needs]):
        return
    else:
        for need in node.process.needs:
            if need.name not in [stock.name for stock in content_file.stock_list]:
                processes = [process for process in content_file.process_list if (need.name in [result.name for result in process.results])]
                
                if buy_process := next((process for process in processes if content_file.is_process_only_using_thing_in_stock(process)), None):
                    new_node = Node(buy_process)
                    node.add_child(new_node)

                    find_route(new_node, content_file, i+1)
                else:
                    for process in processes:
                        new_node = Node(process)
                        node.add_child(new_node)

                        find_route(new_node, content_file, i+1)
                    
def main():
    args = parse_args()

    content_file = parse_file(args.path)


    main_nodes = []
    for optimize in content_file.optimize_list:
        if optimize != 'time':

            for process in content_file.process_list:
                if len([True for result in process.results if result.name == optimize]) > 0:
                    main_nodes.append(Node(process))
    
    

    print(main_nodes)
    
    # buy_beurre_process = next((process for process in content_file.process_list if process.name == "buy_beurre"))
    
    print(find_route(main_nodes[0], content_file, 0))
    
    main_nodes[0].display()
    
    
    # print(main_nodes[0].children)



if __name__ == "__main__":
    main()
