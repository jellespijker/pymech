import math as math

import matplotlib.pyplot as pl
import numpy as np

import pymech.print.Latex as Latex
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

    def plotfmt(self, figsize=(10, 5)):
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

    def M_max(self, pretty=False):
        M_max = np.max(self.M) * ureg.N * ureg.m ** -2
        if pretty:
            pr = Latex.display(Latex.toStr(r"M_{max} = \max(M_{nom}) \rightarrow " + Latex.toStr(M_max)))
            return [M_max, pr]
        else:
            return M_max

    def M_b(self, pretty=False):
        M_b = self.M_max() * self.properties.appliancefactor.K_a
        if pretty:
            pr = Latex.display(Latex.toStr(r"M_{b} = K_A \max(M_{nom}) \times \rightarrow " + Latex.toStr(
                self.properties.appliancefactor.K_a) + r" \times " + Latex.toStr(self.M_max()) + r" = " + Latex.toStr(
                self.M_b())))
            return [M_b, pr]
        else:
            return M_b

    def d_prime(self, pretty=False):
        if not self.properties.geometry.solved:
            self.solvegeometry()
        d_prime = 3.4 * math.pow(self.M_b() / self.properties.material.sigma_bWN, 1 / 3) * ureg.meter

        if pretty:
            formArray = [[self.M_b(pretty=True)[1].data[1:-1]],
                         [r"d^{'} = \approx 3.4 " + Latex.sqrt(Latex.frac(r"M_{b}", r"\sigma_{bWN}"),
                                                               3) + r" \rightarrow 3.4 [m] " + Latex.sqrt(
                             Latex.frac(self.M_b(), self.properties.material.sigma_bWN),
                             3) + r" \approx " + Latex.toStr(d_prime)]]
            pr = Latex.display(Latex.array(formArray))
            return [d_prime, pr]
        else:
            return d_prime

    def d_a(self, k: float = 0.5, pretty=False):
        if not self.properties.geometry.solved:
            self.solvegeometry()
        d_a = 3.4 * math.pow(self.M_b() / ((1 - math.pow(k, 4)) * self.properties.material.sigma_bWN),
                             1 / 3) * ureg.meter

        if pretty:
            formArray = [[self.M_b(pretty=True)[1].data[1:-1]],
                         [r"d_{a} = \approx 3.4 " + Latex.sqrt(
                             Latex.frac(r"M_{b}", r"\left(1 - k^4 \right) \sigma_{bWN}"),
                             3) + r" \rightarrow 3.4 [m] " + Latex.sqrt(Latex.frac(self.M_b(),
                                                                                   r"\left(1 - " + str(k) + r"^{4} " + r"\right)" + Latex.toStr(
                                                                                       self.properties.material.sigma_bWN)),
                                                                        3) + r" \approx " + Latex.toStr(d_a)]]
            pr = Latex.display(Latex.array(formArray))
            return [d_a, pr]
        else:
            return d_a
