import pickle

from pymech.fluid.Component import Component
from pymech.fluid.Point import Point
from pymech.units.SI import ureg

class Discharge(Component):
    Connection = Point()

    def __init__(self, Q=0. * ureg['m**3/s']):
        self.Q = Q.to_base_units()

    def set_q(self, Q):
        self.Q = Q.to_base_units()