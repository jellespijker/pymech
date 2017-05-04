import math
import pickle

import pymech.materials as mat
from pymech.units.SI import ureg
from pymech.fluid.Component import Component
from pymech.fluid.Point import Point
from pymech.fluid.Core import flowrate, Regime, Reynolds, Darcy, flowregime, HagenPoiseuille, friction, fluidspeed, \
    hydrostatic_headloss


class Pipe(Component):
    L = 0. * ureg['m']  # Length of pipe
    D_out = 0. * ureg['m']  # Diameter outer
    r_in = 0. * ureg['m']  # Radius inner
    r_out = 0. * ureg['m']  # Radius outer
    D_in = 0. * ureg['m']  # Diameter inner
    wt = 0. * ureg['m']  # wall thickness of pipe
    A = 0. * ureg['m**2']  # Cross section of fluid
    LD = 0.  # Length of pipe divide by diameter
    material = mat.Steel()  # Material of pipe
    Re = 0.  # Reynolds
    Pr = 0.  # Prandtl
    Nu = 0.  # Nusselt
    Standard = "ASME B36.10"  # Standard norm used
    From = Point()
    To = Point
    fluid = mat.Fluid()

    def __init__(self, ID=None, L=None, D_out=None, wt=None, material=None, fluid=None):
        Component.__init__(self, ID)
        if L is not None and D_out is not None and wt is not None:
            self.updatedimensions(L=L, D_out=D_out, wt=wt)
        if material is not None:
            self.set_material(material=material)
        if fluid is not None:
            self.fluid = fluid
        else:
            fluid = mat.Fluid()

    def __repr__(self):
        return Component.__repr__(self) + repr([self.L, self.D_out, self.wt, self.hl])

    def load(self, filename, ID=None, L=None, fluid=None ,From=None, To=None):
        data = pickle.load(open(filename, "rb"))
        if ID is None:
            self.ID = data.ID
        else:
            self.ID = ID
        if L is None:
            self.L = data.L
        else:
            self.L = L
        self.D_out = data.D_out
        self.r_in = data.r_in
        self.r_out = data.r_out
        self.D_in = data.D_in
        self.wt = data.wt
        self.A = data.A
        self.LD = self.L / self.D_in
        self.material = data.material
        self.Q = data.Q
        self.v = data.v
        self.Re = data.Re
        self.Pr = data.Pr
        self.Nu = data.Nu
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

    def updatedimensions(self, L=None, D_out=None, wt=None):
        if L is not None:
            self.L = L.to('m')
        if D_out is not None:
            self.D_out = D_out.to('m')
        if wt is not None:
            self.wt = wt.to('m')
        self.D_in = self.D_out - 2 * self.wt
        self.A = (math.pi / 4) * self.D_in ** 2
        self.LD = self.L / self.D_in
        self.r_out = self.D_out / 2
        self.r_in = self.D_in / 2

    def set_material(self, material=None):
        self.material = material

    def set_q(self, Q, pretty=False):
        self.Q = Q.to('m**3/s')
        self.v = fluidspeed(self.Q, self.A)

    def set_re(self, pretty=False):
        self.Re = Reynolds(v=abs(self.v), D=self.D_in, fluid=self.fluid, pretty=pretty)

    def save(self, filename):
        pickle.dump(self, open(filename, "wb"))

    def headloss(self, dP=False, pretty=False):
        hl = 0.

        # Calc energyloss due to friction
        self.set_re(pretty=pretty)
        f = friction(Re=self.Re, D=self.D_in, eps=self.material.epsilon)
        hl = Darcy(f=f, L=self.L, D=self.D_in, v=abs(self.v), fluid=self.fluid, dP=dP, pretty=pretty)

        # Calc energyloss due to height
        hl += hydrostatic_headloss(z_from=self.From.Height, z_to=self.To.Height, fluid=self.fluid, dP=dP, pretty=pretty)
        self.hl = hl
        return hl
