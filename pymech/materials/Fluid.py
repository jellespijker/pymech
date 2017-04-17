from pymech.units.SI import ureg, Q_
import pickle
import sys
from .Material import Material, Category


class Fluid(Material):
    gamma = 9.79 * ureg['kN/m**3']
    _gamma = {0.: 9.81 * ureg['kN/m**3'],
              5.: 9.81 * ureg['kN/m**3'],
              10.: 9.81 * ureg['kN/m**3'],
              15.: 9.81 * ureg['kN/m**3'],
              20.: 9.79 * ureg['kN/m**3'],
              25.: 9.78 * ureg['kN/m**3'],
              30.: 9.77 * ureg['kN/m**3'],
              35.: 9.75 * ureg['kN/m**3'],
              40.: 9.73 * ureg['kN/m**3'],
              45.: 9.71 * ureg['kN/m**3'],
              50.: 9.69 * ureg['kN/m**3'],
              55.: 9.67 * ureg['kN/m**3'],
              60.: 9.65 * ureg['kN/m**3'],
              65.: 9.62 * ureg['kN/m**3'],
              70.: 9.59 * ureg['kN/m**3'],
              75.: 9.56 * ureg['kN/m**3'],
              80.: 9.53 * ureg['kN/m**3'],
              85.: 9.50 * ureg['kN/m**3'],
              90.: 9.47 * ureg['kN/m**3'],
              95.: 9.44 * ureg['kN/m**3'],
              100.: 9.40 * ureg['kN/m**3']}

    mu = 0. * ureg['Pa*s']
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

    nu = 0. * ureg['m**2/s']
    _nu = {0.: 1.75e-6 * ureg['m**2/s'],
           5.: 1.52e-5 * ureg['m**2/s'],
           10.: 1.3e-6 * ureg['m**2/s'],
           15.: 1.15e-6 * ureg['m**2/s'],
           20.: 1.02e-6 * ureg['m**2/s'],
           25.: 8.94e-7 * ureg['m**2/s'],
           30.: 8.03e-7 * ureg['m**2/s'],
           35.: 7.22e-7 * ureg['m**2/s'],
           40.: 6.56e-7 * ureg['m**2/s'],
           45.: 6.e-7 * ureg['m**2/s'],
           50.: 5.48e-7 * ureg['m**2/s'],
           55.: 5.05e-7 * ureg['m**2/s'],
           60.: 4.67e-7 * ureg['m**2/s'],
           65.: 4.39e-7 * ureg['m**2/s'],
           70.: 4.11e-7 * ureg['m**2/s'],
           75.: 3.83e-7 * ureg['m**2/s'],
           80.: 3.6e-7 * ureg['m**2/s'],
           85.: 3.41e-7 * ureg['m**2/s'],
           90.: 3.22e-7 * ureg['m**2/s'],
           95.: 3.04e-7 * ureg['m**2/s'],
           100.: 2.94e-7 * ureg['m**2/s']}

    def __init__(self, name: str = 'Water', id: str = '0.0001', T=293.15 * ureg['K'],
                 category: Category = Category.FLUID):
        Material.__init__(self, name=name, id=id)
        self._density = {0.: 1000. * ureg['kg/m**3'],
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
        self.getgamma()
        self.getmu()
        self.getnu()

    def __repr__(self):
        mat = Material.__repr__(self) + repr([self.gamma, self.mu, self.nu])
        return repr(mat)

    def load(self, filename):
        data = pickle.load(open(filename, "rb"))
        self.name = data.name
        self.id = data.id
        self.category = data.category
        self.temperature = data.temperature
        self._density = data._density
        self.getdensity()
        self._gamma = data._gamma
        self.getgamma()
        self._mu = data._mu
        self.getmu()
        self._nu = data._nu
        self.getnu()

    def getgamma(self):
        try:
            self.gamma = self._gamma[self.temperature.to('degC').magnitude]
        except KeyError:
            if len(self._gamma) == 1 or list(self._gamma.keys())[0] > self.temperature.to('degC').magnitude:
                self.gamma = list(self._gamma.values())[0]
                return self.gamma
            prev_key = sys.float_info.min
            for key in self._gamma.items():
                if key[0] > self.temperature.to('degC').magnitude:
                    dT = (self.temperature.to('degC').magnitude - prev_key)
                    dGamma = (self._gamma[key[0]] - self._gamma[prev_key])
                    self.gamma = self._gamma[prev_key] + dT * dGamma / (key[0] - prev_key)
                    return self.gamma
                else:
                    prev_key = key[0]
            self.gamma = self._gamma[prev_key]
        return self.gamma

    def getmu(self):
        try:
            self.mu = self._mu[self.temperature.to('degC').magnitude]
        except KeyError:
            if len(self._mu) == 1 or list(self._mu.keys())[0] > self.temperature.to('degC').magnitude:
                self.mu = list(self._mu.values())[0]
                return self.mu
            prev_key = sys.float_info.min
            for key in self._mu.items():
                if key[0] > self.temperature.to('degC').magnitude:
                    dT = (self.temperature.to('degC').magnitude - prev_key)
                    dMu = (self._mu[key[0]] - self._mu[prev_key])
                    self.mu = self._mu[prev_key] + dT * dMu / (key[0] - prev_key)
                    return self.mu
                else:
                    prev_key = key[0]
            self.mu = self._mu[prev_key]
        return self.mu

    def getnu(self):
        try:
            self.nu = self._nu[self.temperature.to('degC').magnitude]
        except KeyError:
            if len(self._nu) == 1 or list(self._nu.keys())[0] > self.temperature.to('degC').magnitude:
                self.nu = list(self._nu.values())[0]
                return self.nu
            prev_key = sys.float_info.min
            for key in self._nu.items():
                if key[0] > self.temperature.to('degC').magnitude:
                    dT = (self.temperature.to('degC').magnitude - prev_key)
                    dNu = (self._nu[key[0]] - self._nu[prev_key])
                    self.nu = self._nu[prev_key] + dT * dNu / (key[0] - prev_key)
                    return self.nu
                else:
                    prev_key = key[0]
            self.nu = self._nu[prev_key]
        return self.nu

    def settemperaturecelsius(self, T: float = 20.):

        self.temperature = Q_(T, ureg['degC']).to('K')
        self.getdensity()
        self.getgamma()
        self.getmu()
        self.getnu()
