from .Core import Node, Vector, ureg


class SpringNode(Node):
    def __init__(self, point: Vector, force: Vector = None, displacement=None):
        Node.__init__(point=point)
        if force is not None:
            self.F = force
        else:
            self.F = Vector(unit=ureg['N'])
        if displacement is not None:
            self.D = displacement
        else:
            self.D = 0. * ureg['m']

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, value):
        self._F = value

    @property
    def D(self):
        return self._D

    @D.setter
    def D(self, value):
        self._D = value.to('m')
