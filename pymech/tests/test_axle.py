import unittest

import pymech.fmt as fmt
from pymech.materials.Metal import Steel
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

        d_prime = axle.d_prime()
        d_prime_exp = 0.3957349532059932
        d = axle.d_prime(pretty=True)
        self.assertAlmostEqual(first=d_prime.magnitude, second=d_prime_exp, places=5)

    def test_d_a(self):

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

        d_a = axle.d_a(k=0.5)
        d_a_exp = 0.32092532294768505
        self.assertAlmostEqual(first=d_a.magnitude, second=d_a_exp, places=5)