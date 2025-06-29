# pages/Fruehere_Assignments.py

# --- 1. Allgemeine Imports und Pfad-Anpassungen ---
import streamlit as st
import os
import sys

# Passe den Pfad an, je nachdem wo 'source' relativ zu 'pages' liegt.
# Wenn 'source' ein Geschwisterordner von 'pages' ist (z.B. beide direkt im Hauptverzeichnis),
# dann ist 'os.path.abspath("../source")' korrekt.
# Wenn 'source' ein Unterordner des Hauptverzeichnisses ist, und 'pages' auch ein Unterordner,
# dann könnte der Pfad zum Hauptverzeichnis und dann zu 'source' nötig sein.
# Der sicherste Weg ist oft, den Basispfad der App zu ermitteln und dann anzuhängen.
# Oder, wenn du die Haupt-App mit `streamlit run main_streamlit_app.py` startest,
# und `sys.path.append("./source")` in `main_streamlit_app.py` hast,
# dann sind die Module aus 'source' oft schon global verfügbar.
# Aber zur Sicherheit hier nochmal der explizite Pfad:
sys.path.append(os.path.abspath("./source")) # Angenommen, 'source' ist im Hauptverzeichnis.
# Oder: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))
# Dies geht einen Ordner hoch (von 'pages' zum Hauptverzeichnis) und dann in 'source'.

# Importiere NUR das, was auf dieser spezifischen Seite benötigt wird.
from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
import source.functions_Leistungskurve2 as functions_leistung2
from source.person_class import Person # Für den Zugriff auf das Person-Objekt im Session State

# --- 2. Spezifische Dateipfade für diese Seite ---
FILE_PATH_HR = "data/activity.csv" # Diese Datei wird nur hier benötigt

# --- 3. Titel und Überschriften der Seite ---
st.title("Frühere Assignments")
st.write("---") # Trennlinie zur besseren Übersicht

# --- 4. Widgets und Logik dieser Seite ---
st.write("### Wählen Sie aus, ob Assignment 3 angezeigt werden soll.")
# Jedes Widget auf einer Seite sollte einen eindeutigen Key haben,
# besonders wenn es auf mehreren Seiten (oder früher in Tabs) verwendet wurde.
show_assignment_3 = st.checkbox("Zeige Assignment 3", value=False, key="show_assignment_3_checkbox_page")

if show_assignment_3:
    st.write("## Herzfrequenz- und Leistungsdaten analysieren")
    st.write("Etwas fehlleitend, da immer dieselben Daten analysiert werden und die richtigen Herzfrequenzen im User_State gespeichert sind..")
    st.write("Der Regler, die Grafik und die Tabelle sind nur für die Demonstration der Funktionalität und Erfüllung eines früheren Assignments da.")
    
    # Hole die maximale Herzfrequenz aus dem Session State, wenn verfügbar
    max_hr_from_session = None
    if "session_state_person_obj" in st.session_state and st.session_state.session_state_person_obj is not None:
        try:
            max_hr_from_session = Person.calc_max_hr(st.session_state.session_state_person_obj)
        except Exception as e:
            # Fängt Fehler ab, falls das Objekt nicht vollständig geladen ist
            st.warning(f"Konnte maximale Herzfrequenz nicht aus Session State laden: {e}. Verwende Standardwert.")
            max_hr_from_session = 200 
    else:
        max_hr_from_session = 200 # Fallback, wenn kein Person-Objekt im Session State ist

    max_hr = st.number_input("Geben Sie Ihre maximale Herzfrequenz ein:", 
                             min_value=160, 
                             max_value=226, 
                             value=int(max_hr_from_session) if max_hr_from_session else 200,
                             key="max_hr_input")

    # Caching der Funktionen für diese Seite
    @st.cache_data
    def get_analysed_hr(file_path_hr, max_hr_val):
        return analyse_heart_rate(file_path_hr, max_hr_val)

    @st.cache_data
    def get_time_per_zone(analysed_hr_data, max_hr_val):
        return calculate_time_per_zone(analysed_hr_data, max_hr_val)

    @st.cache_data # cache_data für load_data_power, da es Daten lädt
    def get_power_data():
        return functions_leistung2.load_data_power()


    analysed_hr_data = get_analysed_hr(FILE_PATH_HR, max_hr)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = plot_analysed_hr(analysed_hr_data, max_hr)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.write("## Zeit in den Herzfrequenzzonen")
        st.plotly_chart(get_time_per_zone(analysed_hr_data, max_hr), use_container_width=True)

    power_data = get_power_data() # Lade Leistungsdaten einmal
    col3, col4 = st.columns(2)
    with col3:
        st.write("### Power Duration Curve")
        st.pyplot(functions_leistung2.plot_power_duration_curve(power_data), use_container_width=True)
    with col4:
        st.write("### Power Curve")
        st.pyplot(functions_leistung2.plot_power(power_data), use_container_width=True)