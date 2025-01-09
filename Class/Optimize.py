class Optimize:
    def __init__(self):
        self.optimize = []

    def add_optimize(self, names: list[str]):
        for name in names:
            if name in self.optimize:
                print("already optimized")
            else:
                self.optimize.append(name)

    def __repr__(self):
        return "\n".join(
            [f"{name}" for name in self.optimize]
        )