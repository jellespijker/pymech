from pint import UnitRegistry, set_application_registry
ureg = UnitRegistry()
Q_ = ureg.Quantity
set_application_registry(ureg)
g = 9.80665 * ureg['m/s**2']

