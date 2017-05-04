import pickle

from pymech.units.SI import ureg


class Component:
    ID: int = 0  # ID number
    Q = 0. * ureg['m**3/s']  # Volumetric flow
    v = 0. * ureg['m/s']  # Speed of fluid
    P = [0. * ureg['Pa'], 0. * ureg['Pa']]  # Pressure at point A and B
    hl = 0. * ureg['Pa']  # Headloss in Pa or m

    def __init__(self, ID=None):
        if ID is not None:
            self.ID = int(ID)
        else:
            self.ID = int(0)

    def __repr__(self):
        return repr([self.ID, self.Q, self.v])

    def __hash__(self):
        return hash(self.ID)