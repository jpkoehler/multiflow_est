"""import time
import streamlit as st
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from lib.chen_flow import chen_flow
from lib.hagedorn_brown_flow import HagedornBrownFlow
from lib.beggs_and_brill import flow_regime, liq_holdup, beggs_brill_flow


def app():
    chen_result = []
    beggs_and_brill_result = []
    st.title('Multiphase Flow Estimation')
    st.header('Input Data')

    IP = st.number_input('Productivity Index []:', 1.0, 100.0, 28.0, step=0.1)
    Pe = st.number_input('Reservoir Pressure [Bara]:', 1.0, 1000.0, 120.0, step=0.1)
    RGO = st.number_input('Gas-Oil Ratio (GOR)[m³/m³]:', 1.0, 1000.0, 280.0, step=0.1)
    Psep = st.number_input('Separator Pressure [Bara]:', 0.0, 100.0,  10.0, step=0.1)
    diam = st.number_input('Flowline Diameter[inch]:', 0.0, 20.0,  8.0, step=0.1)
    L = st.number_input('Flowline Length[Meters]:', 0.0, 10000.0,  2000.0, step=0.1)
    depth = st.number_input('Reservoir Depth[Meters]:', 0.0, 10000.0,  1000.0, step=0.1)

    button1 = st.button('Calculate Chen')

    if st.session_state.get('button1') != True:
        st.session_state['button1'] = button1

    if (button1):
        with st.spinner('Processando...'):
            chen_result = chen_flow(IP, Pe, Psep, diam, L, depth)

             beggs_and_brill_result = beggs_brill_flow(IP, Pe, Psep, diam, L, depth, RGO) 

            

            dataknock = pd.DataFrame(
                [["Wellhead Pressure (bara)", str("{:.0f}".format(chen_result[0]))],
                 ["Well Production (Barrels/day)", str("{:.0f}".format(chen_result[1]))],
                 ],
                columns=['Chen Flow', 'Value'])
            dataknock.index += 1
            st.table(dataknock)

             dataknock = pd.DataFrame(
                [["Wellhead Pressure (bara)", str("{:.0f}".format(beggs_and_brill_result[0]))],
                 ["Well Prod (Barrels/day)", str(
                     "{:.0f}".format(beggs_and_brill_result[1]))],
                 ],
                columns=['Beggs and Brill', 'Value'])
            dataknock.index += 1
            st.table(dataknock) """

            """ dataknock = pd.DataFrame(
                [["PW Calc", str("{:.0f}".format(hagedorn_brow_result[0]))],
                 ["Well Prod Barrels", str(
                     "{:.0f}".format(hagedorn_brow_result[1]))],
                 ],
                columns=['Hagedorn Brown', 'Value'])
            dataknock.index += 1
            st.table(dataknock) 
            
    button2 = st.button('Calculate H&B')

    if st.session_state.get('button2') != True:
        st.session_state['button2'] = button1


    if (button2):
        with st.spinner('Processando...'):
            hagedorn_brow_result = HagedornBrownFlow(IP, Pe, Psep, diam, L, depth, RGO)

            dataknock = pd.DataFrame(  # <-- Essa linha estava um nível a mais de indentação
                [["Wellhead Pressure (bara)", str("{:.0f}".format(hagedorn_brow_result[0]))],
                 ["Well Production (Barrels/day)", str("{:.0f}".format(hagedorn_brow_result[1]))],
                 ],
                columns=['Hagedorn & Brown Flow', 'Value'])
            dataknock.index += 1
            st.table(dataknock)"""










            
            """beggs_and_brill_result = beggs_brill_flow(IP, Pe, Psep, diam, L, depth, RGO)

            dataknock = pd.DataFrame(
                [["Wellhead Pressure (bara)", str("{:.0f}".format(beggs_and_brill_result[0]))],
                 ["Well Prod (Barrels/day)", str(
                     "{:.0f}".format(beggs_and_brill_result[1]))],
                 ],
                columns=['Beggs and Brill', 'Value'])
            dataknock.index += 1
            st.table(dataknock) """

    "st.success('Sucesso!')"

import time
import streamlit as st
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from lib.chen_flow import chen_flow
from lib.hagedorn_brown_flow import HagedornBrownFlow

# Inicializa as variáveis na sessão se ainda não existirem
if 'chen_result' not in st.session_state:
    st.session_state.chen_result = None
if 'hagedorn_brown_result' not in st.session_state:
    st.session_state.hagedorn_brown_result = None

st.title('Multiphase Flow Estimation')
st.header('Input Data')

IP = st.number_input('Productivity Index []:', 1.0, 100.0, 28.0, step=0.1)
Pe = st.number_input('Reservoir Pressure [Bara]:', 1.0, 1000.0, 120.0, step=0.1)
RGO = st.number_input('Gas-Oil Ratio (GOR)[m³/m³]:', 1.0, 1000.0, 280.0, step=0.1)
Psep = st.number_input('Separator Pressure [Bara]:', 0.0, 100.0, 10.0, step=0.1)
diam = st.number_input('Flowline Diameter[inch]:', 0.0, 20.0, 8.0, step=0.1)
L = st.number_input('Flowline Length[Meters]:', 0.0, 10000.0, 2000.0, step=0.1)
depth = st.number_input('Reservoir Depth[Meters]:', 0.0, 10000.0, 1000.0, step=0.1)

button1 = st.button('Calculate Chen')
button2 = st.button('Calculate H&B')

if button1:
    with st.spinner('Processando...'):
        st.session_state.chen_result = chen_flow(IP, Pe, Psep, diam, L, depth)

if button2:
    with st.spinner('Processando...'):
        st.session_state.hagedorn_brown_result = HagedornBrownFlow(IP, Pe, Psep, diam, L, depth, RGO)

# Exibe a tabela do modelo Chen, se os dados existirem
if st.session_state.chen_result:
    dataknock = pd.DataFrame(
        [["Wellhead Pressure (bara)", str("{:.0f}".format(st.session_state.chen_result[0]))],
         ["Well Production (Barrels/day)", str("{:.0f}".format(st.session_state.chen_result[1]))],
         ],
        columns=['Chen Flow', 'Value'])
    dataknock.index += 1
    st.table(dataknock)

# Exibe a tabela do modelo Hagedorn & Brown, se os dados existirem
if st.session_state.hagedorn_brown_result:
    dataknock = pd.DataFrame(
        [["Wellhead Pressure (bara)", str("{:.0f}".format(st.session_state.hagedorn_brown_result[0]))],
         ["Well Production (Barrels/day)", str("{:.0f}".format(st.session_state.hagedorn_brown_result[1]))],
         ],
        columns=['Hagedorn & Brown Flow', 'Value'])
    dataknock.index += 1
    st.table(dataknock)



