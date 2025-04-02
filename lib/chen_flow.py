import math

def chen_flow(IP, Pe, Psep, diam, L, depth):
    ro = 800
    mi = 0.002
    roughness = 0.000045
    D = diam * 0.0254
    qguess = 0.01
    v = (4 * qguess) / (math.pi * (D ** 2))
    Re = (D * ro * v) / mi
    fatrito = (1 / (-2 * math.log10(((roughness / D) / 3.7065) - (5.0452 / Re) * math.log10(
        ((1 / 2.8257) * ((roughness / D) ** 1.1098)) + (5.8506 / (Re ** 0.8981)))))) ** 2
    Deltaatr = (fatrito * ((ro / 2) * (L / D) * (v ** 2))) / 100000
    tol = 0.0001
    pwcalc1 = 0
    pwcalc2 = 1
    wellprod = qguess * 86400
    wellprodbarrel = 0

    while abs(pwcalc1) - abs(pwcalc2) < tol:
        qguess += 0.000001
        v = (4 * qguess) / (math.pi * (D ** 2))
        Re = (D * ro * v) / mi
        fatrito = (1 / (-2 * math.log10(((roughness / D) / 3.7065) - (5.0452 / Re) * math.log10(
            ((1 / 2.8257) * ((roughness / D) ** 1.1098)) + (5.8506 / (Re ** 0.8981)))))) ** 2
        Deltaatr = (fatrito * ((ro / 2) * (L / D) * (v ** 2))) / 100000
        pwcalc1 = Psep + ((ro * 9.81 * depth) / 100000) + Deltaatr
        pwcalc2 = Pe - ((qguess * 86400) / IP)
    wellprod = qguess * 86400  # m³/dia
    wellprodbarrel = wellprod * 6.2898  # barril/dia

    return [pwcalc1, wellprodbarrel]
