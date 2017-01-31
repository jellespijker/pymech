from IPython.display import Latex
from pymech.units.SI import ureg
from decimal import Decimal

def toStr(obj):
    if type(obj).__name__ == 'str':
        return obj
    elif type(obj).__name__ == 'Quantity':
        retStr = toStr(obj.magnitude) + r" [" + str(obj.units) + r"]"
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
                    a = [i - 2, n - i , power]
                    tStr = retStr[:a[0]] + r"^{" + a[2] + r"}" + retStr[a[0]+ a[1] + 2:]
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

def sqrt(obj, pow = 2):
    if not pow == 2:
        return r"\sqrt[" + str(pow) + r"]{" + toStr(obj) + r"}"
    else:
        return r"\sqrt{" + toStr(obj) + r"}"


def formulaprint(obj):
    return  r"$" + toStr(obj) + r"$"

def display(obj):
    return Latex(formulaprint(obj))

