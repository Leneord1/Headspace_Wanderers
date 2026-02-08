import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme
import pandas as pd
import numpy as np
import plotly.express as px
import json
import time

#--------------------------------CONSTANTS-----------------------------------
# screens
LOGIN = 0
MENU = 1
OVERVIEW = 2

TEST = -1

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

def total_score():
    return "75"

def back():
    st.session_state.screen -= 1

#--------------------------------SESSION VALS--------------------------------

if "screen" not in st.session_state:
    st.session_state.screen = LOGIN

if "kits" not in st.session_state:
    st.session_state.kits = ["Lexus Monitor", "Porsche Monitor", "Truck Monitor"]

if "is_updated" not in st.session_state:
    st.session_state.is_updated = False

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
            st.button(name, on_click=device_display, args=(name, ))

elif st.session_state.screen == OVERVIEW:
    st.set_page_config(layout='wide')
    st.title("Overview")

    try:
        with open('overview.html', 'r', encoding='utf-8') as file:
            overview_html = file.read()
        with open('humidity.html', 'r', encoding='utf-8') as file:
            humidity_html = file.read()
        with open('temperature.html', 'r', encoding='utf-8') as file:
            temperature_html = file.read()
    except FileNotFoundError:
        st.error(f"Error: The file 'chart.html' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    theme = st_theme()

    with st.spinner("Wait for it...", show_time=True):
        time.sleep(1)

    text_color = "\"#FFFFFF\"" if theme['base'] == "dark" else "\"#000000\""

    val = total_score()
    overview_html = overview_html.replace("__VAL__", val)
    overview_html = overview_html.replace("__COL__", text_color)
    components.html(overview_html, height=550)

    data = pd.read_csv("data\data.csv")

    #-----------------Humidity Graph-----------------

    humidity_html = humidity_html.replace("__DATA__", data.to_json(orient='records'))
    humidity_html = humidity_html.replace("__COL__", text_color)

    components.html(humidity_html, height=550)

    #----------------Temperature Graph-----------------

    temperature_html = temperature_html.replace("__DATA__", data.to_json(orient='records'))
    temperature_html = temperature_html.replace("__COL__", text_color)

    components.html(temperature_html, height=550)

    st.button("<-", on_click=back)
