import streamlit as st
import json
import os

from source.ekg_data import EKGdata
from source.person_class import Person

# Pfad zur JSON-Datenbank
FILE_PATH = "data/person_db.json"

tab1, tab2 = st.tabs(["Person hinzufügen", "Bestehende Personen bearbeiten"])

with tab1:
    st.title("Neue Person hinzufügen")

    # Formular zur Eingabe neuer Personendaten
    with st.form("person_form"):
        firstname = st.text_input("Vorname")
        lastname = st.text_input("Nachname")
        date_of_birth = st.number_input("Geburtsjahr", min_value=1945, max_value=2025, value= 1990, step=1)
        gender = st.selectbox("Geschlecht", ["male", "female"])
        picture_path = st.text_input("Pfad zum Bild (z. B. data/pictures/name.jpg)")
        
        # Eingabe für ersten EKG-Test
        ekg_id = st.number_input("EKG-Test ID", min_value=1, step=1)
        ekg_date = st.text_input("Datum des EKG-Tests (z. B. 10.2.2023)")
        ekg_result_link = st.text_input("Pfad zur EKG-Datei (z. B. data/ekg_data/test.txt)")

        submitted = st.form_submit_button("Person hinzufügen")

        if submitted:
            def speichere_personen_daten(data):
                """
                Speichert die übergebenen Personendaten in der JSON-Datei.
                """
                with open(FILE_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

            daten = lade_personen_daten()

            # Neue eindeutige ID berechnen
            new_id = max([p["id"] for p in daten], default=0) + 1

            neue_person = {
                "id": new_id,
                "date_of_birth": int(date_of_birth),
                "firstname": firstname,
                "lastname": lastname,
                "picture_path": picture_path,
                "gender": gender,
                "ekg_tests": [{
                    "id": int(ekg_id),
                    "date": ekg_date,
                    "result_link": ekg_result_link
                }]
            }

            daten.append(neue_person)
            speichere_personen_daten(daten)

            st.success(f"{firstname} {lastname} wurde erfolgreich hinzugefügt!")

with tab2:
    st.title("Bestehende Personen bearbeiten")