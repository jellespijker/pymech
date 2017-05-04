import networkx as nx
import numpy as np
import math

from pymech.materials.Fluid import Fluid
from pymech.units.SI import ureg
from pymech.fluid.Pipe import Pipe
from pymech.fluid.Point import Point
from pymech.fluid.Reservoir import Resevoir
from pymech.fluid.Discharge import Discharge


class System:
    _components = []
    _self_loops: int = 0
    _points = []
    F: Fluid
    Network = nx.Graph()

    def __init__(self, fluid: Fluid = None):
        if fluid is not None:
            self.fluid = fluid

    def _register_component(self, comp):
        if comp.ID in self._components:
            comp.ID = self._components[-1] + 1
        self._components.append(int(comp.ID))

    def _register_point(self, point):
        if point.ID in self._points:
            point.ID = self._points[-1] + 1
        self._points.append(int(point.ID))

    def number_of_points(self):
        return len(self._points)

    def number_of_components(self):
        return len(self._components)

    def add_point(self, point):
        if type(point) == list:
            for p in point:
                self._register_point(p)
                self.Network.add_node(p)
        else:
            self._register_point(point)
            self.Network.add_node(point)

    def add_comp(self, comp):
        if type(comp) == list:
            for c in comp:
                self._register_component(c)
                if type(c) == Pipe:
                    self.Network.add_edge(c.From, c.To, value=c)
                elif type(c) == Resevoir:
                    self.Network.add_edge(c.Connection, c.Connection, value=c)
                    self._self_loops += 1
                elif type(c) == Discharge:
                    self.Network.add_edge(c.Connection, c.Connection, value=c)
                    self._self_loops += 1
        else:
            self._register_component(comp)
            if type(comp) == Pipe:
                self.Network.add_node(comp.From, comp.To, value=comp)
            elif type(comp) == Resevoir:
                self.Network.add_node(comp.Connection, comp.Connection, value=comp)
                self._self_loops += 1
            elif type(comp) == Discharge:
                self.Network.add_node(comp.Connection, comp.Connection, value=comp)
                self._self_loops += 1

    def connect(self, comp_a, comp_b):
        if self.Network.has_node(comp_a) and self.Network.has_node(comp_b):
            self.Network.add_edge(comp_a, comp_b)

    def is_serial_system(self):
        for c in nx.cycle_basis(self.Network):
            if len(c) > 1:
                return True
        return False

    def solve(self):
        err = 1e-6
        max_no_itt = 100
        g = self.Network
        flow_loops = self.findloops(g)  # find no of loops
        nuk = self.number_of_components() - self._self_loops - len(
            flow_loops)  # determine no of functions ( no of nodes -1 + no of loops)
        A = np.zeros((nuk + len(flow_loops), nuk + len(flow_loops)))  # make A matrix
        b = np.zeros((nuk + len(flow_loops), 1))  # make B matrix
        Q = np.zeros((max_no_itt, nuk + len(flow_loops), 1))  # make Q matrix

        # Initialize flow 0.1 [m**3/s]
        Q[0] = 0.1
        for e in g.edges_iter():
            c = g.get_edge_data(e[0], e[1])['value']
            if type(c) == Pipe:
                c.set_q(0.1 * ureg['m**3/s'])  # TODO optimize initial guess

        # START
        for i in range(1, max_no_itt):
            # Determine flow in each node taking in to account the direction From -> To of each pipe
            j = 0
            for n in g.nodes():
                # get edge to each neighbor and add to list ignore self-loops because those will be discharges
                for nn in g.neighbors(n):
                    # loop through each pipe, check if flow is in to or out of node
                    if n != nn:
                        p = g.get_edge_data(n, nn)['value']
                        if p.From == n:
                            A[j, p.ID] = -1.
                        else:
                            A[j, p.ID] = 1.
                        if p.Q.magnitude >= 0.:
                            A[j, p.ID] *= 1.
                        else:
                            A[j, p.ID] *= -1.
                    else:
                        b[j] = -1. * g.get_edge_data(n, nn)['value'].Q.to_base_units().magnitude
                j += 1

            # Remove the last node equation that doesn't have additional information such as a discharge
            A[nuk, :] = 0.
            b[nuk] = 0.
            j = nuk
            # for k in range(j, -1, -1):
            #     if b[k] == 0.:
            #         A = np.delete(A, k, 0)
            #         b = np.delete(b, k, 0)
            #         break

            # Determine the headloss for each pipe in each loop comparing the pipe direction with the loop direction, positve for same negative for counter
            for fl in flow_loops:
                for p_in_flow in range(len(fl)):
                    next_p_in_flow = p_in_flow + 1
                    if next_p_in_flow > len(fl) - 1:
                        next_p_in_flow = 0
                    bn = 1.
                    comp = g.get_edge_data(fl[p_in_flow], fl[next_p_in_flow])['value']
                    if comp.To != fl[next_p_in_flow]:
                        bn = -1.
                    bn *= comp.headloss().magnitude * comp.Q.magnitude
                    hl = bn * comp.Q.magnitude
                    A[j, comp.ID] = hl
                j += 1

            # Solve for new Qs
            Q[i] = np.dot(np.linalg.inv(A), b)
            print(Q[i])
            err_mat = np.abs(Q[i] - Q[i - 1]) - err
            # Update flow
            for e in g.edges_iter():
                c = g.get_edge_data(e[0], e[1])['value']
                if type(c) == Pipe:
                    c.set_q(Q[i,c.ID] * ureg['m**3/s'])
            if np.all(err_mat < np.zeros(Q[i].shape)):
                print(i)
                break

    def findloops(self, G):
        loops = []
        for c in nx.cycle_basis(G):
            if len(c) > 1:
                loops.append(c)
        return loops
