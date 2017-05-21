import pickle

from pymech.units.SI import *
from pymech.fluid.Core import fluidspeed, flowrate


class Component:
    ID: int = 0  # ID number
    _Q = 0. * ureg['m**3/s']  # Volumetric flow
    _v = 0. * ureg['m/s']  # Speed of fluid
    _A = 0. * ureg['m**2']  # Cross section of fluid plane
    _P = [0. * ureg['Pa'], 0. * ureg['Pa']]  # Pressure at point A and B

    def __init__(self, ID=None):
        if ID is not None:
            self.ID = int(ID)
        else:
            self.ID = int(0)

    def __repr__(self):
        return repr([self.ID, self.Q, self.v, self.A])

    def __hash__(self):
        return hash(self.ID)

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        A_old = self.A
        if A_old == 0. * ureg['m**2']:
            A_old = value.to('m**2')
        self._A = value.to('m**2')
        self.Q = (self.A / A_old) * self.Q  # update Q en v

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value.to('m/s')
        self._Q = flowrate(self.v, self.A)  # update Q

    @property
    def Q(self):
        return self._Q

    @Q.setter
    def Q(self, value):
        self._Q = value.to('m**3/s')
        self._v = fluidspeed(self.Q, self.A)  # update v

    @property
    def P(self):
        """ Get the pressure at both points np.array(2,1) [Pa]"""
        return self._P

    @P.setter
    def P(self, value):
        """ Set the pressure at both points np.array(2,1) [Pa]"""
        self._P = value.to('Pa')

    @property
    def P0(self):
        return self.P[0]

    @P0.setter
    def P0(self, value):
        self._P[0] = value.to('Pa')

    @property
    def P1(self):
        return self.P[1]

    @P1.setter
    def P1(self, value):
        self._P[1] = value.to('Pa')

    @property
    def dp(self):
        """ Pressure drop [Pa] """
        return self._P[0] - self._P[1]

    @property
    def hl(self):
        """ Headloss in the component [m]"""
        return self.dp / g

    def save(self, filename):
        serialize_dump(self, filename, fmt='yaml')

    def load(self, filename):
        comp = serialize_load(filename, fmt='yaml')
        self.ID = comp.ID
        self._P = comp._P
        self._A = comp._A
        self._Q = comp._Q
        self._v = comp._v

    def Component_to_builtin(u):
        return (u.ID, u._P, u._A, u._Q, u._v)

    def Component_from_builtin(c):
        comp = Component()
        comp.ID = c[0]
        comp._P = c[1]
        comp._A = c[2]
        comp._Q = c[3]
        comp._v = c[4]
        return comp
