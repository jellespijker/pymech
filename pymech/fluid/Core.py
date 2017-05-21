from enum import Enum
import sys
import numpy as np

from pymech.units.SI import ureg, g
from pymech.materials.Fluid import Fluid
from pymech.fluid.Pipe import *
import pymech.print.Latex as Latex


class Regime(Enum):
    LAMINAR = 1
    TURBULENT = 2
    TRANSITIONAL = 3


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
        Re = (v * D.to('m') * fluid.rho) / fluid.mu
        Re = Re.to_base_units()
        if pretty:
            pr = Latex.display(Latex.toStr(
                r"Re = \frac{v{f} \times D_i \times \rho_{f}}{\mu_{f}} \rightarrow \frac{" + Latex.toStr(
                    v) + r" \times " + Latex.toStr(D) + r" \times " + Latex.toStr(fluid.rho) + r"}{" + Latex.toStr(
                    fluid.mu) + r"} = " + Latex.toStr(Re)))
            return [Re, pr]
        else:
            return Re
    else:
        print('Error! Either fill in mu, nu or a fluid')
        return None
    return Re


def flowrate(v, A, pretty=False):
    Q = v * A
    Q = Q.to_base_units()
    if pretty:
        pr = Latex.display(Latex.toStr(
            r"Q_{f} = v_{f} \times A \rightarrow " + Latex.toStr(v) + r" \times " + Latex.toStr(
                A) + r" = " + Latex.toStr(Q)))
        return [Q, pr]
    return Q


def Darcy(f, L, D, v, fluid=None, rho=None, dP=False, pretty=False):
    if fluid is not None:
        rho = fluid.rho
    darcy = f * (L / D)
    if dP and rho is not None:
        darcy *= (v ** 2 * rho) / 2
        darcy.ito('Pa')
    else:
        darcy *= v ** 2 / (2 * g)
        darcy.ito('m')
    return darcy


def flowregime(Re):
    if Re < 2000:
        return Regime.LAMINAR
    elif Re < 4000:
        return Regime.TRANSITIONAL
    else:
        return Regime.TURBULENT


def HagenPoiseuille(L, D, v, mu=None, fluid=None, rho=None, dP=False, pretty=False):  # TODO check
    if fluid is not None:
        mu = fluid.mu
        rho = fluid.rho
    hp = 32. * mu * L * v
    if dP:
        hp /= D ** 2
        hp.ito('Pa')
    else:
        hp /= rho * g * D ** 2
        hp.ito('m')
    return hp


def friction(Re, D=None, eps=None, pipe=None, pretty=False):
    if type(Re.magnitude).__module__ == 'numpy':
        fr = np.zeros(Re.magnitude.shape)
        count = 0
        for R in Re:
            if flowregime(R) is Regime.LAMINAR:
                if R == 0.:
                    R = 1.e-310  # sys.float_info.min
                fr[count] = 64. / R
            elif flowregime(R):
                if pipe is not None:
                    D = pipe.D_in
                    eps = pipe.material.epsilon
                fr[count] = 0.25 / (math.log((1 / (3.7 * (D / eps))) + (5.74 / R ** 0.9), 10)) ** 2
            count += 1
        return fr
    else:
        if flowregime(Re) is Regime.LAMINAR:
            if Re == 0.:
                Re = 0.001  # sys.float_info.min
            return 64. / Re
        elif flowregime(Re):
            if pipe is not None:
                D = pipe.D_in
                eps = pipe.material.epsilon
            return 0.25 / (math.log((1 / (3.7 * (D / eps))) + (5.74 / Re ** 0.9), 10)) ** 2


def fluidspeed(Q, A):
    return Q / A


def hydrostatic_headloss(z_from, z_to, fluid=None, rho=None, dP=False, pretty=False):
    if fluid is not None:
        rho = fluid.rho
    if dP:
        return rho * g * (z_to - z_from)
    else:
        return z_to - z_from


def hl_to_dp(hl, rho=None, fluid=None, pretty=False):
    if fluid is not None:
        rho = fluid.rho
    return rho * g * hl


def dp_to_hl(dp, rho=None, fluid=None, pretty=False):
    if fluid is not None:
        rho = fluid.rho
    return dp / (rho * g)


def I_m(friction, pipe=None, D=None, v=None):
    """ Hydraulic gradient for pseudo-homogeneous mixture flow [-], Source: Matousek"""
    if pipe is not None:
        D = pipe.D_in
        v = pipe.v
    return (friction / D) * (v ** 2 / (2 * g))
