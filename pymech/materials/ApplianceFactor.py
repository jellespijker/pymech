from enum import Enum

class Bumps(Enum):
    NO_BUMPS = 1
    LIGHT_BUMPS = 2
    MEDIUM_BUMPS = 3
    HEAVY_BUMPS = 4

class ApplianceFactor:
    K_a: float = 1.0
    drivingmachine: Bumps = Bumps.NO_BUMPS
    machine: Bumps = Bumps.NO_BUMPS

    def __init__(self, drivingmachine: Bumps = Bumps.NO_BUMPS, machine: Bumps = Bumps.NO_BUMPS):
        self.drivingmachine = drivingmachine
        self.machine = machine
        self.getK_a()

    def getK_a(self):
        if self.drivingmachine == Bumps.NO_BUMPS:
            if self.machine == Bumps.NO_BUMPS:
                self.K_a = 1.0
            elif self.machine == Bumps.LIGHT_BUMPS:
                self.K_a = 1.1
            elif self.machine == Bumps.MEDIUM_BUMPS:
                self.K_a = 1.25
            else:
                self.K_a = 1.5
        elif self.drivingmachine == Bumps.LIGHT_BUMPS:
            if self.machine == Bumps.NO_BUMPS:
                self.K_a = 1.25
            elif self.machine == Bumps.LIGHT_BUMPS:
                self.K_a = 1.35
            elif self.machine == Bumps.MEDIUM_BUMPS:
                self.K_a = 1.5
            else:
                self.K_a = 1.75
        elif self.drivingmachine == Bumps.MEDIUM_BUMPS:
            if self.machine == Bumps.NO_BUMPS:
                self.K_a = 1.5
            elif self.machine == Bumps.LIGHT_BUMPS:
                self.K_a = 1.6
            elif self.machine == Bumps.MEDIUM_BUMPS:
                self.K_a = 1.75
            else:
                self.K_a = 2.0
        else:
            if self.machine == Bumps.NO_BUMPS:
                self.K_a = 1.75
            elif self.machine == Bumps.LIGHT_BUMPS:
                self.K_a = 1.85
            elif self.machine == Bumps.MEDIUM_BUMPS:
                self.K_a = 2.0
            else:
                self.K_a = 2.25
