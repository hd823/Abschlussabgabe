import json
import datetime as dt
import os

class Person:
    '''
    Beschreibt Objekte, die EKG-Tests, ein Bild, ein Alter, ein Geschlecht usw haben.
    Werden in JSON-Datei person_db.json gespeichert.
    '''
    @staticmethod
    def load_person_data(FILE_PATH = "data/person_db.json"):
        """
        Lädt die bestehenden Personendaten aus der JSON-Datei.
        Gibt eine leere Liste zurück, wenn die Datei nicht existiert.
        """
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


    @staticmethod
    def get_person_list(person_data : list) -> list[str]:
        """
        Funktion, die aus einer Liste alle Namen extrahiert und diese in eine neue Liste speichert
        Eingabeparameter: Liste mit Personendaten
        Ausgabeparameter: Liste mit Personennamen
        """
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring : str, FILE_PATH = "data/person_db.json") -> dict:
        """
        Findet Person nach Name und gibt Daten dieser Person als Dictionary aus
        Eingabeparameter: Name der gesuchten Person
        Ausgabeparamter: Dictionary der gesuchten Person
        """
        person_data = Person.load_person_data(FILE_PATH)

        # Kontrolle, dass suchstring den Eingabeanforderungen entspricht
        if not suchstring or ", " not in suchstring: 
            return None
        
        # Liste mit zwei Einträgen wird zurückgegeben, kann so auch direkt auf verschiedene Variablen gespeichert werden
        nachname, vorname = suchstring.split(", ") 

        for eintrag in person_data:
            if eintrag["lastname"] == nachname and eintrag["firstname"] == vorname:
                return eintrag
        return None
    
    def calc_age(self) -> int:
        """
        Berechnet das Alter eines Personenobjekts basierend auf dem Geburtsjahr
        Ausgabeparameter: Alter
        """
        birthday_year = int(self.date_of_birth)
        today = dt.date.today()
        age = today.year - birthday_year
        self.age = age
        return age
    
    def calc_max_hr(self) -> int:
        '''
        Berechnet die maximale Herzfrequenz eines Personenobjekts auf Grundlage des Alters und des Geschlechts
        Ausgabeparameter: maximale Herzfrequenz 
        '''
        if self.gender == "female":
            self.max_heart_rate = round(226 - self.age)
        else:
            self.max_heart_rate = round(220 - self.age)
        return self.max_heart_rate
    
    @staticmethod
    def load_by_id(person_id : int, FILE_PATH = "data/person_db.json") -> 'Person':
        '''
        Erstellt ein Personen-Objekt anhand der übergebenen ID und der Personendatenbank
        Eingabeparameter: ID
        Ausgabeparameter: Objekt der Klasse Person nach ID
        '''
        Person_aus_id = None

        person_data = Person.load_person_data(FILE_PATH)

        for person in person_data:
            if person_id == int(person["id"]):
                Person_aus_id = Person(person)
                break

        return Person_aus_id
    
    def __init__(self, person_dict : dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.name= f"{self.lastname}, {self.firstname}"
        self.picture_path = person_dict["picture_path"]
        self.gender = person_dict["gender"]
        self.id = person_dict["id"]

        self.ekg_tests = person_dict.get("ekg_tests", []) 
        self.ekg_tests_by_id = {str(ekg["id"]): ekg for ekg in self.ekg_tests}

        self.age = self.calc_age()
        self.max_hr = self.calc_max_hr()