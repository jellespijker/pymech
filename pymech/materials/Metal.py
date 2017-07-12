from .Material import Material, Category, LoadType
from .Solid import Solid
from pymech.units.SI import *
import pymech.print.Latex as Latex


class Steel(Solid):
    def __init__(self, name=None, id=None, rho=None, T=None, G=None, A=None, R_mN=None, R_eN=None, sigma_tdWN=None,
                 sigma_bWN=None, tau_tWN=None, rel_cost=None, epsilon=None, E=None):
        Solid.__init__(self, name=name, id=id, rho=rho, T=T, category=Category.STEEL,
                       E=E, rel_cost=rel_cost, epsilon=epsilon)
        if G is not None:
            self.G = G
        else:
            self.G = 81. * ureg['N/mm**2']
        if A is not None:
            self.A = A
        else:
            self.A = 0.2
        if R_mN is not None:
            self.R_mN = R_mN
        else:
            self.R_mN = 130. * ureg['MPa']
        if R_eN is not None:
            self.R_eN = R_eN
        else:
            self.R_eN = 130. * ureg['MPa']
        if sigma_tdWN is not None:
            self.sigma_tdWN = sigma_tdWN
        else:
            self.sigma_tdWN = 140. * ureg['MPa']
        if sigma_bWN is not None:
            self.sigma_bWN = sigma_bWN
        else:
            self.sigma_bWN = 180. * ureg['MPa']
        if tau_tWN is not None:
            self.tau_tWN = tau_tWN
        else:
            self.tau_tWN = 105. * ureg['MPa']

    @property
    def G(self):
        return self._G

    @G.setter
    def G(self, value):
        self._G = value.to('N/mm**2')

    @property
    def R_mN(self):
        return self._R_mN

    @R_mN.setter
    def R_mN(self, value):
        self._R_mN = value.to('MPa')

    @property
    def R_eN(self):
        return self._R_eN

    @R_eN.setter
    def R_eN(self, value):
        self._R_eN = value

    @property
    def sigma_tdWN(self):
        return self._sigma_tdWN

    @sigma_tdWN.setter
    def sigma_tdWN(self, value):
        self._sigma_tdWN = value.to('MPa')

    @property
    def sigma_bWN(self):
        return self._sigma_bWN

    @sigma_bWN.setter
    def sigma_bWN(self, value):
        self._sigma_bWN = value.to('MPa')

    @property
    def tau_tWN(self):
        return self._tau_tWN

    @tau_tWN.setter
    def tau_tWN(self, value):
        self._tau_tWN = value.to('MPa')

    def __repr__(self):
        mat = Solid.__repr__(self) + repr(
            [self.G, self.A, self.R_mN, self.R_eN, self.sigma_tdWN, self.sigma_bWN, self.tau_tWN, ])
        return repr(mat)

    def __str__(self):
        return Solid.__str__(self) + '<br/>Shear modulus: ' + Latex.formulaprint(
            self.G) + '<br/>Ultimate tensile strength: ' + Latex.formulaprint(
            self.R_mN) + '<br/>Ultimate yield strength: ' + Latex.formulaprint(
            self.R_eN) + '<br/>Max allowable torsion stress: ' + Latex.formulaprint(
            self.sigma_tdWN) + '<br/>Max allowable bending stress: ' + Latex.formulaprint(
            self.sigma_bWN) + '<br/>Max allowable shear stress: ' + Latex.formulaprint(self.tau_tWN)

    def sigma_v(self, typeofload=LoadType.Bend, pretty=False):
        """ Returns the Von Mises"""
        if typeofload is LoadType.Bend:
            sigma = self.sigma_bWN
            sigma_str = r"\sigma_{bWN}"
        else:
            sigma = self.sigma_tdWN
            sigma_str = r"\sigma_{tdWN}"
        sigma_v = (sigma ** 2 + 3 * self.tau_tWN ** 2) ** (1 / 2)
        if pretty:
            pr = Latex.display(
                Latex.toStr(r"\sigma_{v} = \sqrt{" + sigma_str) + r"^2 + 3 \times \tau_{tWN}^2} = \sqrt{" + Latex.toStr(
                    sigma) + r"^2 + 3 \times " + Latex.toStr(self.tau_tWN) + r"^2} = " + Latex.toStr(sigma_v))
            return [sigma_v, pr]
        else:
            return sigma_v

    def load(self, filename):
        steel = serialize_load(filename, fmt='yaml')
        Solid.load(self, filename)
        self.A = steel.A
        self._G = steel._G
        self._R_eN = steel._R_eN
        self._R_mN = steel._R_mN
        self._sigma_bWN = steel._sigma_bWN
        self._sigma_tdWN = steel._sigma_tdWN
        self._tau_tWN = steel._tau_tWN

    def Steel_to_builtin(u):
        return (Solid.Solid_to_builtin(u), u.A, u._G, u._R_eN, u._R_mN, u._sigma_bWN, u._sigma_tdWN, u._tau_tWN)

    def Steel_from_builtin(c):
        steel = Solid.Solid_from_builtin(c[0])
        steel.__class__ = Steel
        steel.A = c[1]
        steel._G = c[2]
        steel._R_eN = c[3]
        steel._R_mN = c[4]
        steel._sigma_bWN = c[5]
        steel._sigma_tdWN = c[6]
        steel._tau_tWN = c[7]
        return steel
