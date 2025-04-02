import math
from scipy.interpolate import CubicSpline
import csv

def HagedornBrownFlow(IP, Pe, Psep, diam, L, depth, rgo):
    # Fluid data input
    ro = 800  # (kg/m³)
    ro_gas = 0.6
    mi = 0.002  # (Pa.s)
    mi_gas = 0.00002
    sigma = 0.020  # (N/m)
    roughness = 0.000045  # (m)
    D = diam * 0.0254  # (m)
    qguess = 0.0001  # (m³/s)
    v = (4 * qguess) / (math.pi * (D ** 2))
    Re = (D * ro * v) / mi
    tol = 1
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


#Reading csv for H&B Correlation graphs
#Graph 1 - Psi Factor
file_path_graph1 = "database/psi_factor.csv"
graph1data = []
with open(file_path_graph1, mode='r') as file:
    reader = csv.reader(file)
    graph1data = list(reader)
print(graph1data)
xgraph1=[]
ygraph1=[]
for i in range(1,len(graph1data)):
    xgraph1.append(graph1data[i][0])
    ygraph1.append(graph1data[i][1])

#Função do gráfico por Interpolação de Spline Cúbica para dados do gráfico 1
psi_factor = CubicSpline(xgraph1, ygraph1)

#Graph 2 - CNl
file_path_graph2 = "database/cnlcalc.csv"
graph2data = []
with open(file_path_graph2, mode='r') as file:
    reader = csv.reader(file)
    graph2data = list(reader)
print(graph2data)
xgraph2=[]
ygraph2=[]
for i in range(1,len(graph2data)):
    xgraph2.append(graph2data[i][0])
    ygraph2.append(graph2data[i][1])

#Função do gráfico por Interpolação de Spline Cúbica para dados do gráfico 2
cnlcalc = CubicSpline(xgraph2, ygraph2)

#Graph 3 - Holdup líq/psi
file_path_graph3 = "database/holdup_psi.csv"
graph3data = []
with open(file_path_graph3, mode='r') as file:
    reader = csv.reader(file)
    graph3data = list(reader)
print(graph3data)
xgraph3=[]
ygraph3=[]
for i in range(1,len(graph3data)):
    xgraph3.append(graph3data[i][0])
    ygraph3.append(graph3data[i][1])

#Função do gráfico por Interpolação de Spline Cúbica para dados do gráfico 3
holdup_psi = CubicSpline(xgraph3, ygraph3)


