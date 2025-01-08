import argparse



def parse_args():
    parser = argparse.ArgumentParser(description="Give us a file and select a valid delay.")
    parser.add_argument(
        "path", type=str, help="Path to the configuration file with stocks and process."
    )
    parser.add_argument(
        "delay", type=float, help="Delay of the waiting time the program will not have to exceed."
    )
    return parser.parse_args()

def is_stock():
    pass

def is_process():
    pass

def is_optimize():
    pass

def parse_file(path):
    parsed_values = []

    with open(path, "r") as file:
        for line in file:
            if line.startswith('#'):
                print(line)
            elif is_stock:
                print('is_stock')
            elif is_process:
                print('is_process')
            elif is_optimize:
                print('is_optimize')
            if not line:
                raise ValueError(
                    f"The file is empty."
                )
        
    return parsed_values

def main():
    args = parse_args()
    print(args)

    parsing = parse_file(args.path)


if __name__ == "__main__":
    main()
