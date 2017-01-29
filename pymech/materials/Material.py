from enum import Enum
import pickle
from pymech.units.SI import ureg, Q_

class Category(Enum):
    STEEL = 1
    PLASTIC = 2


class Material:
    name: str
    id: str
    category: Category
    density = 1000.0

    def __init__(self, name: str = 'Steel', id: str = '1.0000', density = 1000.0 * (ureg.kg / ureg.m**3), category: Category = Category.STEEL):
        self.name = name
        self.id = id
        self.category = category
        self.density = density

    def __repr__(self):
        return repr([self.name, self.id, self.category, self.density])

    def load(self, filename):
        data = pickle.load(open(filename, "rb"))
        self.name = data.name
        self.id = data.id
        self.category = data.catergory
        self.density = data.density

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))