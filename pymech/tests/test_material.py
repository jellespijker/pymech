import unittest

from pymech.materials.Metal import Steel
from pymech.materials.Fluid import Fluid, BinghamFluid
from pymech.units.SI import ureg


class test_material_methods(unittest.TestCase):
    def test_load_S235JR(self):
        S = Steel()
        S.load('../resources/materials/S235JR.mat')
        self.assertEquals(S.name, 'S235JR')
        self.assertEquals(S.id, '1.0037')
        self.assertEquals(S.rho, 7800. * ureg['kg/m**3'])
        self.assertEquals(S.T.to('degC'), 15. * ureg['degC'])
        self.assertEquals(S.E, 210.e3 * ureg['N/mm**2'])
        self.assertEquals(S.G, 81e3 * ureg['N/mm**2'])
        self.assertEquals(S.A, 26)
        self.assertEquals(S.R_mN, 360 * ureg['MPa'])
        self.assertEquals(S.R_eN, 235 * ureg['MPa'])
        self.assertEquals(S.sigma_tdWN, 140 * ureg['MPa'])
        self.assertEquals(S.sigma_bWN, 180 * ureg['MPa'])
        self.assertEquals(S.tau_tWN, 105 * ureg['MPa'])
        self.assertEquals(S.rel_cost, 1.0)
        self.assertEquals(S.epsilon, 4.6e-5 * ureg['m'])

    def test_load_Water(self):
        W = Fluid()
        W.load('../resources/materials/Water.mat')
        self.assertEquals(W.name, 'Water')
        self.assertEquals(W.id, '0.0001')
        self.assertEquals(W.rho, 1000. * ureg['kg/m**3'])
        self.assertEquals(W.T.to('degC'), 15. * ureg['degC'])
        self.assertEquals(W.mu, 1.15e-3 * ureg['Pa*s'])

    def test_load_GP(self):
        B = BinghamFluid()
        B.load('../resources/materials/12417-GP-5to1-Z1.mat')
        self.assertEquals(B.name, '12417-GP-5to1-Z1')
        self.assertEquals(B.id, 'GP.0000')
        self.assertEquals(B.rho, 2100. * ureg['kg/m**3'])
        self.assertEquals(B.mu, 1.62 * ureg['Pa*s'])
        self.assertEquals(B.T.to('degC'), 15. * ureg['degC'])
        self.assertEquals(B.tau_y, 100. * ureg['Pa'])
        self.assertEquals(B.eta_b, 1.62 * ureg['Pa*s'])
