from .Material import Material
from pymech.units.SI import *
from pymech.print import Latex


class Solid(Material):
    def __init__(self, name=None, id=None, rho=None, category=None, T=None, E=None, rel_cost=None, epsilon=None):
        Material.__init__(self, name=name, id=id, rho=rho, category=category, T=T)
        if E is not None:
            self.E = E
        else:
            self.E = 0. * ureg['N/mm**2']
        if rel_cost is not None:
            self.rel_cost = rel_cost
        else:
            self.rel_cost = 0.
        if epsilon is not None:
            self.epsilon = epsilon
        else:
            self.epsilon = 4.6e-5 * ureg['m']

    def __repr__(self):
        mat = Material.__repr__(self) + repr([self.E, self.rel_cost, self.epsilon, self.rel_cost])
        return repr(mat)

    def __str__(self):
        return Material.__str__(self) + '<br/>Elastic modulus: ' + Latex.formulaprint(
            self.E)

    @property
    def E(self):
        return self._E

    @E.setter
    def E(self, value):
        self._E = value.to('N/mm**2')

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value):
        self._epsilon = value.to('m')

    def load(self, filename):
        solid = serialize_load(filename, fmt='yaml')
        Material.load(self, filename)
        self._E = solid._E
        self.rel_cost = solid.rel_cost
        self._epsilon = solid._epsilon

    def Solid_to_builtin(u):
        return (Material.Material_to_builtin(u), u._E, u.rel_cost, u._epsilon)

    def Solid_from_builtin(c):
        solid = Material.Material_from_builtin(c[0])
        solid.__class__ = Solid
        solid._E = c[1]
        solid.rel_cost = c[2]
        solid._epsilon = c[3]
        return solid
