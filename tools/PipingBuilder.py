from pymech.fluid.Pipe import Pipe
from pymech.materials.Steel import Steel
from pymech.units.SI import ureg, Q_


def buildPipe(name, ID, L, D_out, wt, material):
    P = Pipe(ID, L * ureg['m'], D_out * ureg['mm'], wt * ureg['mm'], material)
    P.save("../pymech/resources/piping/" + name + ".pip")


def main():
    material = Steel()
    material.load("../pymech/resources/materials/S235JR.mat")

    buildPipe('1_8inch-Sc40', 0, 1., 10.3, 1.73, material)
    buildPipe('1_4inch-Sc40', 0, 1., 13.7, 2.24, material)
    buildPipe('3_8inch-Sc40', 0, 1., 17.1, 2.31, material)
    buildPipe('1_2inch-Sc40', 0, 1., 21.3, 2.77, material)
    buildPipe('3_4inch-Sc40', 0, 1., 26.7, 2.87, material)
    buildPipe('1.inch-Sc40', 0, 1., 33.4, 3.38, material)
    buildPipe('1.1_4inch-Sc40', 0, 1., 42.2, 3.56, material)
    buildPipe('1.1_2inch-Sc40', 0, 1., 48.3, 3.68, material)
    buildPipe('2.inch-Sc40', 0, 1., 60.3, 3.91, material)
    buildPipe('2.1_2inch-Sc40', 0, 1., 73., 5.16, material)
    buildPipe('3.inch-Sc40', 0, 1., 88.9, 5.49, material)
    buildPipe('3.1_2inch-Sc40', 0., 1., 101.6, 5.74, material)
    buildPipe('4.inch-Sc40', 0, 1., 114.3, 6.02, material)
    buildPipe('5.inch-Sc40', 0, 1., 141.3, 6.55, material)
    buildPipe('6.inch-Sc40', 0, 1., 168.3, 7.11, material)
    buildPipe('8.inch-Sc40', 0, 1., 219.1, 8.18, material)
    buildPipe('10.inch-Sc40', 0, 1., 273.1, 9.27, material)
    buildPipe('12.inch-Sc40', 0, 1., 323.9, 10.31, material)
    buildPipe('14.inch-Sc40', 0, 1., 355.6, 11.10, material)
    buildPipe('16.inch-Sc40', 0, 1., 406.4, 12.7, material)
    buildPipe('18.inch-Sc40', 0, 1., 457.2, 14.27, material)
    buildPipe('20.inch-Sc40', 0, 1., 508., 15.06, material)
    buildPipe('24.inch-Sc40', 0, 1., 609.6, 17.45, material)


if __name__ == '__main__':
    main()
