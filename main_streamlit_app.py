import streamlit as st
from PIL import Image
from source.functions_hr_plot import analyse_heart_rate, plot_analysed_hr, calculate_time_per_zone
import source.object_functions_person_data as obj_func_person
import source.ekg_data as ekgdata
from person_class import Person

# Sicherstellen, dass auch vor der Nutzerauswahl schon ein Wert im SessionState ist
if "aktuelle_versuchsperson" not in st.session_state:
    st.session_state.aktuelle_versuchsperson = "None"

# Sollen hier die statischen Funktionen der Klasse Person verwendet werden, oder die importierten Funktionen aus dem Modul object_functions_person_data?
FILE_PATH = "data/person_db.json"
FILE_PATH_HR = "data/activity.csv"
# user_data = obj_func_person.load_person_data(FILE_PATH)
# name_list = obj_func_person.get_person_list(user_data)
user_data = Person.load_person_data(FILE_PATH)
name_list = Person.get_person_list(user_data)

st.title("EKG App")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

st.write("Bitte wählen Sie eine Versuchsperson aus der Liste aus.")

# Eine Auswahlbox für die Versuchsperson
st.session_state.aktuelle_versuchsperson = st.selectbox(
    'Versuchsperson',
    options =  name_list, key="sbVersuchsperson")

st.write("Aktuelle Versuchsperson:", st.session_state.aktuelle_versuchsperson)

if st.session_state.aktuelle_versuchsperson in name_list:
    st.session_state.picture_path = obj_func_person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]


image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.aktuelle_versuchsperson)


st.write("Id der Versuchsperson ist: ", obj_func_person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["id"])
st.write("Alter der Versuchsperson ist: ", obj_func_person.calc_age(st.session_state.aktuelle_versuchsperson))
st.write("Maximale Herzfrequenz der Versuchsperson ist: ", obj_func_person.calc_max_hr(st.session_state.aktuelle_versuchsperson))

# Soll Assignemt 3 angezeigt werden?
st.write("### Wählen Sie aus, ob Assignment 3 angezeigt werden soll.")
show_assignment_3 = st.checkbox("Zeige Assignment 3", value=False)
if show_assignment_3:
    # nicht mehr notwendig, da max_hr jetzt im SessionState gespeichert wird
    st.write("## Herzfrequenzdaten analysieren")
    st.write("Etwas fehlleitend, da immer die selben Daten analysiert werden und die richtigen Herzfrequenzen im User_State gespeichert sind..")
    st.write("Der Regler, die Grafik und die Tabelle sind nur für die Demonstration der Funktionalität und Erfüllung eines früheren Assignments da.")
    # Nächste Zeile beschreibt den Regler zum manuellen Setzen der maximalen Herzfrequenz, was nicht mehr nötig ist, allerdings in einer vorherigen Abgabe wichtig war.
    max_hr = st.number_input("Geben Sie Ihre maximale Herzfrequenz ein:", min_value=160, max_value=226, value=200)
    fig1 = plot_analysed_hr(analyse_heart_rate(FILE_PATH_HR, max_hr), max_hr)
    st.plotly_chart(fig1)

    st.write("## Zeit in den Herzfrequenzzonen")
    st.plotly_chart(calculate_time_per_zone(analyse_heart_rate(FILE_PATH_HR, max_hr)))

st.write("## EKG-Daten der Versuchsperson")

current_egk_data = ekgdata.EKGdata(obj_func_person.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["ekg_tests"][0])
fig = current_egk_data.plot_time_series()
st.plotly_chart(fig)