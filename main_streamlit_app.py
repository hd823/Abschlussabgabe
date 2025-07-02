import sys
import os
sys.path.append(os.path.abspath("./source"))
import streamlit as st
from PIL import Image

from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
from source.ekg_data import EKGdata
from source.person_class import Person


if "aktuelle_versuchsperson" not in st.session_state:
    st.session_state.aktuelle_versuchsperson = "None"

FILE_PATH = "data/person_db.json"
FILE_PATH_HR = "data/activity.csv"
user_data = Person.load_person_data(FILE_PATH)
name_list = Person.get_person_list(user_data)


st.title("EKG App")

st.markdown("## Versuchsperson auswählen")

st.markdown("Bitte wählen Sie eine Versuchsperson aus der Liste aus.")

st.session_state.aktuelle_versuchsperson = st.selectbox(
    'Versuchsperson',
    options =  name_list, key="sbVersuchsperson")

st.markdown("Aktuelle Versuchsperson:")

st.session_state.picture_path = "data/pictures/placeholder.jpg"
if st.session_state.aktuelle_versuchsperson in name_list:
    person_data_dict = Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
    if person_data_dict and "picture_path" in person_data_dict:
        st.session_state.picture_path = person_data_dict["picture_path"]
    session_state_person_obj = Person(person_data_dict)
else:
    st.warning("Bitte wählen Sie eine gültige Versuchsperson aus.")
    st.stop()

col1, col2, col3 = st.columns([0.33, 2, 0.33])
with col2:
    innercol1, innercol2 = st.columns([1, 1])
    with innercol1:
        image = Image.open(st.session_state.picture_path)
        st.image(image, caption=st.session_state.aktuelle_versuchsperson)

    with innercol2:
        st.markdown(st.session_state.aktuelle_versuchsperson)
        if 'person_data_dict' in locals() and person_data_dict:
            st.write("ID der Versuchsperson ist: ", person_data_dict["id"])
            st.write("Alter der Versuchsperson ist: ", Person.calc_age(session_state_person_obj))
            st.write("Maximale Herzfrequenz der Versuchsperson ist: ", Person.calc_max_hr(session_state_person_obj))


st.markdown("## EKG-Daten der Versuchsperson")

selected_ekg_id = None
selected_ekg_date = None

if len(session_state_person_obj.ekg_tests) > 0:
    personal_ekg_list = []
    for ekg in session_state_person_obj.ekg_tests:
        personal_ekg_list.append(f"{ekg["id"]}, Datum: {ekg["date"]}")
    selected_ekg_display = st.selectbox('EKG-Test', options = personal_ekg_list, key = "sbEKG")

    selected_ekg_id, selected_ekg_date_str = selected_ekg_display.split(", Datum: ")
    selected_ekg_id = int(selected_ekg_id)
    selected_ekg_date = selected_ekg_date_str

    SAMPLING_RATE_HZ = 500
    current_ekg_data = EKGdata.load_by_id(selected_ekg_id)

    if current_ekg_data:
        st.markdown(f"Erstelldatum des Tests: {selected_ekg_date} und die Gesamtdauer des Tests beträgt {round(len(current_ekg_data.df) / (500*60))} Minuten")

        st.subheader("EKG-Signal Ansichtsfenster")
        
        total_data_points = len(current_ekg_data.df)
        max_gesamt_sekunden = total_data_points / SAMPLING_RATE_HZ
        min_gesamt_sekunden = 0.0
        # Setzt Fenstergröße
        fenster_groesse_sekunden = st.number_input("Geplottete Länge des EKG-Tests in Sekunden:", min_value= 10, max_value=300, value=60)

        st.session_state.fixed_window_size_s = fenster_groesse_sekunden
        st.markdown(f"Die Fenstergröße beträgt {st.session_state.fixed_window_size_s} Sekunden.")
        st.markdown(f"Sobald am Schieberegler der Zeitausschnitt geändert wird, wird auch die Fenstergröße angepasst.")

        if 'current_window_start_s' not in st.session_state or \
           'current_window_end_s' not in st.session_state or \
           st.session_state.get('last_ekg_id_for_slider') != selected_ekg_id:
            st.session_state.current_window_start_s = min_gesamt_sekunden
            st.session_state.current_window_end_s = min_gesamt_sekunden + fenster_groesse_sekunden
            if st.session_state.current_window_end_s > max_gesamt_sekunden:
                st.session_state.current_window_end_s = max_gesamt_sekunden
                st.session_state.current_window_start_s = max_gesamt_sekunden - fenster_groesse_sekunden
                if st.session_state.current_window_start_s < min_gesamt_sekunden:
                     st.session_state.current_window_start_s = min_gesamt_sekunden
            st.session_state.last_ekg_id_for_slider = selected_ekg_id

        def enforce_fixed_window_range():
            slider_start, slider_end = st.session_state.slider_window_range

            fixed_width = st.session_state.fixed_window_size_s
            max_total_s = max_gesamt_sekunden
            min_total_s = min_gesamt_sekunden

            current_slider_width = slider_end - slider_start

            if abs(current_slider_width - fixed_width) > 0.001:
                if slider_end > max_total_s:
                    new_end = max_total_s
                    new_start = max(min_total_s, new_end - fixed_width) 
                elif slider_start < min_total_s:
                    new_start = min_total_s
                    new_end = min(max_total_s, new_start + fixed_width) 
                elif abs(slider_end - (st.session_state.current_window_start_s + fixed_width)) > abs(slider_start - st.session_state.current_window_start_s):
                    new_end = slider_end
                    new_start = new_end - fixed_width
                    if new_start < min_total_s:
                        new_start = min_total_s
                        new_end = new_start + fixed_width
                else:
                    new_start = slider_start
                    new_end = new_start + fixed_width
                    if new_end > max_total_s:
                        new_end = max_total_s
                        new_start = new_end - fixed_width

                st.session_state.current_window_start_s = new_start
                st.session_state.current_window_end_s = new_end
            else:
                st.session_state.current_window_start_s = slider_start
                st.session_state.current_window_end_s = slider_end

        if fenster_groesse_sekunden >= max_gesamt_sekunden:
            st.warning(f"Die definierte Fenstergröße ({fenster_groesse_sekunden:.1f}s) ist gleich oder größer als die gesamte Testdauer ({max_gesamt_sekunden:.1f}s). Das Fenster wird die gesamte Dauer umfassen.")
            st.session_state.current_window_start_s = min_gesamt_sekunden
            st.session_state.current_window_end_s = max_gesamt_sekunden
            start_des_fensters_sekunden = min_gesamt_sekunden
            ende_des_fensters_sekunden = max_gesamt_sekunden

            st.slider(
                "Ansichtsfenster (Gesamtdauer):",
                min_value=min_gesamt_sekunden,
                max_value=max_gesamt_sekunden,
                value=(min_gesamt_sekunden, max_gesamt_sekunden),
                step=0.1,
                format="%.1f s",
                disabled=True
            )
        else:
            st.slider(
                "Wählen Sie das Ansichtsfenster (in Sekunden):",
                min_value=min_gesamt_sekunden,
                max_value=max_gesamt_sekunden,
                value=(st.session_state.current_window_start_s, st.session_state.current_window_end_s),
                step=0.1,
                format="%.1f s",
                key="slider_window_range",
                on_change=enforce_fixed_window_range
            )
            start_des_fensters_sekunden = st.session_state.current_window_start_s
            ende_des_fensters_sekunden = st.session_state.current_window_end_s

        fig = current_ekg_data.plot_time_series(start_s=start_des_fensters_sekunden, end_s=ende_des_fensters_sekunden)
        st.plotly_chart(fig)

    else:
        st.error("Fehler beim Laden der EKG-Daten für den ausgewählten Test.")
    st.markdown("Zum Näheren Auswählen des geplotteten Zeitbereichs kann mit Doppelklick und Ziehen in horizontale Richtung (relativ genau) ein Bereich ausgewählt werden.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("Durchschnitts-Herzfrequenz über gesamten EKG-Test:")
        if current_ekg_data:
            average_hr = current_ekg_data.estimate_hr()
            st.markdown(f"{average_hr:.2f} bpm")
        else:
            st.warning("Keine EKG-Daten verfügbar, um die Herzfrequenz zu schätzen.")
    with col2:
        st.markdown("Durchschnitts-Herzfrequenz über ausgewählten EKG-Test-Zeitraum:")
        if current_ekg_data:
            average_hr = current_ekg_data.estimate_hr(start_s=start_des_fensters_sekunden, end_s=ende_des_fensters_sekunden)
            st.markdown(f"{average_hr:.2f} bpm")
else:
    st.info("Für die ausgewählte Person sind keine EKG-Tests verfügbar.")
