from pymech.units.SI import register_class
from pymech.fluid import Pipe, Component

register_class(Pipe, Pipe.Pipe_to_builtin, Pipe.Pipe_from_builtin)
register_class(Component, Component.Component_to_builtin, Component.Component_from_builtin)

from pymech.materials import Plastic, Steel, BinghamFluid, Fluid, Material

register_class(Plastic, Plastic.Plastic_to_builtin, Plastic.Plastic_from_builtin)
register_class(Steel, Steel.Steel_to_builtin, Steel.Steel_from_builtin)
register_class(BinghamFluid, BinghamFluid.BinghamFluid_to_builtin, BinghamFluid.BinghamFluid_from_builtin)
register_class(Fluid, Fluid.Fluid_to_builtin, Fluid.Fluid_from_builtin)
register_class(Material, Material.Material_to_builtin, Material.Material_from_builtin)
