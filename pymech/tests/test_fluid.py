import networkx_viewer as nxv
import matplotlib.pyplot as plt
import numpy as np
import unittest
import math

from pymech.fluid import *
from pymech.materials import Fluid
from pymech.units.SI import ureg


class test_fluid_methods(unittest.TestCase):
    def test_fluid_density(self):
        f = Fluid()
        f.load('../resources/materials/Water.mat')
        self.assertEqual(f.density, 998 * ureg['kg/m**3'])
        f.settemperaturecelsius(22.5)
        self.assertEqual(f.density, 997.5 * ureg['kg/m**3'])
        f.settemperaturecelsius(120.)
        self.assertEqual(f.density, 958 * ureg['kg/m**3'])

    def test_fluid_gamma(self):
        f = Fluid()
        f.load('../resources/materials/Water.mat')
        self.assertEqual(f.getgamma(), 9.79 * ureg['kN/m**3'])
        f.settemperaturecelsius(27.5)
        self.assertEqual(round(f.getgamma(), 3), 9.775 * ureg['kN/m**3'])
        f.settemperaturecelsius(120.)
        self.assertEqual(f.getgamma(), 9.40 * ureg['kN/m**3'])

    def test_fluid_mu(self):
        f = Fluid()
        f.load('../resources/materials/Water.mat')
        self.assertEqual(f.getmu(), 1.02e-3 * ureg['Pa*s'])
        f.settemperaturecelsius(27.5)
        self.assertEqual(round(f.getmu(), 7), 8.455e-4 * ureg['Pa*s'])
        f.settemperaturecelsius(120.)
        self.assertEqual(f.getmu(), 2.82e-4 * ureg['Pa*s'])

    def test_fluid_nu(self):
        f = Fluid()
        f.load('../resources/materials/Water.mat')
        self.assertEqual(f.getnu(), 1.02e-6 * ureg['m**2/s'])
        f.settemperaturecelsius(27.5)
        self.assertEqual(round(f.getnu(), 10), 8.485e-7 * ureg['m**2/s'])
        f.settemperaturecelsius(120.)
        self.assertEqual(f.getnu(), 2.94e-7 * ureg['m**2/s'])

    def test_load_water(self):
        f = Fluid()
        f.load('../resources/materials/Water.mat')
        self.assertEqual(f.getdensity(), 998 * ureg['kg/m**3'])
        self.assertEqual(f.getmu(), 1.02e-3 * ureg['Pa*s'])
        self.assertEqual(f.getnu(), 1.02e-6 * ureg['m**2/s'])


class test_pipe_methods(unittest.TestCase):
    def test_headloss(self):
        f = Fluid()
        f.load('../resources/materials/Benzene.mat')
        points = [Point() for i in range(2)]
        points[1].Height = 21. * ureg['m']
        p = Pipe()
        p.load("../resources/piping/2.inch-Sc40.pip", L=240 * ureg['m'], fluid=f ,From=points[0], To=points[1])
        p.set_q(110. * ureg['l/min'])
        p.fluid.settemperaturecelsius(50)
        hl = np.zeros(2000) * ureg['m']
        for i in range(2000):
            p.set_q(i * ureg['l/min'])
            hl[i] = p.headloss()

        data = np.load('../resources/tests/test_headloss.npz')['arr_0']
        np.testing.assert_almost_equal(hl[1:2000].magnitude,data[1:2000],3)


class test_core_methods(unittest.TestCase):
    def test_Reynolds(self):
        Re = Reynolds(v=3.6 * ureg['m/s'], D=150 * ureg['mm'], mu=9.6e-1 * ureg['Pa*s'], rho=1258 * ureg['kg/m**3'],
                      pretty=True)
        self.assertAlmostEqual(Re[0], 707.625 * ureg['dimensionless'], places=0)
        self.assertEqual(Re[1].data,
                         r"$Re = \frac{v{f} \times D_i \times \rho_{f}}{\mu_{f}} \rightarrow \frac{3.60 \left[\frac{m}{s}\right] \times 1.50 \cdot 10^{2} \left[mm\right] \times 1.26 \cdot 10^{3} \left[\frac{kg}{m ^{3}}\right]}{9.60 \cdot 10^{-1} \left[Pa \cdot s\right]} = 7.08 \cdot 10^{2} \left[-\right]$")
        Re = Reynolds(v=3.6 * ureg['m/s'], D=150 * ureg['mm'], nu=7.63e-4 * ureg['m**2/s'])
        self.assertAlmostEqual(Re, 707.625 * ureg['dimensionless'], places=0)

        fluid = Fluid()
        fluid.load('../resources/materials/Water.mat')
        fluid.settemperaturecelsius(40)
        Re = Reynolds(v=3.6 * ureg['m/s'], D=150 * ureg['mm'], rho=fluid.density, mu=fluid.mu)
        self.assertAlmostEqual(Re, 822857. * ureg['dimensionless'], places=0)

    def test_flowrate(self):
        A = (math.pi / 4) * (150 * ureg['mm']) ** 2
        Q = flowrate(v=12. * ureg['km/hr'], A=A, pretty=True)
        self.assertAlmostEqual(round(Q[0], 6), 5.8905e-2 * ureg['m**3/s'])
        self.assertEqual(Q[1].data,
                         r"$Q_{f} = v_{f} \times A \rightarrow 1.20 \cdot 10^{1} \left[\frac{km}{h}\right] \times 1.77 \cdot 10^{4} \left[mm ^{2}\right] = 5.89 \cdot 10^{-2} \left[\frac{m ^{3}}{s}\right]$")

    def test_darcy(self):
        f = 4.3e-2
        L = 10. * ureg['m']
        D = 60.3 * ureg['mm']
        v = 3.6 * ureg['m/s']
        darcy = Darcy(f=f, L=L, D=D, v=v)
        self.assertEqual(round(darcy, 3), 4.712 * ureg['m'])
        rho = 992. * ureg['kg/m**3']
        darcy = Darcy(f=f, L=L, D=D, v=v, rho=rho, dP=True)
        self.assertEqual(round(darcy, 1), 45839.3 * ureg['Pa'])

    def test_flowregime(self):
        self.assertEqual(flowregime(200.7), Regime.LAMINAR)
        self.assertEqual(flowregime(3010.7), Regime.TRANSITIONAL)
        self.assertEqual(flowregime(10000.0), Regime.TURBULENT)

    def test_hagenpoiseuille(self):
        L = 10. * ureg['m']
        D = 60.3 * ureg['mm']
        v = 3.6 * ureg['m/s']
        mu = 1.02e-3 * ureg['Pa*s']
        hp = HagenPoiseuille(mu=mu, L=L, D=D, v=v, dP=True)
        self.assertEqual(round(hp,3), 323.160 * ureg['Pa'])
        rho = 998. * ureg['kg/m**3']
        hp = HagenPoiseuille(mu=mu, L=L, D=D, v=v, rho=rho)
        self.assertEqual(round(hp,3),0.033 * ureg['m'])

    def test_friction(self):
        Re = 1040.3
        D = 60.3 * ureg['mm']
        eps = 2.4e-4 * ureg['m']
        f = friction(Re=Re, D=D,eps=eps)
        self.assertEqual(round(f,4),0.0615 * ureg['dimensionless'])
        Re = 8999.2
        f = friction(Re=Re, D=D,eps=eps)
        self.assertEqual(round(f, 4), 0.0377 * ureg['dimensionless'])


class test_system_methods(unittest.TestCase):
    def test_network_singlepipe(self):
        F = Fluid()
        F.load("../resources/materials/Water.mat")
        S = System(F)
        points = [Point() for i in range(4)]
        S.add_point(points)
        pipes = [Pipe() for i in range(5)]
        pipes[0].load("../resources/piping/6.inch-Sc40.pip", L=300 * ureg['m'], From=points[0], To=points[1])
        pipes[1].load("../resources/piping/6.inch-Sc40.pip", L=200 * ureg['m'], From=points[1], To=points[2])
        pipes[2].load("../resources/piping/6.inch-Sc40.pip", L=200 * ureg['m'], From=points[2], To=points[3])
        pipes[3].load("../resources/piping/6.inch-Sc40.pip", L=300 * ureg['m'], From=points[3], To=points[0])
        pipes[4].load("../resources/piping/4.inch-Sc40.pip", L=320 * ureg['m'], From=points[0], To=points[2])
        discharges = [Discharge() for i in range(2)]
        discharges[0].Q = 10. * ureg['m**3/s']
        discharges[0].Connection = points[0]
        discharges[1].Q = -10 * ureg['m**3/s']
        discharges[1].Connection = points[2]

        S.add_comp(pipes)
        S.add_comp(discharges)

        # nnn = nxv.ViewerApp(S.Network)
        # nnn.mainloop()

        print(pipes)
        # S.solve()
        print(pipes)
