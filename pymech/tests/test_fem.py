import unittest

from pymech.units.SI import ureg
from pymech.materials.Metal import Steel
from pymech.fem import *
import numpy as np


class test_fem_methods(unittest.TestCase):
    def test_global_stiffness_assembly(self):
        nodes = [Node(Vector(x=i * 100, unit=ureg['mm'])) for i in range(4)]
        nodes[0].displacement = Vector(x=0., y=0, z=0., unit=ureg['mm'])
        nodes[1].displacement = Vector(x=0., y=0, z=0., unit=ureg['mm'])
        nodes[3].force = Vector(x=5000., y=0., z=0., unit=ureg['N'])
        elements = [Spring() for i in range(3)]
        elements[0].nodes = (nodes[0], nodes[2])
        elements[0].k = 1000. * ureg['N/m']
        elements[1].nodes = (nodes[2], nodes[3])
        elements[1].k = 2000. * ureg['N/m']
        elements[2].nodes = (nodes[3], nodes[1])
        elements[2].k = 3000. * ureg['N/m']
        mesh = SpringMesh(nodes=nodes, elements=elements)
        model = SpringModel(topology=mesh)
        model.solve()
        model.print()

        pass

    def test_global_stiffness_assembly(self):
        nodes = [Node(Vector(x=i * 100, unit=ureg['mm'])) for i in range(5)]
        nodes[0].displacement = Vector(x=0., y=0, z=0., unit=ureg['mm'])
        nodes[4].displacement = Vector(x=20., y=0, z=0., unit=ureg['mm'])
        elements = [Spring(nodes=(nodes[i], nodes[i + 1]), k=200 * ureg['N/m']) for i in range(4)]
        mesh = SpringMesh(nodes=nodes, elements=elements)
        model = SpringModel(topology=mesh)
        model.solve()
        model.print()

        pass
