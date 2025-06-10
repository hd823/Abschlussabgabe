# %%
import sys
import os
sys.path.append(os.path.abspath(".."))  # Passe ggf. den Pfad an

# %%
import json
import pandas as pd
import plotly.express as px
import source.object_functions_person_data as obj_func_person
from person_class import Person
from source.find_peaks_EKG import find_peaks

# %%
# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])


    def plot_time_series(self):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        peaks = find_peaks(self.df.head(2000))
        peak_df = self.df.head(2000).iloc[peaks]

        fig.add_scatter(
            x= peak_df["Zeit in ms"], 
            y=peak_df["Messwerte in mV"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
        )
        return fig

    def find_peaks(self):
        """
        Funktion, die die Peaks in der EKG-Datenreihe findet und sie in der DataFrame speichert.
        """
        # Hier wird angenommen, dass self.df bereits eine DataFrame mit den EKG-Daten ist
        self.df["Peaks"] = find_peaks(self.df)
        return self.df
    
    def estimate_hr(self):
        peak_indices= find_peaks(self.df)
        
        hr_series = [None] * len(self.df)  # Leere Liste für Spalte
        
        delta_time_ms = self.df.loc[idx2, "Zeit in ms"] - self.df.loc[idx1, "Zeit in ms"]
        delta_time_sec = delta_time_ms / 1000.0

        for i in range(1, len(peak_indices)):
            idx1 = peak_indices[i - 1]
            idx2 = peak_indices[i]

            delta_time_sec = idx2- idx1
            hr = 60 / delta_time_sec  # beats per minute

            hr_series[idx2] = hr

        self.df["Estimated HR"] = hr_series
        return hr_series


def load_by_id(ekg_id):
    ekg_by_id = None

    person_data = obj_func_person.load_person_data()
    for person in person_data:
        for ekg_test in person["ekg_tests"]:
            if int(ekg_id) == int(ekg_test["id"]):
                ekg_by_id = EKGdata(ekg_test)  # <-- wichtig: Korrekte Instanziierung
                return ekg_by_id  # Frühzeitiger return möglich
    return ekg_by_id

# %%
# if __name__ == "__main__":
    # print("This is a module with some functions to read the EKG data")
    # file = open("data/person_db.json")
    # person_data = json.load(file)
    # ekg_dict = person_data[0]["ekg_tests"][0]
    # print(ekg_dict)
    # ekg = EKGdata(ekg_dict)
    # print(ekg.df.head())