import numpy as np

from .Point import Point

class Geometry:
    axle = np.linspace(0, 1, 1)
    points = []
    size = 1
    solved = False

    def __init__(self, length: int = 1000):
        self.axle = np.linspace(start=0, stop=length, num=length)

    def addpoint(self, point: Point, sort: bool = True):
        if point.x <= self.axle.size:
            if any(p.x == point.x for p in self.points):
                for i in self.points:
                    if i.x == point.x:
                        i.F += point.F
                        i.M += point.M
                        i.T += point.T
            else:
                self.points.append(point)
                self.size += 1
                if sort:
                    self.sort()

    def addweight(self, startpoint: Point, endpoint: Point, weight: float = 1.0):
        if startpoint.x < endpoint.x:
            if endpoint.x <= self.axle.size:
                dx = endpoint.x - startpoint.x
                FpW = (weight * 9.81) / dx

                for i in range(startpoint.x, endpoint.x):
                    p = Point(i, f=FpW)
                    self.addpoint(p, sort=False)
                self.sort()

    def addtorqueload(self, startpoint: Point, endpoint: Point, Torque_per_mm: float = 1.0):
        if startpoint.x < endpoint.x:
            if endpoint.x <= self.axle.size:
                for i in range(startpoint.x, endpoint.x):
                    p = Point(i, t=Torque_per_mm)
                    self.addpoint(p, sort=False)
                self.sort()

    def sort(self):
        self.points.sort(key=lambda p: p.x)

    def getA(self):
        unknown = []
        for p in self.points:
            if not p.Known:
                unknown.append(p)
        A = np.zeros((2, len(unknown)))
        for i in range(len(unknown)):
            if unknown[i].F < 0:
                A[0, i] = -1
            else:
                A[0, i] = 1

        for i in range(len(unknown)):
            A[1, i] = unknown[i].x / 1000

        return A

    def getx(self):
        index = []
        for p in range(len(self.points)):
            if not self.points[p].Known:
                index.append(p)

        x: Point = []
        for i in index:
            x.append(self.points[i])

        return x

    def getb(self):
        known: Point = []
        for p in self.points:
            if p.Known:
                known.append(p)
        b = np.zeros((2, 1))
        for i in range(len(known)):
            b[0] -= known[i].F

        for i in range(len(known)):
            b[1] -= (known[i].x / 1000.) * known[i].F + known[i].M

        return b
