import sys
import os
sys.path.append(os.path.abspath("..")) 

import pandas as pd
import streamlit as st
import plotly.express as px
from person_class import Person 
import neurokit2 as nk
import numpy as np

class EKG:
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
    
    def estimate_hr(self, start_s=None, end_s=None):
        """
        Schätzt die Herzfrequenz in bpm auf Basis der in self.df gespeicherten Peaks.
        Optional kann ein Zeitbereich in Sekunden angegeben werden.
        """
        if start_s is None and end_s is None:
            # Wenn kein Zeitbereich angegeben ist, gesamtes DataFrame verwenden
            start_s = self.df["Zeit in s"].min()
            end_s = self.df["Zeit in s"].max()

        df = self.df.copy()

        if self.df.empty:
            st.warning("Keine EKG-Daten verfügbar, um die Herzfrequenz zu schätzen.")
            return None

        # Falls Zeitbereich angegeben ist, DataFrame filtern
        if start_s is not None:
            df = df[df["Zeit in s"] >= start_s]
        if end_s is not None:
            df = df[df["Zeit in s"] <= end_s]

        # Filtere nur Zeilen mit erkannten Peaks
        peak_df = df[df["Peaks"] == 1]

        # Prüfen, ob genügend Peaks vorhanden sind
        if len(peak_df) < 2:
            return None  # Zu wenig Daten für Berechnung

        # Zeitstempel der Peaks extrahieren
        time_stamps = peak_df["Zeit in ms"].values
        rr_intervals = np.diff(time_stamps)  # in ms

        avg_rr = np.mean(rr_intervals)

        hr_bpm = 60000 / avg_rr  # Umrechnung in bpm

        return round(hr_bpm, 2)



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
                    ekg_by_id = EKG(ekg_test) 
                    return ekg_by_id
        return ekg_by_id
    
    @staticmethod
    def validate_ekg_file(file_path):
        try:
            df = pd.read_csv(file_path, sep='\t', header=None)
            if df.shape[1] != 2 or df.empty:
                return False
            
            # Versuche, beide Spalten in numerische Werte umzuwandeln
            df[0] = pd.to_numeric(df[0], errors='coerce')
            df[1] = pd.to_numeric(df[1], errors='coerce')
            
            # Prüfe, ob nach der Umwandlung NaN-Werte vorkommen -> ungültig
            if df[0].isna().any() or df[1].isna().any():
                return False
            return True
        except Exception as e:
            print(f"Fehler beim Validieren der EKG-Datei: {e}")
            return False
