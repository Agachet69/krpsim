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

def parse_file(path):

    stocks = []


    with open(path, "r") as file:
        for line in file:
            if not line.startswith('#'):
                    name = line[:line.index(":")]
                    if name == "optimize":
                        pass
                    else:
                        if line[line.index(":") + 1 :][0] == '(':
                            pass
                        else:
                            print(line)



                    

            if not line:
                raise ValueError(
                    f"The file is empty."
                )
        
    return stocks

def main():
    args = parse_args()

    stocks = parse_file(args.path)


if __name__ == "__main__":
    main()
