import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

#--------------------------------CONSTANTS-----------------------------------
# screens
LOGIN = 0
MENU = 1
OVERVIEW = 2
TEMP_HUM = 3
AIR_QUAL = 4
# other
LOW_TEMP_THRESHOLD = 20
HI_TEMP_THRESHOLD = 30
HUM_THRESHOLD = 60

#----------------------------------LOGIN------------------------------------
def check_password():

    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Password incorrect")
        return False
    else:
        return True

#----------------------------------CALLBACKS------------------------------------

def device_display(name):
    st.session_state.screen = OVERVIEW


#--------------------------------SESSION VALS--------------------------------

if "screen" not in st.session_state:
    st.session_state.screen = LOGIN

if "kits" not in st.session_state:
    st.session_state.kits = ["Lexus Monitor", "Porsche Monitor", "Truck Monitor"]

#---------------------------------SCREENS------------------------------------

if st.session_state.screen == LOGIN:
    st.set_page_config(layout='centered')
    st.title("Please enter your password")
    if check_password():
        st.session_state.screen = MENU
        st.rerun()

elif st.session_state.screen == MENU:
    st.set_page_config(layout='centered')
    st.title("Please select your device")
    with st.container(horizontal=True):
        for i, name in enumerate(st.session_state.kits):
            st.button(name, on_click=device_display, args=(name,))


elif st.session_state.screen == OVERVIEW:
    st.set_page_config(layout='wide')
    st.title("Overview")

    try:
        with open('overview.html', 'r', encoding='utf-8') as file:
            overview_html = file.read()
    except FileNotFoundError:
        st.error(f"Error: The file 'chart.html' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    val = '75'
    overview_html = overview_html.replace("__VAL__", val)
    components.html(overview_html, height=550)
    
    with st.container(horizontal=True):
        st.button = ("Temperature and Humidity")
        st.button = ("Air Quality")

elif st.session_state.screen == TEMP_HUM:
    st.set_page_config(layout='wide')  
    st.title("Dashboard")

    data = pd.read_csv("data\data.csv")

    #-----------------Humidity Display-----------------

    fig = px.line(data, x='timestamp', y='humidity_pct', title='Humidity')
    
    st.plotly_chart(fig)

    #-----------------Temperature Display-----------------

    fig = px.line(data, x='timestamp', y='temperature_c', title='Temperature')
    
    st.plotly_chart(fig)