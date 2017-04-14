from pymech.units.SI import ureg
from pymech.materials.Fluid import Fluid
import pymech.print.Latex as Latex


def Reynolds(v, D, rho=None, mu=None, nu=None, fluid=None, pretty=False):
    if mu is not None and rho is not None:
        Re = (v * D * rho) / mu
        Re = Re.to_base_units()
        if pretty:
            pr = Latex.display(
                Latex.toStr(r"Re = \frac{v{f} \times D_i \times \rho_{f}}{\mu_{f}} \rightarrow \frac{" + Latex.toStr(
                    v) + r" \times " + Latex.toStr(D) + r" \times " + Latex.toStr(rho) + r"}{" + Latex.toStr(
                    mu) + r"} = " + Latex.toStr(Re)))
            return [Re, pr]
        else:
            return Re
    elif nu is not None:
        Re = (v * D) / nu
        Re = Re.to_base_units()
        if pretty:
            pr = Latex.display(
                Latex.toStr(r"Re = \frac{v{f} \times D_{i}}{\nu_{f}} \rightarrow \frac{" + Latex.toStr(
                    v) + r" \times " + Latex.toStr(D) + r" \times " + Latex.toStr(rho) + r"}{" + Latex.toStr(
                    mu) + r"} = " + Latex.toStr(Re)))
            return [Re, pr]
        else:
            return Re
    elif fluid is not None:
        Re = (v * D.to('m') * fluid.density) / fluid.mu
        Re = Re.to_base_units()
        if pretty:
            pr = Latex.display(Latex.toStr(
                r"Re = \frac{v{f} \times D_i \times \rho_{f}}{\mu_{f}} \rightarrow \frac{" + Latex.toStr(
                    v) + r" \times " + Latex.toStr(D) + r" \times " + Latex.toStr(fluid.density) + r"}{" + Latex.toStr(
                    fluid.mu) + r"} = " + Latex.toStr(Re)))
            return [Re, pr]
        else:
            return Re
    else:
        print('Error! Either fill in mu, nu or a fluid')
        return None
    return Re
