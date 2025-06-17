import sys
import os
sys.path.append(os.path.abspath("..")) 

import pandas as pd
import plotly.express as px
from person_class import Person


# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]) # EKG-Dateien kommen immer als .txt
        self.plotted_length = None
        if len(self.df) *0.05 < 2000:
            self.plotted_length = 2000
        else:
            self.plotted_length = int(len(self.df) *0.05)
        self.find_peaks()



    def find_peaks(self, threshold=0.95, min_peak_distance=10, plotted_length= None):
        """
        Findet Peaks in der EKG-Datenreihe und speichert sie im DataFrame.
        Optional können threshold und min_peak_distance angepasst werden.
        Eingabeparameter: self, self, threshold=0.95, min_peak_distance=10, plotted_length= None
        """
        if plotted_length == None:
            plotted_length = self.plotted_length
        df_ekg = self.df.head(plotted_length)
        threshold_value = threshold * df_ekg["Messwerte in mV"].max()
        last_peak_index = 0
        list_of_index_peaks = []

        for index, row in df_ekg.iterrows():
            if index < df_ekg.index.max() - 1 and index >= 1:
                if row["Messwerte in mV"] >= df_ekg.iloc[index - 1]["Messwerte in mV"] and row["Messwerte in mV"] >= df_ekg.iloc[index + 1]["Messwerte in mV"]:
                    if row["Messwerte in mV"] > threshold_value and index - last_peak_index > min_peak_distance:
                        list_of_index_peaks.append(index)
                        last_peak_index = index

        self.df["Peaks"] = self.df.index.isin(list_of_index_peaks)


    def plot_time_series(self):
        '''
        Plottet DataFrame, also Messwerte in mV über die Zeit in s
        Eingabeparameter: self
        Ausgabeparameter: Diagramm Messwerte über Zeit
        '''
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit auf der x-Achse
        fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        peak_df = self.df.head(2000)[self.df["Peaks"].head(2000)]

        fig.add_scatter(
            x = peak_df["Zeit in ms"], 
            y = peak_df["Messwerte in mV"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
        )
        return fig
    
    def estimate_hr(self) -> list:
        '''
        Errechnet Herzfrequenz aus Peaks über Zeit
        Eingabeparameter: self als DataFrame
        Ausgabeparameter: Liste mit Herzfrequenzen
        '''
        peak_indices= self.find_peaks(self.df)
        
        hr_series = [None] * len(self.df)  # Leere Liste für Spalte
        
        delta_time_ms = self.df.loc[idx2, "Zeit in ms"] - self.df.loc[idx1, "Zeit in ms"]
        delta_time_sec = delta_time_ms / 1000.0

        for i in range(1, len(peak_indices)):
            idx1 = peak_indices[i - 1]
            idx2 = peak_indices[i]

            delta_time_sec = idx2- idx1
            hr = 60 / delta_time_sec

            hr_series[idx2] = hr

        self.df["Estimated HR"] = hr_series
        return hr_series


def load_by_id(ekg_id):
    '''
    Erstellt EKG-Objekt aus Datenbank nach ID
    Eingabeparameter: ID des gesuchten EKGs
    Ausgabeparameter: gesuchtes EKG-Objekt
    '''
    ekg_by_id = None

    person_data = Person.load_person_data()
    for person in person_data:
        for ekg_test in person["ekg_tests"]:
            if int(ekg_id) == int(ekg_test["id"]):
                ekg_by_id = EKGdata(ekg_test) 
                return ekg_by_id
    return ekg_by_id