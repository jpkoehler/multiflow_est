import time
import streamlit as st
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from libs.chen_flow import chen_flow
from libs.beggs_and_brill import beggs_brill_flow


def app():
    st.title('Multiphase Flow Estimation')
    st.header('Dados de Entrada')

    IP = st.number_input('IP:', 1, 100, 10)
    Pe = st.number_input('Pe:', 1, 1000, 300)
    RGO = st.number_input('RGO:', 1, 1000, 10)
    Psep = st.number_input('Psep:', 0, 100, 65)
    diam = st.number_input('Diameter:', 0, 20, 8)
    L = st.number_input('Length:', 0, 10000, 6)
    depth = st.number_input('Depth:', 0, 10000, 3)

    button1 = st.button('Calculate')

    if st.session_state.get('button1') != True:
        st.session_state['button1'] = button1

    if (button1):
        with st.spinner('Processando...'):
            chen_result = chen_flow(IP, Pe, Psep, diam, L, depth)
            beggs_and_brill_result = beggs_brill_flow(
                IP, Pe, Psep, diam, L, depth, RGO)
            time.sleep(2)
        st.success('Sucesso!')

    dataknock = pd.DataFrame(
        [["PW Calc", str("{:.0f}".format(chen_result[0]))],
         ["Well Prod Barrels", str("{:.0f}".format(chen_result[1]))],
         ],
        columns=['Chen Flow', 'Value'])
    dataknock.index += 1
    st.table(dataknock)

    dataknock = pd.DataFrame(
        [["PW Calc", str("{:.0f}".format(beggs_and_brill_result[0]))],
         ["Well Prod Barrels", str(
             "{:.0f}".format(beggs_and_brill_result[1]))],
         ],
        columns=['Beggs and Brill', 'Value'])
    dataknock.index += 1
    st.table(dataknock)
