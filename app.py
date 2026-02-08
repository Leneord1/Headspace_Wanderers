import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme
import pandas as pd
import time
import csv_converter as cc

#--------------------------------CONSTANTS-----------------------------------

# screens
LOGIN = 0
MENU = 1
OVERVIEW = 2

# other
TEMP_THRESHOLD = 55
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

def device_display(kit):
    if kit[1]:
        st.session_state.screen = OVERVIEW
    else:
        st.warning("This kit isn't set up yet!")

def total_score():
    return "75"

def back():
    st.session_state.screen -= 1

#--------------------------------SESSION VALS--------------------------------

if "screen" not in st.session_state:
    st.session_state.screen = LOGIN

if "kits" not in st.session_state:
    st.session_state.kits = [["Engine Bay", True], 
                             ["Fuse Box", False], 
                             ["Passenger Fuse Box", False]]

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
        for i, kit in enumerate(st.session_state.kits):
            st.button(kit[0], on_click=device_display, args=(kit, ))

elif st.session_state.screen == OVERVIEW:
    st.set_page_config(layout='wide')
    st.title("Overview")

    try:
        with open('overview.html', 'r', encoding='utf-8') as file:
            hum_overview_html = file.read()
        with open('overview.html', 'r', encoding='utf-8') as file:
            temp_overview_html = file.read()
        with open('humidity.html', 'r', encoding='utf-8') as file:
            humidity_html = file.read()
        with open('temperature.html', 'r', encoding='utf-8') as file:
            temperature_html = file.read()
    except FileNotFoundError:
        st.error(f"Error: The file 'chart.html' was not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    theme = st_theme()

    cc.listen_to_port(port="COM3", baud=9600)

    progress_text = "Loading..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    text_color = "\"#FFFFFF\"" if theme['base'] == "dark" else "\"#000000\""

    data = pd.read_csv("data/data.csv")
    hum_count = (data['humidity_pct'] > HUM_THRESHOLD).sum()
    hum_sum = data['humidity_pct'].sum()

    temp_count = (data['temperature_c'] > TEMP_THRESHOLD).sum()
    temp_sum = data['temperature_c'].sum()

    hum_score = str((((hum_sum - hum_count) / hum_sum) * 100) // 1)
    temp_score = str((((temp_sum - temp_count) / temp_sum) * 100) // 1)

    hum_overview_html = hum_overview_html.replace("__VAL__", hum_score)
    temp_overview_html = temp_overview_html.replace("__VAL__", temp_score)

    hum_overview_html = hum_overview_html.replace("__COL__", text_color)
    temp_overview_html = temp_overview_html.replace("__COL__", text_color)

    hum_overview_html = hum_overview_html.replace("__TITLE__", "\"Humidity\"")
    temp_overview_html = temp_overview_html.replace("__TITLE__", "\"Temperature\"")

    left, right = st.columns(2)
    with left:
        components.html(hum_overview_html, height=550)
    with right:
        components.html(temp_overview_html, height=550)

    

    #-----------------Humidity Graph-----------------

    humidity_html = humidity_html.replace("__DATA__", data.to_json(orient='records'))
    humidity_html = humidity_html.replace("__COL__", text_color)

    components.html(humidity_html, height=550)

    #----------------Temperature Graph-----------------

    temperature_html = temperature_html.replace("__DATA__", data.to_json(orient='records'))
    temperature_html = temperature_html.replace("__COL__", text_color)

    components.html(temperature_html, height=550)

    st.button("<-", on_click=back)
