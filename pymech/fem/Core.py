from pymech.units.SI import ureg
from pymech.units.Physics import Vector
from pymech.materials.Solid import Solid
import numpy as np
from enum import Enum


class FEMtype(Enum):
    Spring = 1
    Beam = 2


class Node(object):
    def __init__(self, point: Vector, force: Vector = None, displacement: Vector = None):
        self.point = point
        if force is not None:
            self.force = force
        else:
            self.force = Vector(unit=ureg['N'])
        if displacement is not None:
            self.displacement = displacement
        else:
            self.displacement = Vector(unit=ureg['m'])

    def __repr__(self):
        return repr(self.force)


class Element(object):
    def __init__(self, nodes: (Node, Node) = None):
        if nodes is not None:
            self.nodes = nodes
        else:
            self.nodes = (Node(point=Vector(unit=ureg['m'])), Node(point=Vector(unit=ureg['m'])))

    @property
    def stiffness_matrix(self):
        return np.eye(2)


class Topology(object):
    def __init__(self, nodes=None, elements=None, dof=1, stiffness_unit=ureg['dimensionless']):
        self._assembled_matrix = {'k': False}
        self._nodes = []
        self._elements = []
        if nodes is not None:
            self.add_nodes(nodes)
        if elements is not None:
            self.add_elements(elements)
        self.dof = dof
        self._stiffness_unit = stiffness_unit
        self._k = np.zeros((self.matrix_size, self.matrix_size)) * self._stiffness_unit

    @property
    def nodes(self):
        return self._nodes

    def add_nodes(self, nodes):
        if hasattr(nodes, '__iter__'):
            self._nodes.extend(nodes)
        else:
            self._nodes.append(nodes)
        for am in self._assembled_matrix:
            am = False

    @property
    def elements(self):
        return self._elements

    def add_elements(self, elements):
        if hasattr(elements, '__iter__'):
            self._elements.extend(elements)
        else:
            self._elements.append(elements)

    @property
    def no_nodes(self):
        return len(self._nodes)

    @property
    def matrix_size(self):
        return self.no_nodes * self.dof

    @property
    def k(self):
        if not self._assembled_matrix['k']:
            for e in self.elements:
                sm = e.stiffness_matrix
                for i in range(2):
                    for j in range(2):
                        self._k[self.nodes.index(e.nodes[i]), self.nodes.index(e.nodes[j])] += sm[i, j]
                        # TODO use DOF when assembling stiffness for 2 and 3 DOF elements.
            self._assembled_matrix['k'] = True
        return self._k


class Model(object):
    def __init__(self, topology: Topology = None, modeltype: FEMtype = None):
        if topology is not None:
            self.topology = topology
        else:
            self.topology = Topology()
        if modeltype is not None:
            self.modelType = modeltype
        else:
            self.modelType = FEMtype.Spring

    def build_global_matrix(self):

        pass

    def solve(self):
        pass

    def print(self):
        pass
