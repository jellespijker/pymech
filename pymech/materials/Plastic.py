from .Material import Material, Category
from .Solid import Solid
from pymech.units.SI import *


class Plastic(Solid):
    def __init__(self, name=None, id=None, rho=None, T=None, E=None, rel_cost=None, epsilon=None):
        Solid.__init__(self, name=name, id=id, rho=rho, category=Category.PLASTIC, T=T, E=E, rel_cost=None,
                       epsilon=epsilon)

    def load(self, filename):
        plastic = serialize_load(filename, fmt='yaml')
        Solid.load(self, filename)

    def Plastic_to_builtin(u):
        return (Solid.Solid_to_builtin(u))

    def Plastic_from_builtin(c):
        plastic = Solid.Solid_from_builtin(c)
        plastic.__class__ = Plastic
        return plastic