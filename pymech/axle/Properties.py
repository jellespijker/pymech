from pymech.fmt.Geometry import Geometry
from pymech.materials.Metal import Steel
from pymech.materials.ApplianceFactor import ApplianceFactor

class Properties:
    geometry: Geometry
    material: Steel
    appliancefactor: ApplianceFactor

    def __init__(self, geometry: Geometry = Geometry(1000), material: Steel = Steel(), appliancefactor: ApplianceFactor = ApplianceFactor()):
        self.material = material
        self.material = Steel
        self.appliancefactor = appliancefactor