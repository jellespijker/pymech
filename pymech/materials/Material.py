from enum import Enum
import sys
from pymech.print import Latex

from pymech.units.SI import *


class LoadType(Enum):
    Torsion = 1
    Bend = 2
    Shear = 3

class Category(Enum):
    STEEL = 1
    PLASTIC = 2
    FLUID = 3


class Material:
    name: str = ''
    id: str
    category: Category
    _T = 293.15 * ureg['K']
    _rho = {20.: 7800. * ureg['kg/m**3']}
    _density_func = None

    def __init__(self, name: str = 'Steel', id: str = '1.0000', density=7800.0 * ureg['kg/m**3'], T=15. * ureg['degC'],
                 category: Category = Category.STEEL):
        self.name = name
        self.id = id
        self.category = category
        self.Tk = T

    def __repr__(self):
        return repr([self.name, self.id, self.category, self.rho, self.TdegC])

    def __str__(self):
        return 'Name: ' + str(self.name) + ' at ' + Latex.formulaprint(
            self.TdegC) + '<br/> Density: ' + Latex.formulaprint(self.rho)

    @property
    def rho(self):
        if self._density_func is None:
            if self.TdegC.magnitude in self._rho.keys():
                return self._rho[self.TdegC.magnitude]
            else:
                if len(self._rho) == 1 or list(self._rho.keys())[0] > self.TdegC.magnitude:
                    return list(self._rho.values())[0]
                prevKey = sys.float_info.min
                for key in self._rho.items():
                    if key[0] > self.TdegC.magnitude:
                        dT = (self.TdegC.magnitude - prevKey)
                        dRho = (self._rho[key[0]] - self._rho[prevKey])
                        return self._rho[prevKey] + dT * dRho / (key[0] - prevKey)
                    else:
                        prevKey = key[0]
                return self._rho[prevKey]
        else:
            return self._density_func(self.TdegC.magnitude)

    @rho.setter
    def rho(self, value):
        self._rho = value

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):
        if type(value).__module__ == 'pint.quantity':
            self._T = value.to('K')
        else:
            self._T = (value * ureg['degC']).to('K')

    @property
    def Tk(self):
        return self._T

    @Tk.setter
    def Tk(self, value):
        self._T = value.to('K')

    @property
    def TdegC(self):
        return self._T.to('degC')

    @TdegC.setter
    def TdegC(self, value):
        self._T = value.to('K')

    @property
    def gamma(self):
        return (self.rho * g).to('N/m**3')

    def load(self, filename):
        mat = serialize_load(filename)
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
