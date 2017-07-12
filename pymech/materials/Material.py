from enum import Enum
import sys
from pymech.print import Latex
from IPython.display import Latex as ltx
from pymech.units.SI import *


<<<<<<< HEAD
=======
class LoadType(Enum):
    Torsion = 1
    Bend = 2
    Shear = 3


>>>>>>> 5458352... Resturcturing of Materials module
class Category(Enum):
    STEEL = 1
    PLASTIC = 2
    FLUID = 3
    GAS = 4
    BINGHAM = 5


class Material:
    def __init__(self, name=None, id=None, rho=None, T=None, category=None):
        self._density_func = None
        if name is not None:
            self.name = name
        else:
            self.name = 'not specified'
        if id is not None:
            self.id = id
        else:
            self.id = 'not specified'
        if rho is not None:
            self.rho = rho
        else:
            self.rho = 0. * ureg['kg/m**3']
        if T is not None:
            self.T = T
        else:
            self.T = 15. * ureg['degC']
        if category is not None:
            self.category = category
        else:
            self.category = Category.STEEL

    def __repr__(self):
        return repr([self.name, self.id, self.category, self.rho, self.T.to('degC')])

    def __str__(self):
        return 'Name: ' + str(self.name) + ' at ' + Latex.formulaprint(
            self.T.to('degC')) + '<br/> Density: ' + Latex.formulaprint(
            self.rho) + + '<br/>Gamma: ' + Latex.formulaprint(
            self.gamma)

    @property
    def rho(self):
        """ Gets the density of the material at the current temperature"""
        if self._density_func is None:
            if not isinstance(self._rho, dict):
                return self._rho
            if self.T.to('degC').magnitude in self._rho.keys():
                return self._rho[self.T.to('degC').magnitude]
            else:
                if len(self._rho) == 1 or list(self._rho.keys())[0] > self.T.to('degC').magnitude:
                    return list(self._rho.values())[0]
                prevKey = sys.float_info.min
                for key in self._rho.items():
                    if key[0] > self.T.to('degC').magnitude:
                        dT = (self.T.to('degC').magnitude - prevKey)
                        dRho = (self._rho[key[0]] - self._rho[prevKey])
                        return self._rho[prevKey] + dT * dRho / (key[0] - prevKey)
                    else:
                        prevKey = key[0]
                return self._rho[prevKey]
        else:
            return self._density_func(self.T.to('degC').magnitude)

    @rho.setter
    def rho(self, value):
        """ Set the density, this can either be a single value, function with respect to the current temperature, or a lookup dictionary with keys in Temperature """
        if hasattr(value, '__call__'):
            self._density_func = value
        elif not isinstance(value, dict):
            self._rho = value.to('kg/m**3')
        else:
            self._rho = value
            for key, val in self._rho.items():
                self._rho[key] = val.to('kg/m**3')

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):
        self._T = value.to('K')

    @property
    def gamma(self):
        return (self.rho * g).to('N/m**3')

    def load(self, filename):
        mat = serialize_load(filename, fmt='yaml')
        self.name = mat.name
        self.id = mat.id
        self._rho = mat._rho
        self._T = mat._T
        self._density_func = mat._density_func
        self.category = mat.category

    def save(self, filename):
        serialize_dump(self, filename, fmt='yaml')

    def Material_to_builtin(u):
        return (u.name, u.id, u._rho, u.T, u._density_func, u.category)

    def Material_from_builtin(c):
        mat = Material()
        mat.name = c[0]
        mat.id = c[1]
        mat._rho = c[2]
        mat._T = c[3]
        mat._density_func = c[4]
        mat.category = c[5]
        return mat

    def print(self):
        return ltx(str(self))
