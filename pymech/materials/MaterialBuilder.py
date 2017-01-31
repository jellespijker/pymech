from pymech.materials.Steel import Steel
from pymech.materials.Material import Category
from pymech.units.SI import ureg, Q_

def buildSteel(name, id, rho, E, G, A, R_mN, R_eN, sigma_tdWN, sigma_bWN, tau_tWN, rel_cost):
    S = Steel(name, id, category=Category.STEEL)
    S.density = rho * ureg.kg * ureg.m ** -3
    S.E = E * ureg.MPa
    S.G = G * ureg.MPa
    S.A = A / 100.
    S.R_mN = R_mN * ureg.MPa
    S.R_eN = R_eN * ureg.MPa
    S.sigma_tdWN = sigma_tdWN * ureg.MPa
    S.sigma_bWN = sigma_bWN * ureg.MPa
    S.tau_tWN = tau_tWN * ureg.MPa
    S.rel_cost = rel_cost
    S.save("../resources/materials/" + name + ".mat")

def main():
    buildSteel("S235JR", "1.0037", 7800., 210.e3, 81.e3, 26., 360., 235., 140., 180., 105., 1.0)
    buildSteel("S275JR", "1.0044", 7800., 210.e3, 81.e3, 22., 430., 275., 170., 215., 125., 1.05)
    buildSteel("S355JR", "1.0045", 7800., 210.e3, 81.e3, 22., 510., 355., 205., 255., 150., 2.0)
    buildSteel("E295", "1.0050", 7800., 210.e3, 81.e3, 20., 490., 295., 195., 245., 145., 1.1)
    buildSteel("E335", "1.0060", 7800., 210.e3, 81.e3, 16., 590., 335., 235., 290., 180., 1.7)
    buildSteel("E360", "1.0070", 7800., 210.e3, 81.e3, 11., 690., 360., 275., 345., 205., 2.0)
    buildSteel("C22E", "1.1151", 7800., 210.e3, 81.e3, 20., 500., 340., 200., 250., 150., 1.6)
    buildSteel("C40E", "1.1186", 7800., 210.e3, 81.e3, 16., 650., 460., 260., 325., 200., 1.7)
    buildSteel("38Cr2", "1.7003", 7800., 210.e3, 81.e3, 14., 800., 550., 320., 400., 240., 1.7)
    buildSteel("41Cr4", "1.7035", 7800., 210.e3, 81.e3, 11., 1000., 800., 400., 500., 300., 1.7)
    buildSteel("50CrMo4", "1.7228", 7800., 210.e3, 81.e3, 9., 1100., 900., 440., 550., 330., 2)

if __name__ == '__main__':
    main()