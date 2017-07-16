from pymech.units.SI import ureg
from pymech.units.Physics import Vector
from pymech.materials.Solid import Solid
from .Core import Element, Node
import numpy as np


class Spring(Element):
    def __init__(self, nodes: (Node, Node) = None, k=None):
        Element.__init__(self, nodes=nodes)
        if k is not None:
            self.k = k
        else:
            self.k = 0. * ureg['N/m']

    @property
    def stiffness_matrix(self):
        r"""
        Get stiffness matrix for this element.

        The stiffness matrix for a spring element is defined by:

        .. math::

            [k]_e = \begin{bmatrix}
            k  & -k \\
            -k &  k \\
            \end{bmatrix}

        where *k* is the spring stiffness.

        Return a numpy array.
        """
        return np.array([[1., -1.],
                         [-1., 1.]]) * self._k

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value.to('N/m')


class Beam(Element):
    def __init__(self, nodes: (Node, Node) = None, material=None, shape=None, E=None, I=None):
        pass
