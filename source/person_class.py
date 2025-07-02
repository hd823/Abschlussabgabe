import json
import datetime as dt
import os

class Person:
    '''
    Klasse zur Verwaltung von Personendaten und EKG-Tests.
    Stellt Methoden zum Laden, Speichern und Auswerten bereit.
    '''

    @staticmethod
    def load_person_data(FILE_PATH = "data/person_db.json"):
        """
        Lädt die bestehenden Personendaten aus der JSON-Datei.
        Gibt eine leere Liste zurück, wenn die Datei nicht existiert.
        Eingabeparameter: FILE_PATH (str)
        Ausgabeparameter: Liste mit Personendaten
        """
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @staticmethod
    def get_person_list(person_data : list) -> list[str]:
        """
        Extrahiert die Namen aus der Personenliste.
        Eingabeparameter: Liste mit Personendaten
        Ausgabeparameter: Liste mit Personennamen (str)
        """
        list_of_names = []
        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names

    @staticmethod
    def find_person_data_by_name(suchstring : str, FILE_PATH = "data/person_db.json") -> dict:
        """
        Findet Person nach Name und gibt deren Daten als Dictionary zurück.
        Eingabeparameter: suchstring (str) – Name im Format 'Nachname, Vorname'
        Ausgabeparameter: Dictionary mit Personendaten oder None
        """
        person_data = Person.load_person_data(FILE_PATH)

        if not suchstring or ", " not in suchstring: 
            return None
        
        nachname, vorname = suchstring.split(", ") 

        for eintrag in person_data:
            if eintrag["lastname"] == nachname and eintrag["firstname"] == vorname:
                return eintrag
        return None

    @staticmethod
    def safe_person_data(data, FILE_PATH = "data/person_db.json"):
        """
        Speichert die übergebenen Personendaten in der JSON-Datei.
        Eingabeparameter: data (Liste oder Dict)
        Ausgabeparameter: keiner
        """
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def calc_age(self) -> int:
        """
        Berechnet das Alter eines Personenobjekts basierend auf dem Geburtsjahr.
        Eingabeparameter: keine
        Ausgabeparameter: Alter (int)
        """
        birthday_year = int(self.date_of_birth)
        today = dt.date.today()
        age = today.year - birthday_year
        self.age = age
        return age

    def calc_max_hr(self) -> int:
        '''
        Berechnet die maximale Herzfrequenz basierend auf Alter und Geschlecht.
        Eingabeparameter: keine
        Ausgabeparameter: maximale Herzfrequenz (int)
        '''
        if self.gender == "female":
            self.max_heart_rate = round(226 - self.age)
        else:
            self.max_heart_rate = round(220 - self.age)
        return self.max_heart_rate

    @staticmethod
    def load_by_id(person_id : int, FILE_PATH = "data/person_db.json") -> 'Person':
        '''
        Lädt ein Personenobjekt anhand einer gegebenen ID.
        Eingabeparameter: person_id (int)
        Ausgabeparameter: Instanz der Klasse Person oder None
        '''
        Person_aus_id = None
        person_data = Person.load_person_data(FILE_PATH)

        for person in person_data:
            if person_id == int(person["id"]):
                Person_aus_id = Person(person)
                break

        return Person_aus_id

    def __init__(self, person_dict : dict) -> None:
        """
        Initialisiert ein Personenobjekt mit Informationen aus einem Dictionary.
        Eingabeparameter: person_dict (dict)
        Ausgabeparameter: keiner
        """
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.name= f"{self.lastname}, {self.firstname}"
        if "picture_path" not in person_dict:
            self.picture_path = "data/pictures/none.jpg"
        else:
            self.picture_path = person_dict["picture_path"]
        self.gender = person_dict["gender"]
        self.id = person_dict["id"]

        self.ekg_tests = person_dict.get("ekg_tests", []) 
        self.ekg_tests_by_id = {str(ekg["id"]): ekg for ekg in self.ekg_tests}

        self.age = self.calc_age()
        self.max_hr = self.calc_max_hr()
