import argparse
from Class.Node import Node
from Class.Item import Item
from Class.Stock import Stock
from Class.ContentFile import ContentFile


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
    name = line[:line.index(":")]

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

    return name, needs, results, delay



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

def find_route(node: Node, content_file: ContentFile):
    if all([True if need.name else False for need in node.process.needs]):
        pass

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



if __name__ == "__main__":
    main()
