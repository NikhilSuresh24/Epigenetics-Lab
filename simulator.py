import numpy as np


class BackSolve:
    def __init__(self):
        self.sim = Simulator()
        self.order = np.full((1, 10), -1)

    def phase_one(self):
        pass

    def phase_two(self):
        values = np.full((1, 10), -1)
        values[self.order[6]] = 1

        for i in range(10):
            if i not in self.order:
                self.sim.reset()
                nextv, nextx = step()
