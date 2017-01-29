import math as math
import numpy as np
from IPython.display import Latex
import matplotlib.pyplot as pl

from pymech.fmt.Solver import Solver
from pymech.units.SI import ureg
from .Properties import Properties


class Axle:
    properties: Properties
    V = np.zeros((1,))
    M = np.zeros((1,))
    T = np.zeros((1,))

    def __init__(self, properties: Properties):
        self.properties = properties
        self.solvegeometry()

    def solvegeometry(self):
        S = Solver(self.properties.geometry)
        x = self.properties.geometry.getx()
        for f in x:
            f.F = 0.0
        S.solve()
        self.V = S.V
        self.M = S.M
        self.T = S.T

    def plotfmt(self, figsize=(10,5)):
        pl.figure(figsize=figsize)
        pl.subplot(311)
        pl.plot(self.properties.geometry.axle, self.V)
        pl.grid(True)
        pl.title('Vertical shear')
        pl.ylabel('Force in [N]')
        pl.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        pl.subplot(312)
        pl.plot(self.properties.geometry.axle, self.M)
        pl.grid(True)
        pl.title('Bending moments')
        pl.ylabel('Moment in [Nm]')
        pl.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        pl.subplot(313)
        pl.plot(self.properties.geometry.axle, self.T)
        pl.grid(True)
        pl.title('Torque')
        pl.ylabel('Torque in [Nm]')
        pl.xlabel('Length in [mm]')
        pl.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        pl.tight_layout()
        pl.show()

    def d_prime(self, pretty=False):
        if not self.properties.geometry.solved:
            self.solvegeometry()
        M_b = np.max(self.M) * self.properties.appliancefactor.K_a * ureg.pascal
        t = M_b / self.properties.material.sigma_bWN
        d_prime = 3.4 * math.pow(t, 1 / 3) * ureg.meter

        if pretty:
            return [d_prime,
                    Latex(r"""$\begin{array}{c}
                     M_{b} = K_A \max(M_{nom}) \rightarrow """ + str(M_b.magnitude) + """ [Nm] = """ + str(np.max(self.M)) + """[Nm] \\times """ + str(self.properties.appliancefactor.K_a) + """ [-] \\\\
                     d^{\'} \\approx 3.4 \\sqrt[3]{\\frac{M_{b}}{\sigma_{bWN}}} \\rightarrow """ + str(d_prime.magnitude) + """ [m] \\approx 3.4 [m] \sqrt[3]{\\frac{""" + str(M_b.magnitude) + " [Nm]}{" + str(self.properties.material.sigma_bWN.magnitude) + """[Nm]}}
                    \end{array}$""")]
        else:
            return [d_prime]
