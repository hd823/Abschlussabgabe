# import sys
# import os
# sys.path.append(os.path.abspath("..")) 

# import pandas as pd
# import plotly.express as px
# from person_class import Person
# import neurokit2 as nk

# class EKGdata:
#     '''
#     Beschreibt Objekte, die zu Personen gehören, Daten zu "Messwerte in mV" und "Zeit in ms" beinhalten
#     Durch klasseneigene Funktionen können die Daten geladen, Peaks gefunden und beide zusammen geplottet werden.
#     '''
#     def __init__(self, ekg_dict, plotted_length=None):
#         self.id = ekg_dict["id"]
#         self.date = ekg_dict["date"]
#         self.data = ekg_dict["result_link"]
#         self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]) # EKG-Dateien kommen immer als .txt
#         if len(self.df) *0.05 < 2000:
#             self.plotted_length = 2000
#         else:
#             self.plotted_length = int(len(self.df) *0.1)
#         self.set_peaks()
        

#     def find_peaks(self, plotted_length=2000):
#         if plotted_length is None:
#             plotted_length = self.plotted_length
#         df_ekg_subset = self.df.head(plotted_length).copy()
#         return nk.ecg_findpeaks(df_ekg_subset["Messwerte in mV"], sampling_rate=700, show=False)

        
#     def set_peaks(self):
#         """
#         Findet Peaks in der EKG-Datenreihe und speichert sie im DataFrame.
#         Optional können threshold und min_peak_distance angepasst werden.
#         """
#         _, info = self.find_peaks()

#         self.df["Peaks"] = 0 # Initialisiere mit 0

#         r_peaks_indices = info["ECG_R_Peaks"]

#         self.df.loc[r_peaks_indices, "Peaks"] = 1

#     def plot_time_series(self):
#         '''
#         Plottet DataFrame, also Messwerte in mV über die Zeit in s
#         Eingabeparameter: self
#         Ausgabeparameter: Diagramm Messwerte über Zeit
#         '''
#         # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit auf der x-Achse
#         fig = px.line(self.df.head(self.plotted_length), x="Zeit in ms", y="Messwerte in mV")
#         peak_df = self.df.head(self.plotted_length).copy()
#         peak_df= peak_df[peak_df["Peaks"]]

#         fig.add_scatter(
#             x = peak_df["Zeit in ms"], 
#             y = peak_df["Messwerte in mV"],
#             mode="markers",
#             marker=dict(color="red", size=8),
#             name="Peaks"
#         )
#         return fig
    
#     def estimate_hr(self) -> list:
#         """
#         Errechnet die Herzfrequenz (in bpm) aus dem Abstand zwischen R-Peaks.
#         Gibt eine Liste mit den geschätzten Werten zurück, wobei nur bei den Peaks ein Wert steht, sonst None.
#         """
#         # Hole die Indizes der gefundenen Peaks
#         peak_indices = self.df.index[self.df["Peaks"] == True].tolist()

#         # Leere Liste für alle Werte (gleiche Länge wie DataFrame)
#         hr_series = [None] * len(self.df)

#         if len(peak_indices) < 2:
#             print("Nicht genug Peaks gefunden für HR-Schätzung.")
#             self.df["Estimated HR"] = hr_series
#             return hr_series

#         for i in range(1, len(peak_indices)):
#             idx1 = peak_indices[i - 1]
#             idx2 = peak_indices[i]

#             # Zeit in Millisekunden → in Sekunden umrechnen
#             t1 = self.df.at[idx1, "Zeit in ms"]
#             t2 = self.df.at[idx2, "Zeit in ms"]
#             delta_time_sec = (t2 - t1) / 1000

#             if delta_time_sec > 0:
#                 hr = 60 / delta_time_sec
#                 hr_series[idx2] = hr  # Setze den Wert nur beim zweiten Peak

#         # Füge Herzfrequenzspalte dem DataFrame hinzu
#         self.df["Estimated HR"] = hr_series
#         return hr_series


#     def load_by_id(ekg_id):
#         '''
#         Erstellt EKG-Objekt aus Datenbank nach ID
#         Eingabeparameter: ID des gesuchten EKGs
#         Ausgabeparameter: gesuchtes EKG-Objekt
#         '''
#         ekg_by_id = None

#         person_data = Person.load_person_data()
#         for person in person_data:
#             for ekg_test in person["ekg_tests"]:
#                 if int(ekg_id) == int(ekg_test["id"]):
#                     ekg_by_id = EKGdata(ekg_test) 
#                     return ekg_by_id
#         return ekg_by_id
    
# # if __name__ == "__main__":
# #     # visualiesiert schonmal Werte, aber die sind so zusammengerückt, dass keine Zuordnung mehr zur eigentlichen Zeit besteht --> Anpassung nötig
# #     import plotly.graph_objects as go
# #     ekg1 = EKGdata.load_by_id(1)
# #     ekg1.estimate_hr()
# #     # Nur die Zeilen mit gültigem HR-Wert (nicht None) herausfiltern
# #     valid_hr_df = ekg1.df[ekg1.df["Estimated HR"].notna()]

# #     # Plot erstellen
# #     fig = go.Figure()

# #     # Optional: graue Hintergrundlinie für visuelle Referenz (komplett leere Zeitreihe)
# #     fig.add_trace(go.Scatter(
# #         x=ekg1.df["Zeit in ms"],
# #         y=[None] * len(ekg1.df),
# #         mode="lines",
# #         name="HR (leer)",
# #         line=dict(color='lightgray', dash='dot')
# #     ))

# #     # Streudiagramm für echte HR-Werte (z. B. an den Peaks)
# #     fig.add_trace(go.Scatter(
# #         x=valid_hr_df["Zeit in ms"],
# #         y=valid_hr_df["Estimated HR"],
# #         mode="markers+lines",  # nur Punkte: "markers", mit Linien: "markers+lines"
# #         marker=dict(size=8, color="red"),
# #         line=dict(color="red"),
# #         name="Herzfrequenz (bpm)"
# #     ))

# #     # Achsentitel und Layout
# #     fig.update_layout(
# #         title="Herzfrequenz über Zeit (nur berechnet an Peaks)",
# #         xaxis_title="Zeit in ms",
# #         yaxis_title="Herzfrequenz (bpm)",
# #         template="plotly_white"
# #     )

# #     fig.show()

# if __name__ == "__main__":
#     df = EKGAnalyzer.load_by_id(1).df
#     analyzer = EKGAnalyzer(df, plotted_length=1500)
#     analyzer.find_peaks()
#     print(analyzer.df.head(20)) # Zeige die ersten 20 Zeilen inkl. Peaks-Spalte


# ekg_data.py
import sys
import os
sys.path.append(os.path.abspath("..")) 

import pandas as pd
import plotly.express as px
# Stellen Sie sicher, dass der Import-Pfad für Person korrekt ist.
# Wenn person_class.py in 'source' liegt und ekg_data.py auch in 'source', dann ist es 'from person_class import Person'
# Wenn ekg_data.py direkt im Hauptverzeichnis wäre, dann müsste der Pfad anders sein.
# Basierend auf deiner Struktur sollte dies funktionieren, da source im sys.path ist.
from person_class import Person 
import neurokit2 as nk

class EKGdata:
    '''
    Beschreibt Objekte, die zu Personen gehören, Daten zu "Messwerte in mV" und "Zeit in ms" beinhalten
    Durch klasseneigene Funktionen können die Daten geladen, Peaks gefunden und beide zusammen geplottet werden.
    '''
    def __init__(self, ekg_dict, plotted_length=None):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',]) # EKG-Dateien kommen immer als .txt
        if len(self.df) *0.05 < 2000:
            self.plotted_length = 2000
        else:
            self.plotted_length = int(len(self.df) *0.1)
        self.set_peaks()
        
    def find_peaks(self, plotted_length=2000):
        if plotted_length is None:
            plotted_length = self.plotted_length
        df_ekg_subset = self.df.head(plotted_length).copy()
        
        # ÄNDERUNG HIER: Empfange das Ergebnis als einzelnes Tupel
        # und gib es dann zurück.
        # NeuroKit2 gibt (cleaned_signals, info) zurück.
        signals, info = nk.ecg_findpeaks(df_ekg_subset["Messwerte in mV"], sampling_rate=700, show=False)
        return signals, info # Gib beide Werte explizit zurück

    def set_peaks(self):
        """
        Findet Peaks in der EKG-Datenreihe und speichert sie im DataFrame.
        """
        # ÄNDERUNG HIER: Die find_peaks Methode sollte jetzt immer zwei Werte zurückgeben
        # So ist das Entpacken sicher.
        _, info = self.find_peaks()

        self.df["Peaks"] = 0 # Initialisiere mit 0

        # Prüfe, ob 'ECG_R_Peaks' im info-Dictionary vorhanden ist
        if "ECG_R_Peaks" in info and len(info["ECG_R_Peaks"]) > 0:
            r_peaks_indices = info["ECG_R_Peaks"]
            self.df.loc[r_peaks_indices, "Peaks"] = 1
        else:
            print(f"Keine R-Peaks für EKG ID {self.id} gefunden. 'Peaks'-Spalte bleibt 0.")


    def plot_time_series(self):
        '''
        Plottet DataFrame, also Messwerte in mV über die Zeit in s
        Eingabeparameter: self
        Ausgabeparameter: Diagramm Messwerte über Zeit
        '''
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit auf der x-Achse
        fig = px.line(self.df.head(self.plotted_length), x="Zeit in ms", y="Messwerte in mV")
        peak_df = self.df.head(self.plotted_length).copy()
        peak_df= peak_df[peak_df["Peaks"] == 1] # Filtern, um nur die Zeilen mit Peaks zu erhalten

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
        # Hier muss der Pfad zur person_db.json korrekt sein.
        # Da ekg_data.py in 'source' ist, und 'data' ein Geschwisterordner von 'source' ist,
        # oder auf der obersten Ebene liegt, muss der Pfad entsprechend angepasst werden.
        # Angenommen, 'data' liegt auf derselben Ebene wie 'main_streamlit_app.py' und 'source'.
        # Dann wäre der relative Pfad von ekg_data.py nach data/person_db.json: '../data/person_db.json'
        # oder './data/person_db.json' falls 'source' und 'data' sich den Parent teilen.
        # Am sichersten ist es, den absoluten Pfad zu verwenden oder den Basispfad zu übergeben.
        # Für diesen Fall nehmen wir an, dass `person_db.json` im `data`-Ordner auf der obersten Ebene liegt.
        
        # Um den Pfad korrekt zu finden, muss man wissen, wo `data/person_db.json` relativ zu dieser Datei ist.
        # Hier ist ein Ansatz, der davon ausgeht, dass die `person_db.json` im `data`-Ordner auf der obersten Ebene liegt:
        current_dir = os.path.dirname(os.path.abspath(__file__)) # Verzeichnis der aktuellen Datei (ekg_data.py)
        # Geh zwei Ebenen hoch, um zum Hauptverzeichnis der App zu kommen (falls source im Hauptverzeichnis ist)
        # main_app_dir = os.path.join(current_dir, '..', '..') 
        # Oder eine Ebene hoch, falls source direkt unter dem Hauptverzeichnis liegt und data auch
        main_app_dir = os.path.join(current_dir, '..') 
        
        person_db_path = os.path.join(main_app_dir, "data", "person_db.json")

        person_data = Person.load_person_data(person_db_path) # Übergib den Pfad explizit
        
        for person in person_data:
            for ekg_test in person["ekg_tests"]:
                if int(ekg_id) == int(ekg_test["id"]):
                    ekg_by_id = EKGdata(ekg_test) 
                    return ekg_by_id
        return ekg_by_id
    
# Anpassung der if __name__ == "__main__": Blöcke
# Der zweite Block hatte einen Fehler (EKGAnalyzer statt EKGdata)
# ... (dein bestehender Code bis zum if __name__ == "__main__": Block)

if __name__ == "__main__":
    # Testen der plot_time_series und estimate_hr Funktionen
    import plotly.graph_objects as go
    
    # Stellen Sie sicher, dass der Pfad zur person_db.json korrekt ist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_app_dir = os.path.join(current_dir, '..') 
    person_db_path = os.path.join(main_app_dir, "data", "person_db.json")

    # Person.load_person_data muss den Pfad zum JSON kennen
    # Dies ist eine Annahme basierend auf deinem Code, dass Person.load_person_data
    # direkt einen Pfad akzeptiert oder über eine Klassenvariable zugänglich ist.
    # Wenn Person.load_person_data keinen Pfad akzeptiert, musst du sicherstellen,
    # dass es den korrekten Pfad zu person_db.json findet.
    
    # Versuche EKGdata Objekt zu laden
    ekg1 = EKGdata.load_by_id(1)
    
    if ekg1: # Stelle sicher, dass ekg1 geladen wurde
        ekg1.estimate_hr()
        valid_hr_df = ekg1.df[ekg1.df["Estimated HR"].notna()]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=ekg1.df["Zeit in ms"],
            y=[None] * len(ekg1.df),
            mode="lines",
            name="HR (leer)",
            line=dict(color='lightgray', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            x=valid_hr_df["Zeit in ms"],
            y=valid_hr_df["Estimated HR"],
            mode="markers+lines",
            marker=dict(size=8, color="red"),
            line=dict(color="red"),
            name="Herzfrequenz (bpm)"
        ))

        fig.update_layout(
            title="Herzfrequenz über Zeit (nur berechnet an Peaks)",
            xaxis_title="Zeit in ms",
            yaxis_title="Herzfrequenz (bpm)",
            template="plotly_white"
        )
        
        # Füge diese Zeile hinzu, um die Grafik anzuzeigen!
        fig.show() 

    else:
        print("Konnte EKG-Daten für den Test nicht laden (ID 1).")

    # Korrektur des zweiten Testblocks (optional, da der erste Block bereits eine Grafik zeigt)
    # Hier solltest du entweder Person.load_person_data nutzen und dann ein EKG-Objekt erstellen
    # oder, wenn du die EKGdata Klasse direkt testen willst, ein passendes EKG-Dictionary bereitstellen.
    # Da dein EKGAnalyzer-Teil eine EKGdata Instanz erwartet, hier die Korrektur:
    # Annahme: Es gibt ein person_db.json und die load_by_id-Methode funktioniert
    # Das Laden des EKG-Objekts ist schon oben im ersten if-Block passiert.
    # Wenn du hier einen neuen Test für die Peak-Bestimmung machen möchtest:
    # ekg_test_obj = EKGdata.load_by_id(1)
    # if ekg_test_obj:
    #     ekg_test_obj.set_peaks() 
    #     print(ekg_test_obj.df.head(20))
    # else:
    #     print("Konnte EKG-Daten für den zweiten Test nicht laden (ID 1).")