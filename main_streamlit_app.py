import sys
import os
sys.path.append(os.path.abspath("./source"))
import streamlit as st
from PIL import Image

from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
from source.ekg_class import EKG
from source.person_class import Person

# Layout
st.set_page_config(layout="wide")

# SIDEBAR – nur Auswahl
with st.sidebar:
    st.title("EKG Analyse App")
    FILE_PATH = "data/person_db.json"
    user_data = Person.load_person_data(FILE_PATH)
    name_list = Person.get_person_list(user_data)

    if "aktuelle_versuchsperson" not in st.session_state:
        st.session_state.aktuelle_versuchsperson = "None"

    st.markdown("## Versuchsperson")
    st.markdown("Wählen Sie eine Person aus der Liste aus:")
    st.session_state.aktuelle_versuchsperson = st.selectbox(
        'Versuchsperson',
        options=name_list,
        key="sbVersuchsperson"
    )

# Person laden
st.session_state.picture_path = "data/pictures/none.jpg"
if st.session_state.aktuelle_versuchsperson in name_list:
    person_data_dict = Person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
    if person_data_dict and "picture_path" in person_data_dict:
        st.session_state.picture_path = person_data_dict["picture_path"]
    session_state_person_obj = Person(person_data_dict)
else:
    st.warning("Bitte wählen Sie eine gültige Versuchsperson aus.")
    st.stop()

# SPALTENAUFTEILUNG
col1, col2 = st.columns([1, 2])

# LINKE SPALTE: Bild + Daten + Testauswahl
with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    if st.session_state.picture_path and os.path.exists(st.session_state.picture_path):
        with open(st.session_state.picture_path, "rb") as f:
            img = Image.open(f)
            st.image(img, width=200, caption=st.session_state.aktuelle_versuchsperson)
    else:
        # Fallback-Bild, wenn kein Bildpfad vorhanden oder gültig ist
        placeholder_path = "data/pictures/none.jpg"
        if os.path.exists(placeholder_path):
            with open(placeholder_path, "rb") as f:
                img = Image.open(f)
                st.image(img, width=200, caption=st.session_state.aktuelle_versuchsperson)
        else:
            st.warning("Kein Bild vorhanden und Platzhalterbild nicht gefunden.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("Versuchsperson-ID:", person_data_dict["id"])
    st.write("Alter:", Person.calc_age(session_state_person_obj), "Jahre")
    st.write("Maximale Herzfrequenz:", Person.calc_max_hr(session_state_person_obj), "bpm")

    st.markdown("### 📊 <b>EKG-Testdaten</b>", unsafe_allow_html=True)

    if len(session_state_person_obj.ekg_tests) > 0:
        personal_ekg_list = [f"{ekg['id']}, Datum: {ekg['date']}" for ekg in session_state_person_obj.ekg_tests]
        selected_ekg_display = st.selectbox('EKG-Test', options=personal_ekg_list, key="sbEKG")

        selected_ekg_id, selected_ekg_date_str = selected_ekg_display.split(", Datum: ")
        selected_ekg_id = int(selected_ekg_id)
        selected_ekg_date = selected_ekg_date_str

        SAMPLING_RATE_HZ = 500
        current_ekg_data = EKG.load_by_id(selected_ekg_id)

        if current_ekg_data:
            st.markdown(f"<b>Testdatum:</b> {selected_ekg_date}", unsafe_allow_html=True)
            st.markdown(f"<b>Testdauer:</b> {round(len(current_ekg_data.df) / (500*60))} Minuten", unsafe_allow_html=True)
    else:
        st.warning(f"😴 Für **{st.session_state.aktuelle_versuchsperson}** wurde kein EKG-Test gefunden. "
                   "Hier könnten Ihre EKG-Daten stehen.")

# RECHTE SPALTE: EKG-Analyse
with col2:
    if 'current_ekg_data' in locals() and current_ekg_data:
        st.subheader("EKG-Signalanalyse")

        total_data_points = len(current_ekg_data.df)
        max_gesamt_sekunden = total_data_points / SAMPLING_RATE_HZ
        min_gesamt_sekunden = 0.0

        fenster_groesse_sekunden = st.number_input(
            "Geplottete Länge des EKG-Tests in Sekunden:",
            min_value=10, max_value=300, value=60
        )
        st.session_state.fixed_window_size_s = fenster_groesse_sekunden

        st.markdown(f"Die aktuelle Fenstergröße beträgt: <b>{fenster_groesse_sekunden} Sekunden</b>.", unsafe_allow_html=True)
        st.markdown("Verwenden Sie den Schieberegler unten, um den Zeitabschnitt anzupassen.")

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
            st.warning(f"Die definierte Fenstergröße ({fenster_groesse_sekunden:.1f}s) ist gleich oder größer als die gesamte Testdauer ({max_gesamt_sekunden:.1f}s).")
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
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Tipp: Zum Einstellen links drücken und nach rechts ziehen.")

        col_hr1, col_hr2 = st.columns(2)
        with col_hr1:
            st.metric("Durchschnittliche Herzfrequenz (gesamt)", f"{current_ekg_data.estimate_hr():.2f} bpm")
        with col_hr2:
            avg_hr_window = current_ekg_data.estimate_hr(start_s=start_des_fensters_sekunden, end_s=ende_des_fensters_sekunden)
            st.metric("Durchschnittliche Herzfrequenz (aktuelles Fenster)", f"{avg_hr_window:.2f} bpm")