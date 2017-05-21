from pymech.units.SI import *
import sys
from IPython.display import Latex as ltx
from pymech.print import Latex
from .Material import Material, Category


class Fluid(Material):
    _mu = {0.: 1.75e-3 * ureg['Pa*s'],
           5.: 1.52e-3 * ureg['Pa*s'],
           10.: 1.3e-3 * ureg['Pa*s'],
           15.: 1.15e-3 * ureg['Pa*s'],
           20.: 1.02e-3 * ureg['Pa*s'],
           25.: 8.91e-4 * ureg['Pa*s'],
           30.: 8.e-4 * ureg['Pa*s'],
           35.: 7.18e-4 * ureg['Pa*s'],
           40.: 6.51e-4 * ureg['Pa*s'],
           45.: 5.94e-4 * ureg['Pa*s'],
           50.: 5.41e-4 * ureg['Pa*s'],
           55.: 4.98e-4 * ureg['Pa*s'],
           60.: 4.6e-4 * ureg['Pa*s'],
           65.: 4.31e-4 * ureg['Pa*s'],
           70.: 4.02e-4 * ureg['Pa*s'],
           75.: 3.73e-4 * ureg['Pa*s'],
           80.: 3.5e-4 * ureg['Pa*s'],
           85.: 3.3e-4 * ureg['Pa*s'],
           90.: 3.11e-4 * ureg['Pa*s'],
           95.: 2.92e-4 * ureg['Pa*s'],
           100.: 2.82e-4 * ureg['Pa*s']}

    def __init__(self, name: str = 'Water', id: str = '0.0001', T=293.15 * ureg['K'],
                 category: Category = Category.FLUID):
        Material.__init__(self, name=name, id=id)
        self.T = T
        self.category = category
        self._rho = {0.: 1000. * ureg['kg/m**3'],
                     5.: 1000. * ureg['kg/m**3'],
                     10.: 1000. * ureg['kg/m**3'],
                     15.: 1000. * ureg['kg/m**3'],
                     20.: 998. * ureg['kg/m**3'],
                     25.: 997. * ureg['kg/m**3'],
                     30.: 996. * ureg['kg/m**3'],
                     35.: 994. * ureg['kg/m**3'],
                     40.: 992. * ureg['kg/m**3'],
                     45.: 990. * ureg['kg/m**3'],
                     50.: 988. * ureg['kg/m**3'],
                     55.: 986. * ureg['kg/m**3'],
                     60.: 984. * ureg['kg/m**3'],
                     65.: 981. * ureg['kg/m**3'],
                     70.: 978. * ureg['kg/m**3'],
                     75.: 975. * ureg['kg/m**3'],
                     80.: 971. * ureg['kg/m**3'],
                     85.: 968. * ureg['kg/m**3'],
                     90.: 965. * ureg['kg/m**3'],
                     95.: 962. * ureg['kg/m**3'],
                     100.: 958. * ureg['kg/m**3']}
        self.category = Category.FLUID

    def __repr__(self):
        mat = Material.__repr__(self) + repr([self.gamma, self.mu, self.nu])
        return repr(mat)

    def __str__(self):
        return Material.__str__(self) + '<br/>Gamma: ' + Latex.formulaprint(
            self.gamma) + '<br/>Dynamic viscosity: ' + Latex.formulaprint(
            self.mu) + '<br/>Kinematic viscosity: ' + Latex.formulaprint(self.nu)

    def load(self, filename):
        fluid = serialize_load(filename, fmt='yaml')
        self.name = fluid.name
        self.id = fluid.id
        self._rho = fluid._rho
        self._T = fluid._T
        self._density_func = fluid._density_func
        self.category = fluid.category
        self._mu = fluid._mu

    @property
    def mu(self):
        if self.TdegC.magnitude in self._mu.keys():
            return self._mu[self.TdegC.magnitude]
        else:
            if len(self._mu) == 1 or list(self._mu.keys())[0] > self.TdegC.magnitude:
                return list(self._mu.values())[0]
            prev_key = sys.float_info.min
            for key in self._mu.items():
                if key[0] > self.TdegC.magnitude:
                    dT = (self.TdegC.magnitude - prev_key)
                    dMu = (self._mu[key[0]] - self._mu[prev_key])
                    return self._mu[prev_key] + dT * dMu / (key[0] - prev_key)
                else:
                    prev_key = key[0]
            return self._mu[prev_key]

    @mu.setter
    def mu(self, value):
        self._mu = value

    @property
    def nu(self):
        return (self.mu / self.rho).to('m**2/s')

    def print(self):
        return ltx(str(self))

    def Fluid_to_builtin(u):
        return (Material.Material_to_builtin(u), u._mu)

    def Fluid_from_builtin(c):
        fluid = Fluid()
        fluid.name = c[0][0]
        fluid.id = c[0][1]
        fluid._rho = c[0][2]
        fluid._T = c[0][3]
        fluid._density_func = c[0][4]
        fluid.category = c[0][5]
        fluid._mu = c[1]
        return fluid


class BinghamFluid(Fluid):
    _tau_y = 0. * ureg['Pa']
    _eta_b = 0. * ureg['Pa*s']

    def __index__(self, name: str = 'Water', id: str = '0.0001', T=15.,
                  category: Category = Category.FLUID):
        Fluid.__init__(self, name=name, id=id, T=T, category=category)

    @property
    def tau_y(self):
        return self._tau_y

    @tau_y.setter
    def tau_y(self, value):
        self._tau_y = value.to('Pa')

    @property
    def etha_b(self):
        return self._eta_b

    @etha_b.setter
    def etha_b(self, value):
        self._eta_b = value.to('Pa*s')

    def load(self, filename):
        bfluid = serialize_load(filename, fmt='yaml')
        self.name = bfluid.name
        self.id = bfluid.id
        self._rho = bfluid._rho
        self._T = bfluid._T
        self._density_func = bfluid._density_func
        self.category = bfluid.category
        self._mu = bfluid._mu
        self._eta_b = bfluid._eta_b
        self._tau_y = bfluid._tau_y

    def BinghamFluid_to_builtin(u):
        return (Fluid.Fluid_to_builtin(u), u._eta_b, u._tau_y)

    def BinghamFluid_from_builtin(c):
        bfluid = BinghamFluid()
        bfluid.name = c[0][0][0]
        bfluid.id = c[0][0][1]
        bfluid._rho = c[0][0][2]
        bfluid._T = c[0][0][3]
        bfluid._density_func = c[0][0][4]
        bfluid.category = c[0][0][5]
        bfluid._mu = c[0][1]
        bfluid._eta_b = c[1]
        bfluid._tau_y = c[2]
        return bfluid
