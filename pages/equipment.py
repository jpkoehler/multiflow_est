import base64
import time

import streamlit as st
import math
from PIL import Image
import numpy
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def app():
    st.title('Multiphase Flow Estimation')
    st.header('Dados de Entrada')

    IP = st.number_input('IP:', 1, 100, 10)
    Pe = st.number_input('Pe:', 1, 1000, 300)
    Psep = st.number_input('Psep:', 0, 100, 65)
    diam = st.number_input('Diameter:', 0, 20, 8)
    L = st.number_input('Length:', 0, 10000, 6)
    depth = st.number_input('Depth:', 0, 10000, 3)
    # st.write("Processos adicionais:")
    # CO2 = st.checkbox("CO2")
    # H2S = st.checkbox("H2S")
    # lavagem = st.checkbox("Lavagem de óleo")

    button1 = st.button('Calculate')

    if st.session_state.get('button1') != True:
        st.session_state['button1'] = button1

    if (button1):
        with st.spinner('Processando...'):
            time.sleep(2)
        st.success('Sucesso!')

    if st.session_state['button1']:

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
            qguess += 0.001
            v = (4 * qguess) / (math.pi * (D ** 2))
            Re = (D * ro * v) / mi
            fatrito = (1 / (-2 * math.log10(((roughness / D) / 3.7065) - (5.0452 / Re) * math.log10(
                ((1 / 2.8257) * ((roughness / D) ** 1.1098)) + (5.8506 / (Re ** 0.8981)))))) ** 2
            Deltaatr = (fatrito * ((ro / 2) * (L / D) * (v ** 2))) / 100000
            pwcalc1 = Psep + ((ro * 9.81 * depth) / 100000) + Deltaatr
            pwcalc2 = Pe - ((qguess * 86400) / IP)
        wellprod = qguess * 86400  # m³/dia
        wellprodbarrel = wellprod * 6.2898  # barril/dia

        chenresult = [pwcalc1, wellprodbarrel]

        dataknock = pd.DataFrame(
            [["PW Calc", str("{:.0f}".format(chenresult[0]))],
             ["Well Prod Barrels", str("{:.0f}".format(chenresult[1]))],
             ],
            columns=['Type', 'Value'])
        dataknock.index += 1
        st.table(dataknock)
