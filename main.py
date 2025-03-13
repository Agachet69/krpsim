import argparse
import math
from typing import List
from Class.Node import Node
from Class.Item import Item
from Class.RouteStockRequirements import RouteStockRequirements
from Class.Stock import Stock
from Class.ContentFile import ContentFile
from Class.TerminalColor import TerminalColor
from simplex import run_simplexe
from utils import temporary_run, find_optmize_process, find_target_childs


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
    process_name = line[: line.index(":")]

    rest = line[line.index(":") + 1 :]

    needs_line = rest[1 : rest.index(")")].split(";")
    needs = []
    results = []

    for need in needs_line:
        name, quantity = need.split(":")
        needs.append(Item(name, int(quantity)))

    if rest[rest.index(")") + 2][0] != "(":
        pass
    else:
        rest = rest[rest.index(")") + 2 :]

        results_line = rest[1 : rest.index(")")].split(";")

        for result in results_line:
            name, quantity = result.split(":")
            results.append(Item(name, int(quantity)))

    delay = int(rest[rest.index(")") + 2 :])

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

                if ":" in line:
                    name = line[: line.index(":")]
                    if name == "optimize":
                        content_file.add_optimize(parse_optimize_line(line))
                    else:
                        if line[line.index(":") + 1 :][0] == "(":
                            content_file.add_process(*parse_process_line(line))
                        else:
                            content_file.add_stock(parse_stock_line(line))
                else:
                    raise ValueError(f"Wrong format file at line : {line}")
            if not line:
                raise ValueError(f"The file is empty.")

    # code pour ajouter le type des process

    for process in content_file.process_list:
        if all(
            [
                True
                if (need.name in [stock.name for stock in content_file.stock_list])
                or need.quantity == 0
                else False
                for need in process.needs
            ]
        ):
            process.type = "ressources"

    return content_file


def find_route(node: Node, content_file: ContentFile):
    if all(
        [
            True
            if need.name in [stock.name for stock in content_file.stock_list]
            else False
            for need in node.process.needs
        ]
    ):
        return
    if node.process.type == "ressources":
        return
    else:
        for need in node.process.needs:
            if need.name not in [stock.name for stock in content_file.stock_list]:
                processes = [
                    process
                    for process in content_file.process_list
                    if (
                        need.name
                        in [
                            result.name
                            for result in process.results
                            if result.quantity > 0
                        ]
                    )
                ]

                if buy_process := next(
                    (process for process in processes if process.type == "ressources"),
                    None,
                ):
                    new_node = Node(buy_process)
                    node.add_child(new_node)
                    return
                    # find_route(new_node, content_file)

                else:
                    for process in processes:
                        new_node = Node(process)
                        node.add_child(new_node)

                        find_route(new_node, content_file)


def run_route(node: Node, parent_node: Node, content_file: ContentFile, time: int):
    while not content_file.is_ressource_in_stock(node.process):
        ressources_process = content_file.get_ressources_process()

        for need in node.process.needs:
            if content_file.is_item_in_stock(need):
                continue
            elif (
                len(
                    ressource_process := [
                        process
                        for process in ressources_process
                        if (need.name in [result.name for result in process.results])
                    ]
                )
                > 0
            ):
                for i, process in enumerate(ressource_process):
                    if content_file.is_ressource_in_stock(process):
                        content_file.run_process(process, node.process, time)
                        break
                    elif i == len(ressource_process) - 1:
                        raise Exception(
                            f"There is no ressource process runnable for {need.name} due to stock capacity."
                        )
            else:
                child = next(
                    (
                        child
                        for child in node.children
                        if need.name
                        in [result.name for result in child.process.results]
                    )
                )

                run_route(child, node, content_file, time)

    if content_file.is_ressource_in_stock(node.process):
        content_file.run_process(
            node.process, parent_node.process if parent_node else None, time
        )


def find_best_route(routes: List[Node], content_file: ContentFile):
    routes_score = {}

    for route in routes:
        score = {}
        test_content_file = content_file.deep_copy()
        test_content_file.total_delay = 0
        test_content_file.mode = "test"
        try:
            run_route(route, None, test_content_file)
            for optimize in content_file.optimize_list:
                if optimize != "time":
                    stock = next(
                        (
                            result
                            for result in route.process.results
                            if result.name == optimize
                        )
                    )
                    score[optimize] = stock.quantity
                else:
                    score[optimize] = test_content_file.total_delay
        except Exception:
            score = "DNF"
        routes_score[route.process.name] = score

    routes_score = {
        index: routes_score[index]
        for index in routes_score
        if routes_score[index] != "DNF"
    }

    if not len(routes_score):
        raise Exception("There is no more route available.")
    if len(routes_score) == 1:
        return next(
            (
                route
                for route in routes
                if route.process.name == next(iter(routes_score))
            )
        )

    for key in iter(routes_score[next(iter(routes_score))]):
        max_value = max([score[key] for _, score in routes_score.items()])

        for _, score in routes_score.items():
            score[key] = round(score[key] * 100 / max_value)

    for key in routes_score:
        routes_score[key] = sum([score for _, score in routes_score[key].items()])

    better_route = max(routes_score, key=routes_score.get)

    return next((route for route in routes if route.process.name == better_route))


def new_run_route(
    node: Node,
    parent_node: Node,
    content_file: ContentFile,
    route_stock_requirements: RouteStockRequirements,
    multiplicator,
    time,
):
    # si process déja lancer alors return
    if _ := next(
        (
            running
            for running in content_file.running_process_list
            if running.process.name == node.process.name
        ),
        None,
    ):
        return

    # si peut lancer le process alors le fait
    if content_file.is_ressource_in_stock(node.process):
        for _ in range(multiplicator):
            if content_file.is_ressource_in_stock(node.process):
                content_file.run_process(
                    node.process, parent_node.process if parent_node else None, time
                )
            else:
                break
        return

    # ici que si pas assez de stock pour TOUT les needs
    for need in node.process.needs:
        # if check si il y a CE need
        if content_file.is_item_in_stock(need):
            continue
        # if check si il y a CE need en attente de process
        elif _ := next(
            (
                running
                for running in content_file.running_process_list
                if running.process_from.name == node.process.name
                and running.process.create_item(need)
            ),
            None,
        ):
            continue
        else:
            need_stock = next(
                (stock for stock in content_file.stock_list if stock.name == need.name),
                None,
            )
            need_stock = need_stock.quantity if need_stock else 0

            running_process = [
                running
                for running in content_file.running_process_list
                if running.process.create_item(need)
            ]

            need_to_create = (
                sum(
                    [
                        next(
                            result
                            for result in process.process.results
                            if result.name == need.name
                        ).quantity
                        for process in running_process
                    ]
                )
                if len(running_process)
                else 0
            )

            total_need_other_process_need = sum(
                [
                    next(
                        (
                            result
                            for result in item.process.results
                            if result.name == need.name
                        )
                    ).quantity
                    * item.multiplicator
                    for item in route_stock_requirements.road_map
                    if item.process.name != node.process
                    and item.process.create_item(need)
                ]
            )

            number_need_rest = (
                need_stock + need_to_create - total_need_other_process_need
            )

            number_need_need_for_that_process = need.quantity * multiplicator

            # si les autre process cree suffisament de need
            if number_need_need_for_that_process <= number_need_rest:
                break
            # if check si CE need est une ressource directement accessible via le stock initial
            elif ressource_process := next(
                (
                    process
                    for process in content_file.get_ressources_process()
                    if process.create_item(need)
                ),
                None,
            ):
                result = next(
                    (
                        result
                        for result in ressource_process.results
                        if result.name == need.name
                    )
                )
                for _ in range(
                    math.ceil(
                        (number_need_need_for_that_process - number_need_rest)
                        / result.quantity
                    )
                ):
                    content_file.run_process(ressource_process, node.process, time)
            # if check si CE need viens d'un child
            elif child := next(
                (child for child in node.children if child.process.create_item(need)),
                None,
            ):
                # child.process.display()
                result = next(
                    (
                        result
                        for result in child.process.results
                        if result.name == need.name
                    )
                )
                new_run_route(
                    child,
                    node,
                    content_file,
                    route_stock_requirements,
                    multiplicator * math.ceil(need.quantity / result.quantity),
                    time,
                )


def calculate_stock_route(
    node: Node,
    route_stock_requirements: RouteStockRequirements,
    multiplicator=1,
    depth=1,
):
    # node.display()
    route_stock_requirements.add_road_map_item(node.process, multiplicator)

    results = [
        result
        for result in node.process.results
        if result.name not in [need.name for need in node.process.needs]
    ]

    for result in results:
        route_stock_requirements.add_require_stock(
            Item(result.name, result.quantity * multiplicator),
            [
                Item(need.name, need.quantity * multiplicator)
                for need in node.process.needs
            ],
            depth,
        )

    needs = [
        need
        for need in node.process.needs
        if need.name not in [result.name for result in node.process.results]
        and need.quantity > 0
    ]

    for need in needs:
        if child := next(
            (child for child in node.children if child.process.create_item(need)), None
        ):
            result_child = next(
                (
                    result
                    for result in child.process.results
                    if result.name == need.name
                ),
                None,
            )
            # print(result_child.quantity)
            calculate_stock_route(
                child,
                route_stock_requirements,
                multiplicator * math.ceil(need.quantity / result_child.quantity),
                depth + 1,
            )


def main():
    args = parse_args()

    content_file = parse_file(args.path)

    target_nodes: List[Node] = []
    already_exist_node = {}

    for optimize_value in content_file.optimize_list:
        if optimize_value != "time":
            find_optmize_process(
                content_file.process_list,
                optimize_value,
                already_exist_node,
                target_nodes,
            )

        else:
            print("optimize time")
    # print(target_nodes[0])

    # print(already_exist_node.get(target_nodes[0].name_exist))

    for node in target_nodes:
        find_target_childs(
            content_file.stock_list,
            content_file.process_list,
            node,
            already_exist_node,
            target_nodes,
        )
    for node in target_nodes:
        while node.parent:
            node = node.parent
        print()
        print(node.display())

    return

    main_nodes = []

    for optimize in content_file.optimize_list:
        if optimize != "time":
            for process in content_file.process_list:
                if (
                    len(
                        [
                            True
                            for result in process.results
                            if result.name == optimize and result.quantity > 0
                        ]
                    )
                    > 0
                ):
                    main_nodes.append(Node(process))

    for node in main_nodes:
        node.display()

    # content_file.display_stock()
    # print()
    # print(
    #     TerminalColor.blue
    #     + "Optimize: "
    #     + ", ".join([optimize for optimize in content_file.optimize_list])
    # )

    for i, _ in enumerate(main_nodes):
        find_route(main_nodes[i], content_file)

    main_nodes = [RouteStockRequirements(route) for route in main_nodes]

    # for process in content_file.process_list:
    #     process.display()
    # print(TerminalColor.white)

    # for i, node in enumerate(main_nodes):
    #     print(TerminalColor.green + f"Route {i + 1} :", TerminalColor.white)
    #     node.route.display()
    #     print(TerminalColor.white)

    for main_node in main_nodes:
        calculate_stock_route(main_node.route, main_node)
    # print()

    # for requirement in main_nodes[0].requirements:
    #     print(
    #         requirement.result.name,
    #         requirement.result.quantity,
    #         "[",
    #         " ".join(
    #             [
    #                 "|".join([need.name, str(need.quantity)])
    #                 for need in requirement.needs
    #             ]
    #         ),
    #         "]",
    #         requirement.depth,
    #     )

    # print()
    # print("ROAD MAP")
    # print()

    # for road in main_nodes[0].road_map:
    #     print(TerminalColor.green + f"Multiplicator [{road.multiplicator}]: ", end="")
    #     road.process.display()

    actual_time = 0

    best_route = main_nodes[0]

    # run_simplexe(content_file=content_file, route_requirements=best_route)

    while True:
        print("Time:", actual_time)

        if running := next(
            (
                running
                for running in content_file.running_process_list
                if not running.process_from
            ),
            None,
        ):
            if running.end_time == actual_time:
                content_file.update_process(actual_time)
                content_file.display_stock()
                # print('finish')
                # run_simplexe(content_file=content_file, node_list=main_nodes)

                return

        content_file.update_process(actual_time)

        # best_route = find_best_route(main_nodes, content_file)
        # main_nodes[0].process.display()

        new_run_route(best_route.route, None, content_file, best_route, 1, actual_time)
        # temporary_run(best_route.route, best_route, content_file.stock_list)

        # content_file.display_stock()

        actual_time = min(
            [running.end_time for running in content_file.running_process_list]
            if (len(content_file.running_process_list) > 0)
            else ([actual_time + 1, actual_time + 1])
        )

        if actual_time > args.delay:
            break

    content_file.display_stock()
    # run_simplexe(content_file=content_file, route_requirements=best_route)
    # print(main_nodes[0].children)


if __name__ == "__main__":
    main()
