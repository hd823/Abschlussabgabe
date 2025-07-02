# Abschlussabgabe Programmierübung 2
## Ida Dürr-Pucher, Hauke Döllefeld

### Zum Installieren des Projekts
- Repository clonen
- 'pdm install' in Powershell-Terminal schreiben, um dem Projekt zu Grunde liegende Bbliotheken und Versionen zu installieren.

# EKG App - Streamlit Anwendung
Die App dient zur Visualisierung von EKG-Daten und wurde als Streamlit-Anwendung entwickelt.

## Anwendung starten
In der Powershell 'streamlit run Startseite.py' eingeben.
Wenn der Fehler "no module named streamlit" ausgegeben wird, muss in der Powershell folgender Befehl zum Öffnen der Streamlit Applikation verwendet werden: "pdm run streamlit".
Nach kurzer Ladezeit öffnet sich automatisch ein Browserfenster unter der URL "http://localhost:8501/" mit der App-Oberfläche. Falls Änderungen am Code vorgenommen werden, müssen diese gespeichert und die Streamlit-Seite im Browser neu geladen werden.

# Startseite
Auf der Startseite wird das Bild und weitere Daten der aktuellen Versuchsperson ausgegeben. Zudem ist eine Auswahl von EKG-Daten möglich, die standartmäßig die ersten 60 Sekunden plottet, die Durchschnittsherzfrequenz über die gesamte Versuchsdauer und den aktuell geplotteten Zeitbereich ausgibt. Die geplottete Fenstergröße kann über das Eingabefeld "Geplottete Länge des EKG-Tests in Sekunden:" eingestellt werden. Mit dem Slider kann ein Bereich mit entsprechender Größe ausgewählt werden. Wenn genauere Auflösung eines geplotteten Bereichs nötig ist, kann über Linksklick gedrückt halten oder linker Doppelklick und horizontale Verschiebung der Maus genauere Bereiche gezeigt werden.

# Personendaten
Die mit Sternchen versehenen Eingaben sind Pflichtfelder, der Rest ist optional.
## Tab 1: Personen hinzufügen
## Tab 2: Personen bearbeiten

# HF Analyse
Dieser Tab ist relativ losgelöst von den anderen und der Grundaufgabenstellung und sind ohne tiefer führenden Vergleich von kleiner Bedeutung.