from Class.Process import Process


class RunningProcess():
    def __init__(self, process: Process, process_from: Process, start_time: int):
        self.process: Process = process
        self.process_from: Process = process_from
        self.start_time: int = start_time
        self.end_time: int = start_time + self.process.delay
