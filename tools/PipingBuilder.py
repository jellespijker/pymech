from pymech.fluid.Pipe import Pipe
from pymech.materials.Metal import Steel
from pymech.materials.Plastic import Plastic
from pymech.units.SI import ureg, Q_


def buildPipe(name, ID, L, D_out, wt, material, standard):
    P = Pipe(ID, L * ureg['m'], D_out * ureg['mm'], wt * ureg['mm'], material)
    P.Standard = standard
    P.save("../pymech/resources/piping/" + name + ".pip")


def main():
    material = Steel()
    material.load("../pymech/resources/materials/S235JR.mat")

    buildPipe('1_8inch-Sc40', 0, 1., 10.3, 1.73, material, 'ASME B36.10')
    buildPipe('1_4inch-Sc40', 0, 1., 13.7, 2.24, material, 'ASME B36.10')
    buildPipe('3_8inch-Sc40', 0, 1., 17.1, 2.31, material, 'ASME B36.10')
    buildPipe('1_2inch-Sc40', 0, 1., 21.3, 2.77, material, 'ASME B36.10')
    buildPipe('3_4inch-Sc40', 0, 1., 26.7, 2.87, material, 'ASME B36.10')
    buildPipe('1.inch-Sc40', 0, 1., 33.4, 3.38, material, 'ASME B36.10')
    buildPipe('1.1_4inch-Sc40', 0, 1., 42.2, 3.56, material, 'ASME B36.10')
    buildPipe('1.1_2inch-Sc40', 0, 1., 48.3, 3.68, material, 'ASME B36.10')
    buildPipe('2.inch-Sc40', 0, 1., 60.3, 3.91, material, 'ASME B36.10')
    buildPipe('2.1_2inch-Sc40', 0, 1., 73., 5.16, material, 'ASME B36.10')
    buildPipe('3.inch-Sc40', 0, 1., 88.9, 5.49, material, 'ASME B36.10')
    buildPipe('3.1_2inch-Sc40', 0., 1., 101.6, 5.74, material, 'ASME B36.10')
    buildPipe('4.inch-Sc40', 0, 1., 114.3, 6.02, material, 'ASME B36.10')
    buildPipe('5.inch-Sc40', 0, 1., 141.3, 6.55, material, 'ASME B36.10')
    buildPipe('6.inch-Sc40', 0, 1., 168.3, 7.11, material, 'ASME B36.10')
    buildPipe('8.inch-Sc40', 0, 1., 219.1, 8.18, material, 'ASME B36.10')
    buildPipe('10.inch-Sc40', 0, 1., 273.1, 9.27, material, 'ASME B36.10')
    buildPipe('12.inch-Sc40', 0, 1., 323.9, 10.31, material, 'ASME B36.10')
    buildPipe('14.inch-Sc40', 0, 1., 355.6, 11.10, material, 'ASME B36.10')
    buildPipe('16.inch-Sc40', 0, 1., 406.4, 12.7, material, 'ASME B36.10')
    buildPipe('18.inch-Sc40', 0, 1., 457.2, 14.27, material, 'ASME B36.10')
    buildPipe('20.inch-Sc40', 0, 1., 508., 15.06, material, 'ASME B36.10')
    buildPipe('24.inch-Sc40', 0, 1., 609.6, 17.45, material, 'ASME B36.10')

    material = Plastic()
    material.load("../pymech/resources/materials/PP.mat")
    buildPipe('16.PVC-U', 0, 1., 16., 1.2, material, 'EN ISO 15874')
    buildPipe('20.PVC-U', 0, 1., 20., 1.5, material, 'EN ISO 15874')
    buildPipe('25.PVC-U', 0, 1., 25., 1.9, material, 'EN ISO 15874')
    buildPipe('32.PVC-U', 0, 1., 32., 2.4, material, 'EN ISO 15874')
    buildPipe('40.PVC-U', 0, 1., 40., 3., material, 'EN ISO 15874')
    buildPipe('50.PVC-U', 0, 1., 50., 3.7, material, 'EN ISO 15874')
    buildPipe('63.PVC-U', 0, 1., 63., 4.7, material, 'EN ISO 15874')
    buildPipe('75.PVC-U', 0, 1., 75., 5.6, material, 'EN ISO 15874')
    buildPipe('90.PVC-U', 0, 1., 90., 6.7, material, 'EN ISO 15874')
    buildPipe('110.PVC-U', 0, 1., 110., 8.1, material, 'EN ISO 15874')
    buildPipe('125.PVC-U', 0, 1., 125., 9.2, material, 'EN ISO 15874')
    buildPipe('140.PVC-U', 0, 1., 140., 10.3, material, 'EN ISO 15874')
    buildPipe('160.PVC-U', 0, 1., 160., 11.8, material, 'EN ISO 15874')

if __name__ == '__main__':
    main()
