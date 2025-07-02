import sys
import os
sys.path.append(os.path.abspath("..")) 

import pandas as pd
import streamlit as st
import plotly.express as px
from person_class import Person 
import neurokit2 as nk

class EKGdata:
    '''
    Beschreibt Objekte, die zu Personen gehören, Daten zu "Messwerte in mV" und "Zeit in ms" beinhalten
    Durch klasseneigene Funktionen können die Daten geladen, Peaks gefunden und beide zusammen geplottet werden.
    '''
    def __init__(self, ekg_dict,):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=["Messwerte in mV","Zeit in ms",]) # EKG-Dateien kommen immer als .txt
        self.df["Zeit in s"] = self.df["Zeit in ms"] / 1000
        self.df["Zeit in min"] = self.df["Zeit in s"] / 60
        self.set_peaks()
        
    def find_peaks(self):

        df_ekg_subset = self.df.copy()

        info = nk.ecg_findpeaks(df_ekg_subset["Messwerte in mV"], sampling_rate=600, show=False)
        return info

    def set_peaks(self):
        """
        Findet Peaks in der EKG-Datenreihe und speichert sie im DataFrame.
        """
        info = self.find_peaks()

        self.df["Peaks"] = 0
        if "ECG_R_Peaks" in info and len(info["ECG_R_Peaks"]) > 0:
            r_peaks_indices = info["ECG_R_Peaks"]
            self.df.loc[r_peaks_indices, "Peaks"] = 1
        else:
            print(f"Keine R-Peaks für EKG ID {self.id} gefunden. 'Peaks'-Spalte bleibt 0.")


    def plot_time_series(self, start_s=None, end_s=None):
        '''
        Plottet DataFrame, also Messwerte in mV über die Zeit in s
        Eingabeparameter: self, optional start_s (Sekunden), optional end_s (Sekunden)
        Ausgabeparameter: Diagramm Messwerte über Zeit
        '''

        df_to_plot = self.df.copy()

        if start_s is not None and end_s is not None:
            df_to_plot = df_to_plot[(df_to_plot["Zeit in s"] >= start_s) & (df_to_plot["Zeit in s"] <= end_s)]
        else:
            pass
        
        if df_to_plot.empty:
            st.warning("Keine Daten im ausgewählten Zeitbereich gefunden. Bitte passen Sie den Bereich an.")
            return px.line(title="Keine Daten im ausgewählten Bereich", template="plotly_white")

        fig = px.line(df_to_plot, x="Zeit in min", y="Messwerte in mV")

        peak_df = df_to_plot[df_to_plot["Peaks"] == 1]

        fig.add_scatter(
            x = peak_df["Zeit in min"],
            y = peak_df["Messwerte in mV"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
        )

        fig.update_layout(
            xaxis_title="Zeit in Minuten",
            yaxis_title="Messwerte in mV",
            title=f"EKG Signal Ansicht (von {round(start_s/60, 2)}min bis {round(end_s/60, 2)}min)" if start_s is not None else "EKG Signal Ansicht"
        )

        return fig
    
    def estimate_hr(self) -> list:
        """
        Errechnet die Herzfrequenz (in bpm) aus dem Abstand zwischen R-Peaks.
        Gibt eine Liste mit den geschätzten Werten zurück, wobei nur bei den Peaks ein Wert steht, sonst None.
        """
        # Hole die Indizes der gefundenen Peaks
        peak_indices = self.df.index[self.df["Peaks"] == True].tolist()

        # Leere Liste für alle Werte (gleiche Länge wie DataFrame)
        hr_series = [None] * len(self.df)

        if len(peak_indices) < 2:
            print("Nicht genug Peaks gefunden für HR-Schätzung.")
            self.df["Estimated HR"] = hr_series
            return hr_series

        for i in range(1, len(peak_indices)):
            idx1 = peak_indices[i - 1]
            idx2 = peak_indices[i]

            # Zeit in Millisekunden → in Sekunden umrechnen
            t1 = self.df.at[idx1, "Zeit in ms"]
            t2 = self.df.at[idx2, "Zeit in ms"]
            delta_time_sec = (t2 - t1) / 1000

            if delta_time_sec > 0:
                hr = 60 / delta_time_sec
                hr_series[idx2] = hr   # Setze den Wert nur beim zweiten Peak

        # Füge Herzfrequenzspalte dem DataFrame hinzu
        self.df["Estimated HR"] = hr_series
        return hr_series


    @staticmethod
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