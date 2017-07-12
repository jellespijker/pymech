from pymech.units.SI import *
import sys
from pymech.print import Latex
from .Material import Material, Category


class Fluidum(Material):
    def __init__(self, name=None, id=None, rho=None, T=None, category=None, P=None, R=None, mu=None, nu=None):
        Material.__init__(self, name=name, id=id, rho=rho, T=T, category=category)
        self._viscosity_func = None
        self._munuset = False
        if P is not None:
            self.P = P
        else:
            self.P = 0. * ureg['Pa']
        if R is not None:
            self.R = R
        else:
            self.R = 0. * ureg['J/(kg*K)']
        if mu is not None:
            self.mu = mu
        else:
            self._mu = None
        if nu is not None:
            self.nu = nu
        else:
            self._nu = None

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, value):
        self._P = value.to('Pa')

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        self._R = value.to('J/(kg*K)')

    @property
    def mu(self):
        # use function if set
        if self._viscosity_func is None:
            # If dynamic viscosity unknown use kinematic viscosity multiplied by density
            if self._mu is None and self._nu is not None:
                return (self.nu * self.rho).to('Pa*s')
            # If dynamic viscosity is single value return value
            if not isinstance(self._mu, dict):
                return self._mu
            # If dynamic viscosity is dict with key temperature, return (interpolated) value from current Temperature
            if self.T.to('degC').magnitude in self._mu.keys():
                return self._mu[self.T.to('degC').magnitude]
            else:
                if len(self._mu) == 1 or list(self._mu.keys())[0] > self.T.to('degC').magnitude:
                    return list(self._mu.values())[0]
                prev_key = sys.float_info.min
                for key in self._mu.items():
                    if key[0] > self.T.to('degC').magnitude:
                        dT = (self.T.to('degC').magnitude - prev_key)
                        dMu = (self._mu[key[0]] - self._mu[prev_key])
                        return self._mu[prev_key] + dT * dMu / (key[0] - prev_key)
                    else:
                        prev_key = key[0]
                return self._mu[prev_key]
        else:
            return self._viscosity_func(self.T.to('K'))

    @mu.setter
    def mu(self, value):
        if hasattr(value, '__call__'):
            self._viscosity_func = value
        elif not isinstance(value, dict):
            self._mu = value.to('Pa*s')
        else:
            self._mu = value
            for key, val in self._mu.items():
                self._mu[key] = val.to('Pa*s')

    @property
    def nu(self):
        # If kinematic viscosity unknown use dynamics viscosity divided by density
        if self._nu is None and self._mu is not None:
            return (self.mu / self.rho).to('m**2/s')
        # If kinematic viscosity is single value return value
        if not isinstance(self._nu, dict):
            return self._nu
        # If kinematic viscosity is dict with key temperature, return (interpolated) value from current Temperature
        if self.T.to('degC').magnitude in self._nu.keys():
            return self._nu[self.T.to('degC').magnitude]
        else:
            if len(self._nu) == 1 or list(self._nu.keys())[0] > self.T.to('degC').magnitude:
                return list(self._nu.values())[0]
            prev_key = sys.float_info.min
            for key in self._nu.items():
                if key[0] > self.T.to('degC').magnitude:
                    dT = (self.T.to('degC').magnitude - prev_key)
                    dNu = (self._nu[key[0]] - self._nu[prev_key])
                    return self._nu[prev_key] + dT * dNu / (key[0] - prev_key)
                else:
                    prev_key = key[0]
            return self._nu[prev_key]

    @nu.setter
    def nu(self, value):
        if not isinstance(value, dict):
            self._nu = value.to('m**2/s')
        else:
            self._nu = value
            for key, val in self._nu.items():
                self._nu[key] = val.to('m**2/s')

    def __repr__(self):
        return repr(Material.__repr__(self) + repr([self.P, self.R, self.mu, self.nu]))

    def __str__(self):
        return Material.__str__(self) + '<br/>Gamma: ' + Latex.formulaprint(
            self.gamma) + '<br/>Dynamic viscosity: ' + Latex.formulaprint(
            self.mu) + '<br/>Kinematic viscosity: ' + Latex.formulaprint(self.nu)

    def load(self, filename):
        fluidum = serialize_load(filename, fmt='yaml')
        Material.load(self, filename)
        self._P = fluidum._P
        self._R = fluidum._R
        self._mu = fluidum._mu
        self._nu = fluidum._nu

    def Fluidum_to_builtin(u):
        return (Material.Material_to_builtin(u), u._P, u._R, u._mu, u._nu)

    def Fluidum_from_builtin(c):
        fluidum = Material.Material_from_builtin(c[0])
        fluidum.__class__ = Fluidum
        fluidum._P = c[1]
        fluidum._R = c[2]
        fluidum._mu = c[3]
        fluidum._nu = c[4]
        return fluidum
