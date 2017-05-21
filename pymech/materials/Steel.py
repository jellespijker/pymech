from .Material import Material, Category
from pymech.units.SI import *


class Steel(Material):
    E = 210.e3 * ureg.MPa
    G = 81.e3 * ureg.MPa
    A = 0.2
    R_mN = 130. * ureg.MPa
    R_eN = 130. * ureg.MPa
    sigma_tdWN = 140. * ureg.MPa
    sigma_bWN = 180. * ureg.MPa
    tau_tWN = 105. * ureg.MPa
    rel_cost = 1.0
    epsilon = 4.6e-5 * ureg['m']

    def __init__(self, name: str = 'Steel', id: str = '1.0000', T=293.15 * ureg['K'],
                 category: Category = Category.STEEL):
        Material.__init__(self)
        self.E = 210.e3 * ureg.MPa
        self.G = 81.e3 * ureg.MPa
        self.A = 0.2
        self.R_mN = 130. * ureg.MPa
        self.R_eN = 130. * ureg.MPa
        self.sigma_tdWN = 140. * ureg.MPa
        self.sigma_bWN = 180. * ureg.MPa
        self.tau_tWN = 105. * ureg.MPa
        self.rel_cost = 1.0
        self.epsilon = 4.6e-5 * ureg['m']

    def __repr__(self):
        mat = Material.__repr__(self) + repr(
            [self.E, self.G, self.A, self.R_mN, self.R_eN, self.sigma_tdWN, self.sigma_bWN, self.tau_tWN,
             self.rel_cost])
        return repr(mat)

    def load(self, filename):
        steel = serialize_load(filename, fmt='yaml')
        self.name = steel.name
        self.id = steel.id
        self._rho = steel._rho
        self._T = steel._T
        self._density_func = steel._density_func
        self.category = steel.category
        self.A = steel.A
        self.E = steel.E
        self.G = steel.G
        self.R_eN = steel.R_eN
        self.R_mN = steel.R_mN
        self.epsilon = steel.epsilon
        self.rel_cost = steel.rel_cost
        self.sigma_bWN = steel.sigma_bWN
        self.sigma_tdWN = steel.sigma_tdWN
        self.tau_tWN = steel.tau_tWN

    def Steel_to_builtin(u):
        return (Material.Material_to_builtin(u), u.A, u.E, u.G, u.R_eN, u.R_mN, u.epsilon, u.rel_cost, u.sigma_bWN,
                u.sigma_tdWN, u.tau_tWN)

    def Steel_from_builtin(c):
        steel = Steel()
        steel.name = c[0][0]
        steel.id = c[0][1]
        steel._rho = c[0][2]
        steel._T = c[0][3]
        steel._density_func = c[0][4]
        steel.category = c[0][5]
        steel.A = c[1]
        steel.E = c[2]
        steel.G = c[3]
        steel.R_eN = c[4]
        steel.R_mN = c[5]
        steel.epsilon = c[6]
        steel.rel_cost = c[7]
        steel.sigma_bWN = c[8]
        steel.sigma_tdWN = c[9]
        steel.tau_tWN = c[10]
        return steel
