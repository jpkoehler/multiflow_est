import math
from scipy.interpolate import CubicSpline

def HagedornBrownFlow(IP, Pe, Psep, diam, L, depth, rgo):
    # Fluid data input
    ro = 800  # (kg/m³)
    ro_gas = 0.6
    mi = 0.002  # (Pa.s)
    mi_gas = 0.00002
    sigma = 0.020  # (N/m)
    roughness = 0.000045  # (m)
    D = diam * 0.0254  # (m)
    qguess = 0.01  # (m³/s)
    v = (4 * qguess) / (math.pi * (D ** 2))
    Re = (D * ro * v) / mi
    tol = 0.1
    epsilon = roughness / D

    # Iteration for Nodal Analysis
    pwcalc1 = 0
    pwcalc2 = 100
    q_oil = 0
    countpw1 = []
    countpw2 = []
    countit = []
    countqoil = []
    while abs(pwcalc2 - pwcalc1) > tol:
        qguess = qguess + 0.0000001
        q_gas = qguess*rgo
        q_oil = qguess
        A_pipe = math.pi * (D ** 2) / 4
        vsg = q_gas/A_pipe
        vsl = q_oil/A_pipe
        # vm = vsg+vsl
        Nlv = vsl*(ro/(9.81*sigma)) ** (-4)  # Número de velocidade do líquido
        # Número de velocidade do gás
        Ngv = vsg * (ro / (9.81 * sigma)) ** (-4)
        Nd = D * (D*ro / sigma) ** (-2)  # Número de diâmetro do tubo
        # Número de viscosidade do líquido
        Nl = mi * (9.81 / (ro * (sigma ** 3))) ** (-4)
        Adim1 = (Ngv*(Nl ** 0.380))/(Nd ** 2.14)
        CNl = cnlcalc(Nl)
        Adim2 = (Nlv/(Ngv ** 0.575))*((Pe/1.031) ** 0.1)*(CNl/Nd)
        # Correlações por gráfico
        psi = psi_factor(Adim1)
        holdupfactor = holdup_psi(Adim2)
        Hl = psi*holdupfactor  # Holdup de líquido
        Hg = 1 - Hl  # Holdup de gás
        vl = q_oil/(A_pipe*Hl)  # velocidade real de líquido, m/s
        vg = q_gas/(A_pipe*Hg)  # velocidade real de gás, m/s

        Re = (D * ro * vl) / mi

        if Re < 2000:
            f = 16 / Re
        else:
            f = 0.046 * (Re ** (-0.2)) * ((epsilon / D) ** (-0.2))

        DeltaP = ((f * L * ro * (vl ** 2)) / (2 * D)) / 100000
        pwcalc1 = Psep + ((ro * 9.81 * depth) / 100000) + DeltaP
        pwcalc2 = Pe - ((q_oil * 86400) / IP)
        countpw1.append(pwcalc1)
        countpw2.append(pwcalc2)
        countqoil.append(q_oil)
        print(pwcalc1)
        print(pwcalc2)
        print(q_oil)

    wellprod = q_oil * 86400  # m³/dia
    wellprodbarrel = wellprod * 6.2898  # barril/dia

    return [pwcalc1, wellprodbarrel]
