from .Material import Material, Category
import pickle
from pymech.units.SI import ureg, Q_

class Steel(Material):
    E = 210.e9 * ureg.pascal
    G = 81.e9 * ureg.pascal
    A = 0.2
    R_mN = 130.e6 * ureg.pascal
    R_eN = 130.e6 * ureg.pascal
    sigma_tdWN = 140.e6 * ureg.pascal
    sigma_bWN = 180.e6 * ureg.pascal
    tau_tWN = 105.e6 * ureg.pascal
    rel_cost = 1.0

    def __init__(self, name: str = 'Steel', id: str = '1.0000', category: Category = Category.STEEL):
        Material.__init__(self)
        self.E = 210.e9 * ureg.pascal
        self.G = 81.e9 * ureg.pascal
        self.A = 0.2
        self.R_mN = 130.e6 * ureg.pascal
        self.R_eN = 130.e6 * ureg.pascal
        self.sigma_tdWN = 140.e6 * ureg.pascal
        self.sigma_bWN = 180.e6 * ureg.pascal
        self.tau_tWN = 105.e6 * ureg.pascal
        self.rel_cost = 1.0

    def __repr__(self):
        mat = Material.__repr__(self) + repr([self.E, self.G, self.A, self.R_mN, self.R_eN, self.sigma_tdWN, self.sigma_bWN, self.tau_tWN, self.rel_cost])
        return repr(mat)

    def load(self, filename):
        data = pickle.load(open(filename, "rb"))
        self.name = data.name  * ureg.pascal
        self.id = data.id
        self.category = data.category
        self.density = data.density
        self.E = data.E
        self.G = data.G
        self.A = data.A
        self.R_mN = data.R_mN
        self.R_eN = data.R_eN
        self.sigma_tdWN = data.sigma_tdWN
        self.sigma_bWN = data.sigma_bWN
        self.tau_tWN = data.tau_tWN
        self.rel_cost = data.rel_cost

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))