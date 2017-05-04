import pickle

from pymech.fluid.Component import Component
from pymech.fluid.Point import Point
from pymech.units.SI import ureg


class Resevoir(Component):
    Connection = Point()
    Level = -1 * ureg['m'] # Level of resevoir use -1 for inifinite amount
    Volume = -1 * ureg['m**3'] # Total volume in resevoir use -1 for infinite amount
    Dimensions = {'x' : -1 * ureg['m'],
                  'y' : -1 * ureg['m'],
                  'z' : -1 * ureg['m']} # Dimensions for the resevoir, use -1 for infinite dimensions

    def __init__(self, ID=None, connection=None, dimensions=None, level=None, volume=None):
        Component.__init__(self, ID=None)
        if connection is not None:
            self.Connection = connection
        if dimensions is not None:
            self.Dimensions = dimensions
            if dimensions['x'] == -1 * ureg['m']:
                self.Level = -1 * ureg['m']
                self.Volume = -1 * ureg['m**3']
            else:
                if volume is not None:
                    self.Volume = volume
                    self.Level = volume / (dimensions['x'] * dimensions['y'])
                    if self.Level > dimensions['z']:
                        self.Volume = dimensions['x'] * dimensions['y'] * dimensions['z']
                        self.Level = dimensions['z']
                elif level is not None:
                   self.Level = level
                   if self.Level > dimensions['z']:
                       self.Level = dimensions['z']
                   self.Volume = dimensions['x'] * dimensions['y'] * self.Level
