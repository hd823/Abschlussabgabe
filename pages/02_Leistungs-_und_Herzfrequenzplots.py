# pages/Leistungs-_und_Herzfrequenzplots.py

import streamlit as st
import os
import sys

sys.path.append(os.path.abspath("./source"))

from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
import source.functions_Leistungskurve2 as functions_leistung2

FILE_PATH_HR = "data/activity.csv"

st.title("Leistungs- und Herzfrequenzplots")
st.markdown("---") 

st.markdown("## Herzfrequenz- und Leistungsdaten analysieren")
st.markdown("Hinweis: Es werden stets dieselben Beispieldaten analysiert. Die tatsächlichen Herzfrequenzwerte sind im `User_State` hinterlegt.")
st.markdown("Regler, Grafik und Tabelle dienen nur der Demonstration und basieren auf einem früheren Assignment.")

max_hr = st.number_input("Geben Sie Ihre maximale Herzfrequenz ein:", min_value=160, max_value=226, value=200)

col1, col2 = st.columns(2)
with col1:
    fig1 = plot_analysed_hr(analyse_heart_rate(FILE_PATH_HR, max_hr), max_hr)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("## Zeit in den Herzfrequenzzonen")
    st.plotly_chart(calculate_time_per_zone(analyse_heart_rate(FILE_PATH_HR, max_hr)), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Power Duration Curve")
    st.pyplot(functions_leistung2.plot_power_duration_curve(functions_leistung2.load_data_power()), use_container_width=True)

with col4:
    st.markdown("### Power Curve")
    st.pyplot(functions_leistung2.plot_power(functions_leistung2.load_data_power()), use_container_width=True)
