from .Material import Material, Category
from pymech.units.SI import *


class Plastic(Material):
    epsilon = 4.6e-5 * ureg['m']

    def __init__(self, name: str = 'Steel', id: str = '1.0000', density=800.0 * ureg['kg/m**3'], T=15. * ureg['degC'],
                 category: Category = Category.PLASTIC):
        Material.__init__(self, name=name, id=id, density=density, category=category)
        self.T = T

    def load(self, filename):
        plastic = serialize_load(filename, fmt='yaml')
        self.name = plastic.name
        self.id = plastic.id
        self._rho = plastic._rho
        self._T = plastic._T
        self._density_func = plastic._density_func
        self.category = plastic.category
        self.epsilon = plastic.epsilon

    def Plastic_to_builtin(u):
        return (Material.Material_to_builtin(u), u.epsilon)

    def Plastic_from_builtin(c):
        plastic = Plastic()
        plastic.name = c[0][0]
        plastic.id = c[0][1]
        plastic._rho = c[0][2]
        plastic._T = c[0][3]
        plastic._density_func = c[0][4]
        plastic.category = c[0][5]
        plastic.epsilon = c[1]
        return plastic
