from decimal import Decimal

from IPython.display import Latex
import re


def toStr(obj):
    if type(obj).__name__ == 'str':
        return obj
    elif type(obj).__name__ == 'Quantity':
        retStr = toStr(obj.magnitude) + unitStr(obj.units)
        tStr = ""
        for i in range(1, len(retStr)):
            try:
                if retStr[i] == '*' and retStr[i - 1] == '*':
                    power = ""
                    for n in range(i + 2, len(retStr)):
                        if ord(retStr[n]) >= 48 and ord(retStr[n]) <= 57:
                            power += retStr[n]
                        else:
                            break
                    a = [i - 2, n - i, power]
                    tStr = retStr[:a[0]] + r"^{" + a[2] + r"}" + retStr[a[0] + a[1] + 2:]
                    retStr = tStr
            except IndexError:
                return tStr
        return retStr
    else:
        retStr = '%.2E' % Decimal(obj)
        for i in range(1, len(retStr)):
            if retStr[i:i + 4] == 'E+00':
                retStr = retStr[:i]
                break
            elif retStr[i] == 'E' and retStr[i + 2] == '0':
                if retStr[i + 1] == '+':
                    retStr = retStr[:i] + r" \cdot 10^{" + retStr[i + 3] + r"}"
                    break
                else:
                    retStr = retStr[:i] + r" \cdot 10^{-" + retStr[i + 3] + r"}"
                    break
            elif retStr[i] == 'E':
                if retStr[i + 1] == '+':
                    retStr = retStr[:i] + r" \cdot 10^{" + retStr[i + 1:] + r"}"
                    break
                else:
                    retStr = retStr[:i] + r" \cdot 10^{-" + retStr[i + 1:] + r"}"
                    break
        return retStr
    return


def unitStr(obj):
    unit = str(obj)
    unit = unit.replace("yocto", "y")
    unit = unit.replace("zepto", "z")
    unit = unit.replace("atto", "a")
    unit = unit.replace("femto", "f")
    unit = unit.replace("pico", "p")
    unit = unit.replace("nano", "n")
    unit = unit.replace("micro", r"\mu")
    unit = unit.replace("milli", "m")
    unit = unit.replace("centi", "c")
    unit = unit.replace("deci", "d")
    unit = unit.replace("deca", "da")
    unit = unit.replace("hecto", "h")
    unit = unit.replace("kilo", "k")
    unit = unit.replace("mega", "M")
    unit = unit.replace("giga", "G")
    unit = unit.replace("tera", "T")
    unit = unit.replace("peta", "P")
    unit = unit.replace("exa", "E")
    unit = unit.replace("zetta", "Z")
    unit = unit.replace("yotta", "Y")

    unit = unit.replace("joule", "J")
    unit = unit.replace("newton", "N")
    unit = unit.replace("meter", "m")
    unit = unit.replace("second", "s")
    unit = unit.replace("ampere", "A")
    unit = unit.replace("candela", "cd")
    unit = unit.replace("gram", "g")
    unit = unit.replace("mole", "mol")
    unit = unit.replace("kelvin", "K")
    unit = unit.replace("celsius", r"^{\circ} C")
    unit = unit.replace("degC", r"^{\circ} C")
    unit = unit.replace("radian", "rad")
    unit = unit.replace("degree", r"^{\circ}")
    unit = unit.replace("volt", "V")
    unit = unit.replace("farad", "F")
    unit = unit.replace("ohm", r"\Omega")
    unit = unit.replace("siemens", "mho")
    unit = unit.replace("Tesla", "T")
    unit = unit.replace("elementary_charge", "e")
    unit = unit.replace("watt", "W")
    unit = unit.replace("hour", "h")
    unit = unit.replace("hertz", "Hz")
    unit = unit.replace("revolutions_per_minute", "rpm")
    unit = unit.replace("lumen", "lm")
    unit = unit.replace("lux", "lx")
    unit = unit.replace("horsepower", "hp")
    unit = unit.replace("pascal", "Pa")
    unit = unit.replace("minute", "min")
    unit = unit.replace("nautical_mile", "nmi")
    unit = unit.replace("knot", "kt")
    unit = unit.replace("poise", "P")
    unit = unit.replace("stokes", "St")
    unit = unit.replace("liter", "L")

    unit = unit.replace("_", "")
    unit = unit.replace("dimensionless", "-")

    unit = re.sub(r"(\*\*\ (-?\b\d\d{0,8}\b))", r"^{\2}", unit)

    unit = unit.replace("*", r"\cdot")

    for i in range(1, len(unit)):
        if unit[i] == r"/":
            unit = frac(unit[:i - 1], unit[i + 2:])
    return r" \left[" + unit + r"\right]"


def array(obj):
    cStr = "c"
    for n in range(1, len(obj[0]) - 1):
        cStr += "c"
    retStr = r"\begin{array}{" + cStr + r"}"

    for i in range(len(obj)):
        for j in range(len(obj[i])):
            retStr += toStr(obj[i][j])
            if not j == len(obj[i]) - 1:
                retStr += r"&"
        if not i == len(obj) - 1:
            retStr += r"\\ "

    retStr += r"\end{array}"
    return retStr


def frac(top, bottom):
    return r"\frac{" + toStr(top) + r"}{" + toStr(bottom) + r"}"


def sqrt(obj, pow=2):
    if not pow == 2:
        return r"\sqrt[" + str(pow) + r"]{" + toStr(obj) + r"}"
    else:
        return r"\sqrt{" + toStr(obj) + r"}"


def formulaprint(obj):
    return r"$" + toStr(obj) + r"$"


def display(obj):
    return Latex(formulaprint(obj))

def pow(obj, power=2):
    return r"\left(" + toStr(obj) + r"\right)^{" + str(power) + r"}"