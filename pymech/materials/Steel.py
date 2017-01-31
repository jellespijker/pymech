from .Material import Material, Category
import pickle
from pymech.units.SI import ureg, Q_

class Steel(Material):
    E = 210.e3 * ureg.MPa
    G = 81.e3 * ureg.MPa
    A = 0.2
    R_mN = 130. * ureg.MPa
    R_eN = 130.* ureg.MPa
    sigma_tdWN = 140.* ureg.MPa
    sigma_bWN = 180.* ureg.MPa
    tau_tWN = 105.* ureg.MPa
    rel_cost = 1.0

    def __init__(self, name: str = 'Steel', id: str = '1.0000', category: Category = Category.STEEL):
        Material.__init__(self)
        self.E = 210.e3 * ureg.MPa
        self.G = 81.e3 * ureg.MPa
        self.A = 0.2
        self.R_mN = 130.* ureg.MPa
        self.R_eN = 130.* ureg.MPa
        self.sigma_tdWN = 140.* ureg.MPa
        self.sigma_bWN = 180.* ureg.MPa
        self.tau_tWN = 105.* ureg.MPa
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