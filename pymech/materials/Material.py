from enum import Enum
import pickle
import sys

from pymech.units.SI import ureg, Q_


class Category(Enum):
    STEEL = 1
    PLASTIC = 2
    FLUID = 3


class Material:
    name: str
    id: str
    category: Category
    temperature = 293.15 * ureg['K']
    density = 7800.0 * ureg['kg/m**3']
    _density = {20.: 7800. * ureg['kg/m**3']}
    _density_func = None

    def __init__(self, name: str = 'Steel', id: str = '1.0000', density=7800.0 * ureg['kg/m**3'], T=293.15 * ureg['K'],
                 category: Category = Category.STEEL):
        self.name = name
        self.id = id
        self.category = category
        self.temperature = T

    def __repr__(self):
        return repr([self.name, self.id, self.category, self.getdensity(), self.temperature.to('degC')])

    @property
    def density(self):
        if self._density_func is None:
            if self.temperature.to('degC').magnitude in self._density.keys():
                return self._density[self.temperature.to('degC').magnitude]
            else:
                if len(self._density) == 1 or list(self._density.keys())[0] > self.temperature.to('degC').magnitude:
                    return list(self._density.values())[0]
                prevKey = sys.float_info.min
                for key in self._density.items():
                    if key[0] > self.temperature.to('degC').magnitude:
                        dT = (self.temperature.to('degC').magnitude - prevKey)
                        dRho = (self._density[key[0]] - self._density[prevKey])
                        return self._density[prevKey] + dT * dRho / (key[0] - prevKey)
                    else:
                        prevKey = key[0]
                return self._density[prevKey]
        else:
            return self._density_func(self.temperature.to('degC').magnitude)

    @density.setter
    def density(self, value):
        self._density = value

    def settemperaturecelsius(self, T: float = 20.):
        self.temperature = Q_(T, ureg['degC']).to('K')

    def load(self, filename):
        data = pickle.load(open(filename, "rb"))
        self.name = data.name
        self.id = data.id
        self.category = data.catergory
        self._density = data.denisty_
        self.temperature = data.temperature
        self._density_func = data._density_func

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))
