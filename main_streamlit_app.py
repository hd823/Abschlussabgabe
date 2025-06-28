import sys
import os
sys.path.append(os.path.abspath("./source"))
import streamlit as st
from PIL import Image

from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
from source.ekg_data import EKGdata
from source.person_class import Person
import source.functions_Leistungskurve2 as functions_leistung2


# Sicherstellen, dass auch vor der Nutzerauswahl schon ein Wert im SessionState ist
if "aktuelle_versuchsperson" not in st.session_state:
    st.session_state.aktuelle_versuchsperson = "None"

FILE_PATH = "data/person_db.json"
FILE_PATH_HR = "data/activity.csv"
user_data = Person.load_person_data(FILE_PATH)
name_list = Person.get_person_list(user_data)

tab1, tab2 = st.tabs(["EKG-App", "Frühere Assignments"])
with tab1:
    st.title("EKG App")

    # Eine Überschrift der zweiten Ebene
    st.write("## Versuchsperson auswählen")

    st.write("Bitte wählen Sie eine Versuchsperson aus der Liste aus.")

    # Eine Auswahlbox für die Versuchsperson
    st.session_state.aktuelle_versuchsperson = st.selectbox(
        'Versuchsperson',
        options =  name_list, key="sbVersuchsperson")

    st.write("Aktuelle Versuchsperson:")

    if st.session_state.aktuelle_versuchsperson in name_list:
        st.session_state.picture_path = Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]

    session_state_person_obj = Person(Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson))
    # sessions_state_person_dict = Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson), darf nicht weil Objektorientierung eine Anforderung ist


    col1, col2, col3 = st.columns([0.33, 2, 0.33])
    with col2:
        innercol1, innercol2 = st.columns([1, 1])
        with innercol1:
            image = Image.open(st.session_state.picture_path)
            st.image(image, caption=st.session_state.aktuelle_versuchsperson)

        with innercol2:
            st.write(st.session_state.aktuelle_versuchsperson)
            st.write("ID der Versuchsperson ist: ", Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["id"])
            st.write("Alter der Versuchsperson ist: ", Person.calc_age(session_state_person_obj))
            st.write("Maximale Herzfrequenz der Versuchsperson ist: ", Person.calc_max_hr(session_state_person_obj))


    st.write("## EKG-Daten der Versuchsperson")
    if len(session_state_person_obj.ekg_tests) > 1:
        personal_ekg_list = []
        for ekg in session_state_person_obj.ekg_tests:
           personal_ekg_list.append(f"{ekg["id"]}, Datum: {ekg["date"]}") 
        selected_ekg = st.selectbox('EKG-Test', options =  personal_ekg_list, key = "sbEKG")
        selected_ekg_id, selected_ekg_date = selected_ekg.split(", ")
    else:
        selected_ekg_id = session_state_person_obj.ekg_tests[0]["id"]
        selected_ekg_date = session_state_person_obj.ekg_tests[0]["date"]

    st.write(f"Erstelldatum des Tests: {selected_ekg_date} und die Gesamtdauer des Test beträgt {round(len(EKGdata.load_by_id(selected_ekg_id).df)/3600)} Minuten")
    current_egk_data = EKGdata.load_by_id(selected_ekg_id)
    fig = current_egk_data.plot_time_series()
    st.plotly_chart(fig)



with tab2:
    # Soll Assignemt 3 angezeigt werden?
    st.write("### Wählen Sie aus, ob Assignment 3 angezeigt werden soll.")
    show_assignment_3 = st.checkbox("Zeige Assignment 3", value=False)
    if show_assignment_3:
        # nicht mehr notwendig, da max_hr jetzt im SessionState gespeichert wird
        st.write("## Herzfrequenz- und Leistungsdaten analysieren")
        st.write("Etwas fehlleitend, da immer die selben Daten analysiert werden und die richtigen Herzfrequenzen im User_State gespeichert sind..")
        st.write("Der Regler, die Grafik und die Tabelle sind nur für die Demonstration der Funktionalität und Erfüllung eines früheren Assignments da.")
        # Nächste Zeile beschreibt den Regler zum manuellen Setzen der maximalen Herzfrequenz, was nicht mehr nötig ist, allerdings in einer vorherigen Abgabe wichtig war.
        max_hr = st.number_input("Geben Sie Ihre maximale Herzfrequenz ein:", min_value=160, max_value=226, value=200)

        col1, col2 = st.columns(2)
        with col1:
            fig1 = plot_analysed_hr(analyse_heart_rate(FILE_PATH_HR, max_hr), max_hr)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.write("## Zeit in den Herzfrequenzzonen")
            st.plotly_chart(calculate_time_per_zone(analyse_heart_rate(FILE_PATH_HR, max_hr)), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.write("### Power Duration Curve")
            st.pyplot(functions_leistung2.plot_power_duration_curve(functions_leistung2.load_data_power()), use_container_width=True)
        with col4:
            st.write("### Power Curve")
            st.pyplot(functions_leistung2.plot_power(functions_leistung2.load_data_power()), use_container_width=True)