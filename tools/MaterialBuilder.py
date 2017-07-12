import numpy as np
from pymech.materials.Material import Material
from pymech.materials.Plastic import Plastic
from pymech.materials.Metal import Steel
from pymech.materials.Fluid import Fluid, BinghamFluid
from pymech.materials.Material import Category
from pymech.units.SI import ureg, Q_, g


def buildSteel(name, id, rho, T, E, G, A, R_mN, R_eN, sigma_tdWN, sigma_bWN, tau_tWN, rel_cost, eps):
    S = Steel(name=name, id=id, rho=rho * ureg['kg/m**3'], T=T * ureg['degC'], E=E * ureg['N/mm**2'],
              G=G * ureg['N/mm**2'], A=A, R_mN=R_mN * ureg['MPa'], R_eN=R_eN * ureg['MPa'],
              sigma_tdWN=sigma_tdWN * ureg['MPa'],
              sigma_bWN=sigma_bWN * ureg['MPa'], tau_tWN=tau_tWN * ureg['MPa'], rel_cost=rel_cost,
              epsilon=eps * ureg['m'])
    S.save("../pymech/resources/materials/" + name + ".mat")


def buildPlastic(name, id, rho, eps):
    P = Plastic(name=name, id=id, rho=rho * ureg['kg/m**3'], T=15. * ureg['degC'])
    P.epsilon = eps * ureg['m']
    P.save("../pymech/resources/materials/" + name + ".mat")


def buildFluid(name, id, rho, T, mu):
    F = Fluid(name, id, T=T * ureg['degC'], rho=rho, mu=mu)
    F.nu
    F.save("../pymech/resources/materials/" + name + ".mat")


def buildBingham(name, id, rho, T, mu, tau_y, eta_b):
    B = BinghamFluid(name=name, id=id, T=T * ureg['degC'], rho=rho, mu=mu, tau_y=tau_y, eta_b=eta_b)
    B.save("../pymech/resources/materials/" + name + ".mat")


def main():
<<<<<<< HEAD
    buildSteel("S235JR", "1.0037", 7800., 293.15, 210.e3, 81.e3, 26., 360., 235., 140., 180., 105., 1.0, 4.6e-5)
    buildSteel("S275JR", "1.0044", 7800., 293.15, 210.e3, 81.e3, 22., 430., 275., 170., 215., 125., 1.05, 4.6e-5)
    buildSteel("S355JR", "1.0045", 7800., 293.15, 210.e3, 81.e3, 22., 510., 355., 205., 255., 150., 2.0, 4.6e-5)
    buildSteel("E295", "1.0050", 7800., 293.15, 210.e3, 81.e3, 20., 490., 295., 195., 245., 145., 1.1, 4.6e-5)
    buildSteel("E335", "1.0060", 7800., 293.15, 210.e3, 81.e3, 16., 590., 335., 235., 290., 180., 1.7, 4.6e-5)
    buildSteel("E360", "1.0070", 7800., 293.15, 210.e3, 81.e3, 11., 690., 360., 275., 345., 205., 2.0, 4.6e-5)
    buildSteel("C22E", "1.1151", 7800., 293.15, 210.e3, 81.e3, 20., 500., 340., 200., 250., 150., 1.6, 4.6e-5)
    buildSteel("C40E", "1.1186", 7800., 293.15, 210.e3, 81.e3, 16., 650., 460., 260., 325., 200., 1.7, 4.6e-5)
    buildSteel("38Cr2", "1.7003", 7800., 293.15, 210.e3, 81.e3, 14., 800., 550., 320., 400., 240., 1.7, 4.6e-5)
    buildSteel("41Cr4", "1.7035", 7800., 293.15, 210.e3, 81.e3, 11., 1000., 800., 400., 500., 300., 1.7, 4.6e-5)
    buildSteel("50CrMo4", "1.7228", 7800., 293.15, 210.e3, 81.e3, 9., 1100., 900., 440., 550., 330., 2, 4.6e-5)
=======
    buildSteel("S235JR", "1.0037", 7800., 15., 210.e3, 81.e3, 26., 360., 235., 140., 180., 105., 1.0, 4.6e-5)
    buildSteel("S275JR", "1.0044", 7800., 15., 210.e3, 81.e3, 22., 430., 275., 170., 215., 125., 1.05, 4.6e-5)
    buildSteel("S355JR", "1.0045", 7800., 15., 210.e3, 81.e3, 22., 510., 355., 205., 255., 150., 2.0, 4.6e-5)
    buildSteel("E295", "1.0050", 7800., 15., 210.e3, 81.e3, 20., 490., 295., 195., 245., 145., 1.1, 4.6e-5)
    buildSteel("E335", "1.0060", 7800., 15., 210.e3, 81.e3, 16., 590., 335., 235., 290., 180., 1.7, 4.6e-5)
    buildSteel("E360", "1.0070", 7800., 15., 210.e3, 81.e3, 11., 690., 360., 275., 345., 205., 2.0, 4.6e-5)
    buildSteel("C22E", "1.1151", 7800., 15., 210.e3, 81.e3, 20., 500., 340., 200., 250., 150., 1.6, 4.6e-5)
    buildSteel("C40E", "1.1186", 7800., 15., 210.e3, 81.e3, 16., 650., 460., 260., 325., 200., 1.7, 4.6e-5)
    buildSteel("38Cr2", "1.7003", 7800., 15., 210.e3, 81.e3, 14., 800., 550., 320., 400., 240., 1.7, 4.6e-5)
    buildSteel("41Cr4", "1.7035", 7800., 15., 210.e3, 81.e3, 11., 1000., 800., 400., 500., 300., 1.7, 4.6e-5)
    buildSteel("50CrMo4", "1.7228", 7800., 15., 210.e3, 81.e3, 9., 1100., 900., 440., 550., 330., 2, 4.6e-5)
    buildSteel("Cf53", "1.1213", 7800., 15., 210.e3, 81.e3, 12., 740., 510., 295., 370., 220., 2., 4.6e-5)
    buildSteel("C60E", "1.1221", 7800., 15., 210.e3, 81.e3, 6., 750., 520., 300., 375., 225., 1.8, 4.6e-5)
>>>>>>> 5458352... Resturcturing of Materials module

    buildPlastic("PP", " 9003-07-0", 855., 1.5e-6)

    # Water
    mu = {0.: 1.75e-3 * ureg['Pa*s'],
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

    density = {0.: 1000. * ureg['kg/m**3'],
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

    buildFluid("Water", "0.0001", density, 15., mu)

    #Benzene
    mu = {25.: 6.03e-4 * ureg['Pa*s'],
          50.: 4.2e-4 * ureg['Pa*s']}
    density = {25.: 876. * ureg['kg/m**3'],
               50.: 860. * ureg['kg/m**3']}
    buildFluid("Benzene", "0.0002", density, 15., mu)

    density = 2100 * ureg['kg/m**3']
    mu = 1.62 * ureg['Pa * s']
    tau_y = 100. * ureg['Pa']
    etha_b = 1.62 * ureg['Pa*s']
    buildBingham("12417-GP-5to1-Z1", "GP.0000", density, 15., mu, tau_y, etha_b)


if __name__ == '__main__':
    main()
