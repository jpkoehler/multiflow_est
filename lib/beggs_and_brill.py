import math

def flow_regime(Nfr, laml, L1, L2, L3, L4):
    # Regime 1 - Segregated flow
    if (((laml < 0.01) and (Nfr < L1)) or ((laml >= 0.01) and (Nfr < L2))):
        regime = 1

    # Regime 2 - Transition flow
    if ((laml >= 0.01) and (L2 < Nfr) and (Nfr <= L3)):
        regime = 2

    # Regime 3 - Intermittent flow
    if ((((0.01 <= laml) and (laml < 0.4)) and ((L3 < Nfr) and (Nfr < L1))) or (
            (laml >= 0.4) and (L3 < Nfr) and (Nfr <= L4))):
        regime = 3

    # Regime 4 - Distributed flow
    if (((laml < 0.4) and (Nfr >= L1)) or ((laml >= 0.4) and (Nfr > L4))):
        regime = 4

    return regime


def liq_holdup(Nfr, Nvl, laml, angle, regime):
    angle = angle * 3.1415 / 180
    if (regime == 1):
        a = 0.98
        b = 0.4846
        c = 0.0868
        if (angle >= 0):
            d = 0.011
            e = -3.768
            f = 3.539
            g = -1.614
        else:
            d = 4.7
            e = -0.3692
            f = 0.1244
            g = -0.5056

    if (regime == 3):
        a = 0.845
        b = 0.5351
        c = 0.0173
        if (angle >= 0):
            d = 2.96
            e = 0.305
            f = -0.4473
            g = 0.0978
        else:
            d = 4.7
            e = -0.3692
            f = 0.1244
            g = -0.5056

    if (regime == 4):
        a = 1.065
        b = 0.5824
        c = 0.0609
        if (angle >= 0):
            d = 1
            e = 0
            f = 0
            g = 0
        else:
            d = 4.7
            e = -0.3692
            f = 0.1244
            g = -0.5056

    # Calculate holdup
    corr = (1 - laml) * math.log(d * laml ** e * Nvl ** f * Nfr ** g)
    if (corr < 0):
        corr = 0

    psi = 1 + corr * (math.sin(1.8 * angle) - (math.sin(1.8 * angle)) ** 3 / 3)
    ylo = a * laml ** b / Nfr ** c
    if (ylo < laml):
        ylo = laml

    Hl = ylo * psi
    return Hl

def beggs_brill_flow(IP, Pe, Psep, diam, L, depth, rgo):
    #Fluid data input
    ro = 800  #(kg/m³)
    ro_gas = 0.6
    mi = 0.002 #(Pa.s)
    mi_gas = 0.00002
    sigma = 0.020 #(N/m)
    roughness = 0.000045 #(m)
    D = diam * 0.0254  #(m)
    qguess = Pe * IP / 86400   #(m³/s)
    v = (4 * qguess) / (math.pi * (D ** 2))
    Re = (D * ro * v) / mi
    tol = 0.1
    epsilon = roughness / D
    angle = 90
    max_iterations = 10000  
    iterations = 0

    #Iteration for Nodal Analysis
    pwcalc1 = 0
    pwcalc2 = 100
    q_oil = 0
    countpw1 = []
    countpw2 = []
    countit = []
    countqoil = []
    while abs(pwcalc2 - pwcalc1) > tol  and iterations < max_iterations:
        iterations += 1
        if iterations == max_iterations:
            print("Atenção: Iteração máxima atingida, possível falha na convergência.")
        qguess = qguess + 0.0000001
        q_gas = qguess*rgo
        q_oil = qguess
        A_pipe = math.pi * (D ** 2) / 4
        vsg = q_gas/A_pipe
        vsl = q_oil/A_pipe
        vm = vsg+vsl
        Nlv = vsl*(ro/(9.81*sigma)) ** (-4)  # Número de velocidade do líquido
        Ngv = vsg * (ro / (9.81 * sigma)) ** (-4)  # Número de velocidade do gás
        Nd = D * (D*ro / sigma ) ** (-2)  # Número de diâmetro do tubo
        Nl = mi * (9.81 / (ro * (sigma ** 3))) ** (-4)  # Número de viscosidade do líquido

        # Determine flow regime
        Nfr = vm ** 2 / (D / 12) / 32.174  # Froude number
        sigl = 34  #placeholder
        Nvl = 1.938 * vsl * (ro / sigl) ** 0.25  # Liquid velocity number
        laml = vsl / vm  # Input liquid fraction
        lamg = 1 - laml  # Input gas fraction
        L1 = 316 * laml ** 0.302  # Dimensionless constants
        L2 = 0.0009252 * laml ** -2.4684
        L3 = 0.1 * laml ** -1.4516
        L4 = 0.5 * laml ** -6.738

        regime = flow_regime(Nfr, laml, L1, L2, L3, L4)


        Hl = liq_holdup(Nfr, Nvl, laml, angle, regime)   #Holdup de líquido
        Hg = 1 - Hl     #Holdup de gás
        vl = q_oil/(A_pipe*Hl)   #velocidade real de líquido, m/s
        vg = q_gas/(A_pipe*Hg)   #velocidade real de gás, m/s

        '''#cálculo de propriedades da mistura
        f0 = q_oil/(q_oil+q_gas)
        f1 = 1-f0
        romist = f0*ro + f1*ro_gas
        mimist = f0*mi + f1*mi_gas'''

        Re = (D * ro * vl) / mi

        if Re < 2000:
            f = 16 / Re
        else:
            f = 0.046 * (Re ** (-0.2)) * ((epsilon / D) ** (-0.2))

        DeltaP = ((f * L * ro * (vl ** 2)) / (2 * D)) / 1000000
        pwcalc1 = Psep + ((ro * 9.81 * depth) / 100000) + DeltaP
        pwcalc2 = Pe - ((q_oil * 86400) / IP)
        countpw1.append(pwcalc1)
        countpw2.append(pwcalc2)
        countqoil.append(q_oil)

    wellprod = q_oil * 86400  # m³/dia
    wellprodbarrel = wellprod * 6.2898  # barril/dia
    
    return [pwcalc1, wellprodbarrel]
