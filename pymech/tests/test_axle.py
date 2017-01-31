import unittest
import matplotlib.pyplot as pl

import pymech.fmt as fmt
from pymech.materials.Steel import Steel
from pymech.materials.ApplianceFactor import ApplianceFactor, Bumps
from pymech.axle.Properties import Properties
from pymech.axle.Axle import Axle
from pymech.units.SI import ureg, Q_

class test_axle_methods(unittest.TestCase):
    def test_d_prime(self):

        prop = Properties()
        prop.geometry = fmt.Geometry(1000)
        prop.geometry.addpoint(fmt.Point(100, known=False))
        prop.geometry.addpoint(fmt.Point(500, f=500.))
        prop.geometry.addweight(fmt.Point(600), fmt.Point(800), 20.)
        prop.geometry.addpoint(fmt.Point(950, known=False))

        prop.material = Steel()
        prop.material.load(filename='../resources/materials/S235JR.mat')
        prop.appliancefactor = ApplianceFactor(drivingmachine=Bumps.NO_BUMPS, machine=Bumps.LIGHT_BUMPS)

        axle = Axle(properties=prop)
        axle.solvegeometry()

        d_prime = axle.d_prime(pretty=False)
        d_prime_exp = 0.3242340646818215
        self.assertAlmostEqual(first=d_prime[0].magnitude, second=d_prime_exp, places=5)
