import time
import streamlit as st
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd
from lib.chen_flow import chen_flow
from lib.hagedorn_brown_flow import HagedornBrownFlow
from lib.beggs_and_brill import flow_regime, liq_holdup, beggs_brill_flow

def app():
    if 'chen_result' not in st.session_state:
        st.session_state.chen_result = None
    if 'hagedorn_brown_result' not in st.session_state:
        st.session_state.hagedorn_brown_result = None
    if 'beggs_brill_result' not in st.session_state:
        st.session_state.beggs_brill_result = None


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
    button2 = st.button('Calculate Hagedorn & Brown')
    button2 = st.button('Calculate Beggs & Brill')

    if button1:
        with st.spinner('Processing...'):
            st.session_state.chen_result = chen_flow(IP, Pe, Psep, diam, L, depth)

    if button2:
        with st.spinner('Processing...'):
            st.session_state.hagedorn_brown_result = HagedornBrownFlow(IP, Pe, Psep, diam, L, depth, RGO)
            
    if button3:
        with st.spinner('Processing...'):
            st.session_state.beggs_brill_result = beggs_brill_flow(IP, Pe, Psep, diam, L, depth, RGO) 

    if st.session_state.chen_result:
        dataknock = pd.DataFrame(
            [["Wellhead Pressure (bara)", str("{:.0f}".format(st.session_state.chen_result[0]))],
             ["Well Production (Barrels/day)", str("{:.0f}".format(st.session_state.chen_result[1]))],
             ],
            columns=['Chen Flow', 'Value'])
        dataknock.index += 1
        st.table(dataknock)

    if st.session_state.hagedorn_brown_result:
        dataknock = pd.DataFrame(
            [["Wellhead Pressure (bara)", str("{:.0f}".format(st.session_state.hagedorn_brown_result[0]))],
             ["Well Production (Barrels/day)", str("{:.0f}".format(st.session_state.hagedorn_brown_result[1]))],
             ],
            columns=['Hagedorn & Brown Flow', 'Value'])
        dataknock.index += 1
        st.table(dataknock)

    if st.session_state.beggs_brill_result:
        dataknock = pd.DataFrame(
            [["Wellhead Pressure (bara)", str("{:.0f}".format(st.session_state.beggs_brill_result[0]))],
             ["Well Production (Barrels/day)", str("{:.0f}".format(st.session_state.beggs_brill_result[1]))],
             ],
            columns=['Beggs & Brill Flow', 'Value'])
        dataknock.index += 1
        st.table(dataknock)

if __name__ == "__main__":
    app()
