import math
import pickle

from pymech.units.SI import ureg
from pymech.fluid.Component import Component


class Point(Component):
    Height = 0. * ureg['m']

    def __init__(self, ID=None, height=0. * ureg['m']):
        Component.__init__(self, ID)
        self.Height = height

    def __repr__(self):
        return repr([self.ID, self.Height])