from .Core import Topology, ureg
import numpy as np


class SpringMesh(Topology):
    def __init__(self, nodes=None, elements=None):
        Topology.__init__(self, nodes=nodes, elements=elements, dof=1, stiffness_unit=ureg['N/m'])
        self._assembled_matrix['force'] = False
        self._assembled_matrix['displacement'] = False
        self._assembled_matrix['known'] = False
        self._assembled_matrix['unknown'] = False
        self._force = np.zeros((self.no_nodes, 3)) * ureg['N']
        self._displacement = np.zeros((self.no_nodes, 3)) * ureg['m']
        self._known = []
        self._unknown = []

    @property
    def force(self):
        if not self._assembled_matrix['force']:
            for n in self.nodes:
                self._force[self.nodes.index(n)] = n.force.vector
            self._assembled_matrix['force'] = True
        return self._force

    @force.setter
    def force(self, value):
        for n, v in zip(self.nodes, value):
            n.force.vector = v
        self._assembled_matrix['force'] = False

    @property
    def displacement(self):
        if not self._assembled_matrix['displacement']:
            for n in self.nodes:
                self._displacement[self.nodes.index(n)] = n.displacement.vector
            self._assembled_matrix['displacement'] = True
        return self._displacement

    @displacement.setter
    def displacement(self, value):
        for i, v in zip(self.unknown, value):
            self.nodes[i].displacement.vector = v
        self._assembled_matrix['displacement'] = False

    @property
    def known(self):
        if not self._assembled_matrix['known']:
            known = []
            for n in self.nodes:
                if not np.isnan(n.displacement.vector.m).any():
                    known.append(self.nodes.index(n))
            self._known = known
        return self._known

    @property
    def unknown(self):
        if not self._assembled_matrix['unknown']:
            known = self.known
            self._unknown = np.arange(0, self.no_nodes)
            self._unknown = np.delete(self._unknown, known)
        return self._unknown


class BeamMesh(Topology):
    def __init__(self, nodes=None, elements=None):
        Topology.__init__(self, nodes=nodes, elements=elements, dof=2)
