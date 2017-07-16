import numpy as np

from .Geometry import Geometry


class Solver:
    geometry: Geometry
    V = np.zeros((1,))
    M = np.zeros((1,))
    T = np.zeros((1,))

    def __init__(self, geometry: Geometry):
        self.geometry = geometry
        self.V = np.zeros((geometry.axle.size,))
        self.M = np.zeros((geometry.axle.size,))
        self.T = np.zeros((geometry.axle.size,))

    def solve(self):
        A = self.geometry.getA()
        x = self.geometry.getx()
        b = self.geometry.getb()

        S = np.linalg.solve(A, b)
        index = 0
        for p in x:
            p.force = S.item(index)
            index += 1

        for p in self.geometry.points:
            self.V[p.x] = -1 * p.force
            self.M[p.x] = p.M
            self.T[p.x] = p.T

        for v in range(1, self.V.size):
            self.V[v] += self.V[v - 1]

        self.M[0] += self.V[0]
        for m in range(1, self.M.size):
            self.M[m] = self.M[m] + self.M[m - 1] + self.V[m]

        for t in range(1, self.T.size):
            self.T[t] += self.T[t - 1]

        self.geometry.solved = True
