import sys
import os
sys.path.append(os.path.abspath("..")) 

import pandas as pd
import plotly.express as px
from person_class import Person


# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:
    '''
    Beschreibt Objekte, die zu Personen gehören, Daten zu "Messwerte in mV" und "Zeit in ms" beinhalten
    Durch klasseneigene Funktionen können die Daten geladen, Peaks gefunden und beide zusammen geplottet werden.
    '''
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]) # EKG-Dateien kommen immer als .txt
        if len(self.df) *0.05 < 2000:
            self.plotted_length = 2000
        else:
            self.plotted_length = int(len(self.df) *0.1)
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
        peak_df = self.df.head(2000)
        peak_df= peak_df[peak_df["Peaks"]]

        fig.add_scatter(
            x = peak_df["Zeit in ms"], 
            y = peak_df["Messwerte in mV"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
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
            delta_time_sec = (t2 - t1) / 1000.0

            if delta_time_sec > 0:
                hr = 60 / delta_time_sec
                hr_series[idx2] = hr  # Setze den Wert nur beim zweiten Peak

        # Füge Herzfrequenzspalte dem DataFrame hinzu
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
    
if __name__ == "__main__":
    # visualiesiert schonmal Werte, aber die sind so zusammengerückt, dass keine Zuordnung mehr zur eigentlichen Zeit besteht --> Anpassung nötig
    import plotly.graph_objects as go
    ekg1 = EKGdata.load_by_id(1)
    ekg1.estimate_hr()
    # Nur die Zeilen mit gültigem HR-Wert (nicht None) herausfiltern
    valid_hr_df = ekg1.df[ekg1.df["Estimated HR"].notna()]

    # Plot erstellen
    fig = go.Figure()

    # Optional: graue Hintergrundlinie für visuelle Referenz (komplett leere Zeitreihe)
    fig.add_trace(go.Scatter(
        x=ekg1.df["Zeit in ms"],
        y=[None] * len(ekg1.df),
        mode="lines",
        name="HR (leer)",
        line=dict(color='lightgray', dash='dot')
    ))

    # Streudiagramm für echte HR-Werte (z. B. an den Peaks)
    fig.add_trace(go.Scatter(
        x=valid_hr_df["Zeit in ms"],
        y=valid_hr_df["Estimated HR"],
        mode="markers+lines",  # nur Punkte: "markers", mit Linien: "markers+lines"
        marker=dict(size=8, color="red"),
        line=dict(color="red"),
        name="Herzfrequenz (bpm)"
    ))

    # Achsentitel und Layout
    fig.update_layout(
        title="Herzfrequenz über Zeit (nur berechnet an Peaks)",
        xaxis_title="Zeit in ms",
        yaxis_title="Herzfrequenz (bpm)",
        template="plotly_white"
    )

    fig.show()

