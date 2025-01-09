import argparse
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
    return name, quantity


def parse_process_line(line: str):
    #    TODO
    pass


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
                    content_file.optimize.add_optimize(parse_optimize_line(line))
                else:
                    if line[line.index(":") + 1 :][0] == "(":
                        parse_process_line(line)
                        pass
                    else:
                        content_file.stock.add_stock(*parse_stock_line(line))
            if not line:
                raise ValueError(f"The file is empty.")
        print(content_file.stock)
        print(content_file.optimize)

    return content_file.stock


def main():
    args = parse_args()

    stocks = parse_file(args.path)


if __name__ == "__main__":
    main()
