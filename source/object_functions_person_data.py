#%% Import
import sys
import os
sys.path.append(os.path.abspath(".."))  # Passe ggf. den Pfad an

import json
import pandas as pd
import datetime as dt
from person_class import Person

# %%
# Opening JSON file
def load_person_data(FILE_PATH="data/person_db.json"):
    """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
    file = open(FILE_PATH)
    person_data = json.load(file)
    return person_data

# %%

def get_person_list(person_data):
    """A Function that takes the Persons-Dictionary and returns a List auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names

# %% Test
#get_person_list(load_person_data())


# %%

def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""
    
    person_data = load_person_data()
    #print(suchstring)
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        print(eintrag)
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print()

            return eintrag
    else:
        return {}

# %%
def calc_age(suchstring):
    birth_year = int(find_person_data_by_name(suchstring)["date_of_birth"])
    today = dt.date.today()
    age = today.year - birth_year
    return age


# %%
def calc_max_hr(suchstring):
    age = calc_age(suchstring)
    gender = find_person_data_by_name(suchstring)["gender"]
    if gender == "male":
        max_heart_rate = 220 - age *0.9
    else:
        max_heart_rate = 220 - age
    return round(max_heart_rate)

# %%
def load_by_id(person_id):
    '''Erstellt eine Personen-Object anhand der übergebenen ID und der Personendatenbank'''
    Person_aus_id = None

    person_data = load_person_data()
    for person in person_data:
        if int(person_id) == int(person["id"]):
            Person_aus_id = Person(person)
            break

    return Person_aus_id

# %% Test
#current_person = find_person_data_by_name("Statham, Jason")
#current_person
#current_picture_path = current_person["picture_path"]
#current_picture_path
# %%
if __name__ == "__main__":
    person1 = load_by_id("1")
    print(person1.firstname, person1.lastname)
    print(person1.picture_path)
    
# %%
