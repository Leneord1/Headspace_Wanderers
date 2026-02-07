import streamlit as st
import json
import streamlit.components.v1 as components
from streamlit_theme import st_theme
import pandas as pd
import numpy as np
import plotly.express as px

#--------------------------------CONSTANTS-----------------------------------
# screens
MENU = 0
# other
TEMP_THRESHOLD = 0
HUM_THRESHOLD = 60

#--------------------------------SESSION VALS--------------------------------

if "screen" not in st.session_state:
    st.session_state.screen = 0

#---------------------------------SCREENS------------------------------------

if st.session_state.screen == MENU:
    st.set_page_config(layout='wide')
    st.title("Dashboard")

    data = pd.read_csv("data\data.csv")

    # Find where the line crosses the threshold and add to plot
    crossings = data[( (data['humidity_pct'] >= HUM_THRESHOLD) & (data['humidity_pct'].shift(1) < HUM_THRESHOLD) ) |
                ( (data['humidity_pct'] <= HUM_THRESHOLD) & (data['humidity_pct'].shift(1) > HUM_THRESHOLD) )]

    fig = px.line(data, x='timestamp', y='humidity_pct', title='Humidity')

    fig.add_hline(y=HUM_THRESHOLD, line_dash="dash", line_color="red")

    fig.add_scatter(x=crossings['timestamp'], y=crossings['humidity_pct'], 
                    mode='markers', marker=dict(color='red', size=10), 
                    name='Crossings')

    # plot
    
    st.plotly_chart(fig)