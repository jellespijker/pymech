import numpy as np

from pymech.fluid.Pipe import *


def Hedstrom_B(fluid=None, pipe=None, tau_y=None, D=None, rho=None, eta_b=None):
    if fluid is not None:
        tau_y = fluid.tau_y
        rho = fluid.rho
        eta_b = fluid.eta_b
    if pipe is not None:
        D = pipe.D_in

    he = (tau_y * D ** 2 * rho) / eta_b ** 2
    return he


def Reynolds_B(fluid=None, pipe=None, rho=None, v=None, D=None, eta_b=None, tau_y=None):
    """ Reynolds number of flow of Bingham plastic mixture [-], Source: Matousek """
    if fluid is not None:
        rho = fluid.rho
        eta_b = fluid.eta_b
        tau_y = fluid.tau_y
    if pipe is not None:
        v = pipe.v
        D = pipe.D_in

    re_b = (rho * v * D) / (eta_b * (1. + ((tau_y * D) / (6. * eta_b * v))))
    return re_b.to_base_units()


def friction_B(Re, D=None, eps=None, pipe=None, pretty=False):
    if type(Re.magnitude).__module__ == 'numpy':
        fr = np.zeros(Re.magnitude.shape)
        count = 0
        for R in Re:
            if flowregime(R) is Regime.LAMINAR:
                if R == 0.:
                    R = 0.001  # sys.float_info.min
                fr[count] = 64. / R
            elif flowregime(R):
                if pipe is not None:
                    D = pipe.D_in
                    eps = pipe.material.epsilon
                fr[count] = 0.25 / (math.log((1 / (3.7 * (D / eps))) + (5.74 / R ** 0.9),
                                             10)) ** 2  # TODO check with @edhoog if this still applies in turbulent flows
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
