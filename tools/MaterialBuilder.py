from pymech.materials.Steel import Steel
from pymech.materials.Fluid import Fluid
from pymech.materials.Material import Category
from pymech.units.SI import ureg, Q_

def buildSteel(name, id, rho, T ,E, G, A, R_mN, R_eN, sigma_tdWN, sigma_bWN, tau_tWN, rel_cost, eps):
    S = Steel(name, id, category=Category.STEEL)
    S.temperature = T * ureg['K']
    S.density = rho * ureg['kg/m**3']
    S.E = E * ureg['MPa']
    S.G = G * ureg['MPa']
    S.A = A / 100.
    S.R_mN = R_mN * ureg['MPa']
    S.R_eN = R_eN * ureg['MPa']
    S.sigma_tdWN = sigma_tdWN * ureg['MPa']
    S.sigma_bWN = sigma_bWN * ureg['MPa']
    S.tau_tWN = tau_tWN * ureg['MPa']
    S.rel_cost = rel_cost
    S.epsilon = eps * ureg['m']
    S.save("../resources/materials/" + name + ".mat")

def buildFluid(name, id, rho_, T, gamma_, mu_, nu_):
    F = Fluid(name, id, category=Category.FLUID, T=T * ureg['K'])
    F._density = rho_
    F._gamma = gamma_
    F._mu = mu_
    F._nu = nu_
    F.getdensity()
    F.getgamma()
    F.getmu()
    F.getnu()
    F.save("../resources/materials/" + name + ".mat")


def main():
    buildSteel("S235JR", "1.0037", 7800., 293.15, 210.e3, 81.e3, 26., 360., 235., 140., 180., 105., 1.0, 4.6e5)
    buildSteel("S275JR", "1.0044", 7800., 293.15, 210.e3, 81.e3, 22., 430., 275., 170., 215., 125., 1.05, 4.6e5)
    buildSteel("S355JR", "1.0045", 7800., 293.15, 210.e3, 81.e3, 22., 510., 355., 205., 255., 150., 2.0, 4.6e5)
    buildSteel("E295", "1.0050", 7800., 293.15, 210.e3, 81.e3, 20., 490., 295., 195., 245., 145., 1.1, 4.6e5)
    buildSteel("E335", "1.0060", 7800., 293.15, 210.e3, 81.e3, 16., 590., 335., 235., 290., 180., 1.7, 4.6e5)
    buildSteel("E360", "1.0070", 7800., 293.15, 210.e3, 81.e3, 11., 690., 360., 275., 345., 205., 2.0, 4.6e5)
    buildSteel("C22E", "1.1151", 7800., 293.15, 210.e3, 81.e3, 20., 500., 340., 200., 250., 150., 1.6, 4.6e5)
    buildSteel("C40E", "1.1186", 7800., 293.15, 210.e3, 81.e3, 16., 650., 460., 260., 325., 200., 1.7, 4.6e5)
    buildSteel("38Cr2", "1.7003", 7800., 293.15, 210.e3, 81.e3, 14., 800., 550., 320., 400., 240., 1.7, 4.6e5)
    buildSteel("41Cr4", "1.7035", 7800., 293.15, 210.e3, 81.e3, 11., 1000., 800., 400., 500., 300., 1.7, 4.6e5)
    buildSteel("50CrMo4", "1.7228", 7800., 293.15, 210.e3, 81.e3, 9., 1100., 900., 440., 550., 330., 2, 4.6e5)

    # Water
    gamma_ = {0.: 9.81 * ureg['kN/m**3'],
              5.: 9.81 * ureg['kN/m**3'],
              10.: 9.81 * ureg['kN/m**3'],
              15.: 9.81 * ureg['kN/m**3'],
              20.: 9.79 * ureg['kN/m**3'],
              25.: 9.78 * ureg['kN/m**3'],
              30.: 9.77 * ureg['kN/m**3'],
              35.: 9.75 * ureg['kN/m**3'],
              40.: 9.73 * ureg['kN/m**3'],
              45.: 9.71 * ureg['kN/m**3'],
              50.: 9.69 * ureg['kN/m**3'],
              55.: 9.67 * ureg['kN/m**3'],
              60.: 9.65 * ureg['kN/m**3'],
              65.: 9.62 * ureg['kN/m**3'],
              70.: 9.59 * ureg['kN/m**3'],
              75.: 9.56 * ureg['kN/m**3'],
              80.: 9.53 * ureg['kN/m**3'],
              85.: 9.50 * ureg['kN/m**3'],
              90.: 9.47 * ureg['kN/m**3'],
              95.: 9.44 * ureg['kN/m**3'],
              100.: 9.40 * ureg['kN/m**3']}

    mu_ = {0.: 1.75e-3 * ureg['Pa*s'],
           5.: 1.52e-3 * ureg['Pa*s'],
           10.: 1.3e-3 * ureg['Pa*s'],
           15.: 1.15e-3 * ureg['Pa*s'],
           20.: 1.02e-3 * ureg['Pa*s'],
           25.: 8.91e-4 * ureg['Pa*s'],
           30.: 8.e-4 * ureg['Pa*s'],
           35.: 7.18e-4 * ureg['Pa*s'],
           40.: 6.51e-4 * ureg['Pa*s'],
           45.: 5.94e-4 * ureg['Pa*s'],
           50.: 5.41e-4 * ureg['Pa*s'],
           55.: 4.98e-4 * ureg['Pa*s'],
           60.: 4.6e-4 * ureg['Pa*s'],
           65.: 4.31e-4 * ureg['Pa*s'],
           70.: 4.02e-4 * ureg['Pa*s'],
           75.: 3.73e-4 * ureg['Pa*s'],
           80.: 3.5e-4 * ureg['Pa*s'],
           85.: 3.3e-4 * ureg['Pa*s'],
           90.: 3.11e-4 * ureg['Pa*s'],
           95.: 2.92e-4 * ureg['Pa*s'],
           100.: 2.82e-4 * ureg['Pa*s']}

    nu_ = {0.: 1.75e-6 * ureg['m**2/s'],
           5.: 1.52e-5 * ureg['m**2/s'],
           10.: 1.3e-6 * ureg['m**2/s'],
           15.: 1.15e-6 * ureg['m**2/s'],
           20.: 1.02e-6 * ureg['m**2/s'],
           25.: 8.94e-7 * ureg['m**2/s'],
           30.: 8.03e-7 * ureg['m**2/s'],
           35.: 7.22e-7 * ureg['m**2/s'],
           40.: 6.56e-7 * ureg['m**2/s'],
           45.: 6.e-7 * ureg['m**2/s'],
           50.: 5.48e-7 * ureg['m**2/s'],
           55.: 5.05e-7 * ureg['m**2/s'],
           60.: 4.67e-7 * ureg['m**2/s'],
           65.: 4.39e-7 * ureg['m**2/s'],
           70.: 4.11e-7 * ureg['m**2/s'],
           75.: 3.83e-7 * ureg['m**2/s'],
           80.: 3.6e-7 * ureg['m**2/s'],
           85.: 3.41e-7 * ureg['m**2/s'],
           90.: 3.22e-7 * ureg['m**2/s'],
           95.: 3.04e-7 * ureg['m**2/s'],
           100.: 2.94e-7 * ureg['m**2/s']}

    density_ = {0.: 1000. * ureg['kg/m**3'],
                5.: 1000. * ureg['kg/m**3'],
                10.: 1000. * ureg['kg/m**3'],
                15.: 1000. * ureg['kg/m**3'],
                20.: 998. * ureg['kg/m**3'],
                25.: 997. * ureg['kg/m**3'],
                30.: 996. * ureg['kg/m**3'],
                35.: 994. * ureg['kg/m**3'],
                40.: 992. * ureg['kg/m**3'],
                45.: 990. * ureg['kg/m**3'],
                50.: 988. * ureg['kg/m**3'],
                55.: 986. * ureg['kg/m**3'],
                60.: 984. * ureg['kg/m**3'],
                65.: 981. * ureg['kg/m**3'],
                70.: 978. * ureg['kg/m**3'],
                75.: 975. * ureg['kg/m**3'],
                80.: 971. * ureg['kg/m**3'],
                85.: 968. * ureg['kg/m**3'],
                90.: 965. * ureg['kg/m**3'],
                95.: 962. * ureg['kg/m**3'],
                100.: 958. * ureg['kg/m**3']}

    buildFluid("Water", "0.0001", density_, 293.15, gamma_, mu_, nu_)


if __name__ == '__main__':
    main()