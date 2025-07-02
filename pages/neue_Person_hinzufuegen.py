import streamlit as st
import datetime as dt
import os

from source.ekg_data import EKGdata
from source.person_class import Person

# Pfad zur JSON-Datenbank
FILE_PATH = "data/person_db.json"
ekg_folder = "data"

tab1, tab2 = st.tabs(["Person hinzufügen", "Bestehende Personen bearbeiten"])

with tab1:
    st.title("Neue Person hinzufügen")
    st.subheader("Geben Sie die Daten der neuen Person ein")

    # Formular zur Eingabe neuer Personendaten
    with st.form("person_form"):
        st.markdown("Pflichtfelder sind mit * markiert")
        new_person_firstname = st.text_input("Vorname*", key="new_person_firstname").upper
        new_person_lastname = st.text_input("Nachname*", key="new_person_lastname").upper()
        new_person_date_of_birth = st.date_input("Geburtsdatum*", value=dt.date(2000, 1, 1), key="new_person_birthdate").year
        new_person_gender = st.selectbox("Geschlecht*", ["female", "male"], key="new_person_gender")

        st.markdown("Optionale EKG-Daten hinzufügen")
        new_person_picture = st.file_uploader("Profilbild hochladen", type=["jpg", "jpeg", "png"], key="new_person_picture_file")
        new_person_ekg_file = st.file_uploader("Ruhe-EKG-Datei hochladen", type=["txt", "csv"], key="new_person_ekg_file")
        new_person_ftp_file = st.file_uploader("FTP-Test-Datei hochladen", type=["txt", "csv"], key="new_person_ftp_file")
        cols = st.columns(3)
        with cols[1]:
            submitted = st.form_submit_button("Person hinzufügen")

    if submitted:
        if not new_person_firstname or not new_person_lastname or not new_person_date_of_birth or not new_person_gender:
            st.error("Alle Pflichtfelder müssen ausgefüllt werden!")
            st.stop()
        else:
            current_person_list = Person.load_person_data()
            if not current_person_list:
                st.error("Die Personendatenbank ist leer. Bitte fügen Sie zuerst eine Person hinzu.")
                st.stop()
            else:
                exists = any(p["firstname"].strip().lower() == new_person_firstname.strip().lower() and p["lastname"].strip().lower() == new_person_lastname.strip().lower() for p in current_person_list)
                
                if submitted:
                    if not new_person_firstname or not new_person_lastname or not new_person_date_of_birth or not new_person_gender:
                        st.error("Alle Pflichtfelder müssen ausgefüllt werden!")
                        st.stop()
                    else:
                        current_person_list = Person.load_person_data()
                        exists = any(
                            p["firstname"].strip().lower() == new_person_firstname.strip().lower() and
                            p["lastname"].strip().lower() == new_person_lastname.strip().lower()
                            for p in current_person_list
                        )
                        if exists:
                            st.error(f"Die Person {new_person_firstname} {new_person_lastname} existiert bereits in der Datenbank.")
                            st.stop()

                        new_id = max([p["id"] for p in current_person_list], default=0) + 1
                        os.makedirs("data/pictures", exist_ok=True)
                        os.makedirs("data/ekg_files", exist_ok=True)
                        os.makedirs("data/ftp_tests", exist_ok=True)

                        # Profilbild speichern
                        new_person_picture_path = ""
                        if new_person_picture:
                            new_person_picture_path = f"data/pictures/{new_id}_{new_person_picture.name}"
                            with open(new_person_picture_path, "wb") as f:
                                f.write(new_person_picture.getbuffer())

                        # EKG-Tests vorbereiten
                        ekg_tests = []
                        all_ekg_ids = [ekg["id"] for person in current_person_list for ekg in person.get("ekg_tests", [])]
                        next_ekg_id = max(all_ekg_ids, default=0) + 1

                        if new_person_ekg_file:
                            ekg_file_path = f"data/ekg_files/{new_id}_{new_person_ekg_file.name}"
                            with open(ekg_file_path, "wb") as f:
                                f.write(new_person_ekg_file.getbuffer())

                            ekg_tests.append({
                                "id": next_ekg_id,
                                "date": dt.date.today().isoformat(),
                                "result_link": ekg_file_path
                            })
                            next_ekg_id += 1

                        if new_person_ftp_file:
                            ftp_file_path = f"data/ftp_tests/{new_id}_{new_person_ftp_file.name}"
                            with open(ftp_file_path, "wb") as f:
                                f.write(new_person_ftp_file.getbuffer())

                            ekg_tests.append({
                                "id": next_ekg_id,
                                "date": dt.date.today().isoformat(),
                                "result_link": ftp_file_path
                            })

                        neue_person = {
                            "id": new_id,
                            "firstname": new_person_firstname.strip().upper(),
                            "lastname": new_person_lastname.strip().upper(),
                            "date_of_birth": int(new_person_date_of_birth),
                            "picture_path": new_person_picture_path,
                            "gender": new_person_gender,
                            "ekg_tests": ekg_tests
                        }

                        current_person_list.append(neue_person)
                        Person.safe_person_data(current_person_list)
                        st.success(f"{new_person_firstname} {new_person_lastname} wurde erfolgreich hinzugefügt!")









                # if exists:
                #     st.error(f"Die Person {new_person_firstname} {new_person_lastname} existiert bereits in der Datenbank.")
                #     st.stop()
                # else:
                #     new_id = max([p["id"] for p in current_person_list], default=0) + 1

                #     new_person_picture_path = ""
                #     new_person_ekg_file_path = ""
                #     new_person_ftg_file_path = ""

                #     os.makedirs("data/pictures", exist_ok=True)
                #     os.makedirs("data/ekg_files", exist_ok=True)

                #     if new_person_picture:
                #         picture_path = f"data/pictures/{new_id}_{new_person_picture_path.name}"
                #         with open(picture_path, "wb") as f:
                #             f.write(new_person_picture.getbuffer())
                            
                #     if new_person_ekg_file:
                #         ekg_file_path = f"data/ruhe_ekg_{new_id}_{new_person_ekg_file.name}"
                #         with open(ekg_file_path, "wb") as f:
                #             f.write(new_person_ekg_file.getbuffer())
                    
                #     if new_person_ftp_file:
                #         ftg_file_path = f"data/ftp_tests/{new_id}_{new_person_ftp_file.name}"
                #         with open(ftg_file_path, "wb") as f:
                #             f.write(new_person_ftp_file.getbuffer())


                #     ekg_tests = []
                #     os.makedirs(ekg_folder, exist_ok=True)

                #     # Lade bestehende EKG-IDs aus der Datenbank, um fortlaufende IDs zu erzeugen
                #     all_ekg_ids = [ekg["id"] for person in current_person_list for ekg in person.get("ekg_tests", [])]
                #     next_ekg_id = max(all_ekg_ids, default=0) + 1

                #     # Falls du mehrere EKGs zulassen willst
                #     uploaded_ekg_files = [new_person_ekg_file] if new_person_ekg_file else []

                #     for ekg_file in uploaded_ekg_files:
                #         if ekg_file:
                #             file_name = f"{new_id}_{ekg_file.name}"
                #             save_path = os.path.join(ekg_folder, file_name)
                #             with open(save_path, "wb") as f:
                #                 f.write(ekg_file.getbuffer())

                #             ekg_tests.append({
                #                 "id": next_ekg_id,
                #                 "date": dt.date.today().isoformat(),  # Oder beliebiges Datum
                #                 "result_link": save_path
                #             })
                #             next_ekg_id += 1


                #     neue_person = {
                #         "id": new_id,
                #         "firstname": new_person_firstname.strip(),
                #         "lastname": new_person_lastname.strip(),
                #         "date_of_birth": int(new_person_date_of_birth),
                #         "picture_path": new_person_picture_path,
                #         "gender": new_person_gender,
                #         for test in 
                #             "ekg_tests": [{
                #                 "id": int(ekg_id),
                #                 "date": ekg_date,
                #                 "result_link": ekg_result_link
                #             }]
                #     }

                #     current_person_list.append(neue_person)
                #     Person.safe_person_data(current_person_list)

                #     st.success(f"{new_person_firstname} {new_person_lastname} wurde erfolgreich hinzugefügt!")

with tab2:
    st.title("Bestehende Personen bearbeiten")