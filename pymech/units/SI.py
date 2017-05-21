from pint import UnitRegistry, set_application_registry
from serialize import dump as serialize_dump, load as serialize_load, register_class

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
Q_ = ureg.Quantity
set_application_registry(ureg)


def to_tuple(self):
    return ureg.Quantity.to_tuple(self)


def from_tuple(self):
    return ureg.Quantity.from_tuple(self)


register_class(ureg.Quantity, ureg.Quantity.to_tuple, ureg.Quantity.from_tuple)
g = 9.80665 * ureg['m/s**2']
