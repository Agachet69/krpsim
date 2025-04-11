from Class.Process import Process
from Class.Item import Item
from Class.ContentFile import ContentFile
from typing import List, Literal, Union

# def get_process_need(process: Process):
#     for need in process.needs:


def get_process_by_need(need: Item, process_list: List[Process]):
    process_interests: List[Process] = []

    for process in process_list:
        for result in  process.results:
            if result.name == need.name and result.quantity > 0:
                print(
                    f"{process.name} -> {result.name}: {result.quantity / need.quantity}"
                )
                process_interests.append(process)
    return process_interests


def get_optimize_process_by_need(optimize: str, process_list: List[Process]):
    process_interests = []

    for process in process_list:
        for result in process.results:
            if result.name == optimize and result.quantity > 0:
                print(f"{process.name} -> {result.name}: {result.quantity}")
                process_interests.append(process)
    return process_interests


def get_process_auto_generate_stock(process: Process):
    # for need in process.needs:
        # if need in process.results:
        #     print(f"{process.name} auto ")
        #     return True
    noms_resultats = {res.name for res in process.results}
    return all(need.name in noms_resultats for need in process.needs)

# liste de processus qui optimisent
# P1 -> P2 -> P3
# P1 -> P2 -> P1 -> P3
# P1 -> P2 -> P1 -> P1 -> P3