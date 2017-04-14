from enum import Enum
import pickle
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

    def __init__(self, name: str = 'Steel', id: str = '1.0000', density=7800.0 * ureg['kg/m**3'], T=293.15 * ureg['K'],
                 category: Category = Category.STEEL):
        self.name = name
        self.id = id
        self.category = category
        self.temperature = T
        self.getdensity()

    def __repr__(self):
        return repr([self.name, self.id, self.category, self.getdensity(), self.temperature.to('degC')])

    def getdensity(self):
        try:
            self.density = self._density[self.temperature.to('degC').magnitude]
        except KeyError:
            prevKey = 0
            for key in self._density.items():
                if key[0] > self.temperature.to('degC').magnitude:
                    dT = (self.temperature.to('degC').magnitude - prevKey)
                    dRho = (self._density[key[0]] - self._density[prevKey])
                    self.density = self._density[prevKey] + dT * dRho / (key[0] - prevKey)
                    return self.density
                else:
                    prevKey = key[0]
            self.density = self._density[prevKey]
        return self.density

    def settemperaturecelsius(self, T: float = 20.):
        self.temperature = Q_(T, ureg['degC']).to('K')
        self.getdensity()

    def load(self, filename):
        data = pickle.load(open(filename, "rb"))
        self.name = data.name
        self.id = data.id
        self.category = data.catergory
        self._density = data.denisty_
        self.temperature = data.temperature
        self.getdensity()

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))
