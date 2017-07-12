from pymech.units.SI import *
from pymech.print import Latex
from .Material import Category
from .Fluidum import Fluidum


class Fluid(Fluidum):
    def __init__(self, name=None, id=None, rho=None, T=None, P=None, R=None, mu=None, nu=None):
        Fluidum.__init__(self, name=name, id=id, rho=rho, T=T, category=Category.FLUID, P=P, R=R, mu=mu, nu=nu)

    def load(self, filename):
        fluid = serialize_load(filename, fmt='yaml')
        Fluidum.load(self, filename)

    def Fluid_to_builtin(u):
        return (Fluidum.Fluidum_to_builtin(u))

    def Fluid_from_builtin(c):
        fluid = Fluidum.Fluidum_from_builtin(c)
        fluid.__class__ = Fluidum
        return fluid


class BinghamFluid(Fluid):
    def __init__(self, name=None, id=None, rho=None, T=None, P=None, R=None, mu=None, nu=None, tau_y=None, eta_b=None):
        Fluid.__init__(self, name=name, id=id, rho=rho, T=T, P=P, R=R, mu=mu, nu=nu)
        self.category = Category.BINGHAM
        if tau_y is not None:
            self.tau_y = tau_y
        else:
            self.tau_y = 0. * ureg['Pa']
        if eta_b is not None:
            self.eta_b = eta_b
        else:
            self.eta_b = 0. * ureg['Pa*s']

    def __repr__(self):
        return repr(Fluid.__repr__(self) + repr([self.tau_y, self.eta_b]))

    def __str__(self):
        return Fluid.__str__(self) + r'<br/>\tau_{y}: ' + Latex.formulaprint(
            self.tau_y) + r'<br/>\eta_b: ' + Latex.formulaprint(
            self.eta_b)

    @property
    def tau_y(self):
        return self._tau_y

    @tau_y.setter
    def tau_y(self, value):
        self._tau_y = value.to('Pa')

    @property
    def eta_b(self):
        return self._eta_b

    @eta_b.setter
    def eta_b(self, value):
        self._eta_b = value.to('Pa*s')

    def load(self, filename):
        bfluid = serialize_load(filename, fmt='yaml')
        Fluidum.load(self, filename)
        self._eta_b = bfluid._eta_b
        self._tau_y = bfluid._tau_y

    def BinghamFluid_to_builtin(u):
        return (Fluid.Fluid_to_builtin(u), u._eta_b, u._tau_y)

    def BinghamFluid_from_builtin(c):
        bfluid = Fluid.Fluid_from_builtin(c[0])
        bfluid._eta_b = c[1]
        bfluid._tau_y = c[2]
        return bfluid
