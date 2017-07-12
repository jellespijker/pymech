import numpy as np
from pymech.units.SI import ureg


class Vector():
    def __init__(self, vector=None, x=None, y=None, z=None, unit=ureg['dimensionless']):
        if vector is not None:
            self.vector = vector * unit
        else:
            self.vector = np.zeros((3, 1)) * unit
            if x is not None:
                self.vector[0] = x * unit
            if y is not None:
                self.vector[1] = y * unit
            if z is not None:
                self.vector[2] = z * unit

    @property
    def norm(self):
        return np.linalg.norm(self.vector)
