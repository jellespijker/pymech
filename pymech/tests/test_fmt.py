import numpy as np

import unittest
import pymech.fmt as fmt

class test_fmt_methods(unittest.TestCase):
    def test_solver(self):

        G = fmt.Geometry(1000)
        G.addpoint(fmt.Point(100, known=False))
        G.addpoint(fmt.Point(500, f=1000.))
        G.addweight(fmt.Point(600), fmt.Point(800), 50)
        G.addpoint(fmt.Point(950, known=False))

        S = fmt.Solver(G)
        S.solve()

        data = np.load("../resources/tests/test_solver.npz")
        np.testing.assert_array_equal(data['V'], S.V)
        np.testing.assert_array_equal(data['M'], S.M)
        np.testing.assert_array_equal(data['T'], S.T)
