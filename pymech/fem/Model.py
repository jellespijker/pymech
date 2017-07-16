from .Core import Model, ureg
import numpy as np


class SpringModel(Model):
    def __init__(self, topology=None):
        Model.__init__(self, topology)
        self.k = np.zeros(topology.k.shape)
        self.force = np.zeros((topology.no_nodes, 3))
        self.displacement = np.zeros((topology.no_nodes, 3))

    def solve(self):
        self.k = np.delete(np.delete(self.topology.k.m, self.topology.known, 0), self.topology.known,
                           1) * self.topology.k.u
        # transposing known displacement to known force
        for e in self.topology.elements:
            if e.nodes[0].displacement.norm != 0. and not np.isnan(e.nodes[0].displacement.norm):
                e.nodes[1].force.vector = - e.k * e.nodes[0].displacement.vector
            if e.nodes[1].displacement.norm != 0. and not np.isnan(e.nodes[1].displacement.norm):
                e.nodes[0].force.vector = - e.k * e.nodes[1].displacement.vector

        self.force = np.delete(self.topology.force.m, self.topology.known, 0) * self.topology.force.u
        self.force[np.isnan(self.force)] = 0 * ureg['N']
        self.topology.displacement = np.linalg.solve(self.k.m, self.force.m) * ureg['m']
        self.topology.force = self.topology.k.dot(self.topology.displacement) * ureg['N']
        print(self.topology.displacement.m)
        print(self.topology.force.m)
        pass


class BeamModel(Model):
    def __init__(self, topology=None):
        Model.__init__(self, topology)
