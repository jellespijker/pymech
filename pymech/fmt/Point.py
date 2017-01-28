import numpy as np


class Point:
    x = 0
    F = 0.0
    M = 0.0
    T = 0.0
    Known = True
    DOF = np.array([0, 0])

    def __init__(self, x: int = 0, f: float=0.0, m: float = 0.0, t: float = 0.0,
                 known: bool = True):
        self.x = x
        self.F = f
        self.M = m
        self.T = t
        self.Known = known

    def __contains__(self, item):
        return item.x == self.x

    def __repr__(self):
        return repr([self.x, self.F, self.M, self.T, self.DOF, self.Known])

    def __str__(self):
        return 'x: ' + str(self.x) + ", F: " + str(self.F) + ", M: " + str(self.M) + ", T: " + str(self.T)
