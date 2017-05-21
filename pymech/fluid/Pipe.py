import math

import pymech.materials as mat
from pymech.units.SI import *
from pymech.fluid.Component import Component
from pymech.fluid.Point import Point
from pymech.fluid.Core import flowrate, Regime, Reynolds, Darcy, flowregime, HagenPoiseuille, friction, fluidspeed, \
    hydrostatic_headloss, I_m
from pymech.fluid.Bingham import Reynolds_B


class Pipe(Component):
    L = 0. * ureg['m']  # Length of pipe
    _D_out = 0. * ureg['m']  # Diameter outer
    _wt = 0. * ureg['m']  # wall thickness of pipe
    material = mat.Steel()  # Material of pipe
    Standard = "ASME B36.10"  # Standard norm used
    From = Point()
    To = Point()
    fluid = mat.Fluid()

    def __init__(self, ID=None, L=None, D_out=None, wt=None, material=None, fluid=None):
        Component.__init__(self, ID)
        if L is not None and D_out is not None and wt is not None:
            self.L = L
            self.D_out = D_out
            self.wt = wt
        if material is not None:
            self.set_material(material=material)
        if fluid is not None:
            self.fluid = fluid
        else:
            self.fluid = mat.Fluid()

    def __repr__(self):
        return Component.__repr__(self) + repr([self.L, self.D_out, self.wt, self.hl])

    def Pipe_to_builtin(u):
        return (
            Component.Component_to_builtin(u), u.L, u._D_out, u._wt, u.material, u.Standard, u.From, u.To, u.fluid)

    def Pipe_from_builtin(c):
        pipe = Pipe()
        pipe.ID = c[0][0]
        pipe._P = c[0][1]
        pipe._A = c[0][2]
        pipe._Q = c[0][3]
        pipe._v = c[0][4]
        pipe.L = c[1]
        pipe._D_out = c[2]
        pipe._wt = c[3]
        pipe.material = c[4]
        pipe.Standard = c[5]
        pipe.From = c[6]
        pipe.To = c[7]
        pipe.fluid = c[8]
        return pipe

    def load(self, filename, ID=None, L=None, fluid=None, From=None, To=None):
        data = serialize_load(filename, fmt='yaml')
        if ID is None:
            self.ID = data.ID
        else:
            self.ID = ID
        self._P = data._P
        self._A = data._A
        self._Q = data._Q
        self._v = data._v
        if L is None:
            self.L = data.L
        else:
            self.L = L
        self._D_out = data._D_out
        self._wt = data._wt
        self.material = data.material
        self.Standard = data.Standard
        if fluid is None:
            self.fluid = data.fluid
        else:
            self.fluid = fluid
        if From is None and To is None:
            self.From = data.From
            self.To = data.To
        else:
            self.From = From
            self.To = To

    def set_route(self, From, To):
        self.From = From
        self.To = To

    def set_material(self, material=None):
        self.material = material

    @property
    def Re(self):
        if issubclass(type(self.fluid), mat.BinghamFluid):
            return Reynolds_B(fluid=self.fluid, pipe=self)
        return Reynolds(v=abs(self.v), D=self.D_in, fluid=self.fluid)

    def headloss(self, dP=False, pretty=False):
        hl = 0.

        # Calc energyloss due to friction
        f = friction(Re=self.Re, D=self.D_in, eps=self.material.epsilon)
        hl = Darcy(f=f, L=self.L, D=self.D_in, v=abs(self.v), fluid=self.fluid, dP=dP, pretty=pretty)

        # Calc energyloss due to height
        hl += hydrostatic_headloss(z_from=self.From.Height, z_to=self.To.Height, fluid=self.fluid, dP=dP, pretty=pretty)

        # set pressure at point 1
        if dP:
            self.P1 = self.P0 - hl
        else:
            self.P1 = self.P0 - (hl * self.fluid.rho * g)
        return hl

    @property
    def D_out(self):
        return self._D_out

    @D_out.setter
    def D_out(self, value):
        self._D_out = value.to('m')

    @property
    def r_out(self):
        return self.D_out / 2

    @r_out.setter
    def r_out(self, value):
        self.D_out = value * 2

    @property
    def wt(self):
        return self._wt

    @wt.setter
    def wt(self, value):
        self._wt = value.to('m')

    @property
    def r_in(self):
        return self.r_out - self.wt

    @r_in.setter
    def r_in(self, value):
        self.wt = self.r_out - value

    @property
    def D_in(self):
        return self.D_out - 2 * self.wt

    @D_in.setter
    def D_in(self, value):
        self.wt = (self.D_out - value) / 2

    @property
    def LD(self):
        return self.L / self.D_in

    @property
    def A(self):
        return (math.pi / 4) * self.D_in ** 2
