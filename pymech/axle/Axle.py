import numpy as np
import math as math

from .Properties import Properties
from pymech.fmt.Solver import Solver
from pymech.units.SI import ureg, Q_

class Axle:
    properties: Properties
    V = np.zeros((1,))
    M = np.zeros((1,))
    T = np.zeros((1,))

    def __init__(self, properties: Properties):
        self.properties = properties
        self.solvegeometry()
        self.ureg = ureg

    def solvegeometry(self):
        S = Solver(self.properties.geometry)
        S.solve()
        self.V = S.V
        self.M = S.M
        self.T = S.T

    def d_prime(self):
        if not self.properties.geometry.solved:
            self.solvegeometry()
        M_b = np.max(self.M) * self.properties.appliancefactor.K_a * ureg.pascal
        t = M_b / self.properties.material.sigma_bWN
        d_prime = 3.4 * math.pow(t, 1/3) * ureg.meter
        return d_prime

