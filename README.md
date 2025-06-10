# Projekt_gesamt

Hier drinnen sollen alle Aufgaben für die Programmierübung des Sommersemester 2025 bearbeitet werden


## Funktionsumfang
Hier liegt ein Skript "min.py", mit dem wir eine Leistungskurve plotten.

## Anforderungen und Nutzung

### Zum Installieren des Projekts
- Repository clonen
- 'pdm install' in Powershell-Terminal schreiben, um dem Projekt zu Grunde liegende Bbliotheken und Versionen zu installieren.

- Die Beispieldaten liegen im Ordner 'data' unter 'activity.csv'

### Zum Starten des Projekts
- Im Ordner 'source' die Datei 'power_curve.py ausführen


## Beispielergebnis
![](figures/power_curve.png)

# EKG-App

## Funktionsbeschreibung
Die App soll __Diagnostiker:in__ ermöglichen, EKG_Daten verschiedener Patienten zu erfassen, zu speicher und auszuwerten. Die App soll eine einfache und intuiteve Benutzeroberfläche bierten, um die Bedienung zu erleichtern.
Der __Admin__ kann __Diagnostiker:in__ anlegen.

![](.docs/UML-Diagramm_UseCases.png)

### Use Cases
- UC1: EKG eines Tests auswerten
    UC1.1: ...
- UC2:

## Implementierung
__USe Case 1__ Die User Journey für die Diagnostiker:in, wenn sie einen Test auswerten möchte, folgt aus dem Activity Diagramm:

![](.docs/ekg_data._acticitydiagramm.svg)

### Design

Hier folgen erste Entwürfe eines UI Designs. Das Design ist für die Darstellung auf einem PC optimiert (Querformat). Keine seperaten Frames.

# EKG App - Streamlit Anwendung
Die App dient zur Visualisierung von EKG-Daten und wurde als Streamlit-Anwendung für die Sakai-Abgabe 2 entwickelt.

## Anwendung starten
In der Powershell 'streamlit run main_streamlit_app.py' eingeben.
Nach kurzer Ladezeit öffnet sich automatisch ein Browserfenster unter der URL "http://localhost:8501/" mit der App-Oberfläche. Falls Änderungen am Code vorgenommen werden, müssen diese gespeichert und die Streamlit-Seite im Browser neu geladen werden.


## Funktionsweise der EKG APP

### Auswahl der Versuchsperson
Zu Beginn wird der Name der Versuchsperson ausgewählt. Anschließend erscheint das zugehörige Bild der Person.

### Eingabe der maximalen Herzfrequenz
Diese kann manuell eingegeben oder über Plus-/Minus-Buttons angepasst werden.
Dadurch änderen sich die Einfärbungen der Zonene unter dem Graphen der Herzfrequenz und die Zeit in einzelenen Zonen sowie die Durchschnittsleistung.

### Darstellung der Daten
Zum Schluss wird ein Plot angezeigt, der die Herzfrequenz- und Leistungsdaten über die Zeit visualisiert.

### Tabelle mit Durchschnittsleistung und Zeit in Zonen
Es werden die Gesamtzeiten in den einzelnen Zonen und die durchschnittliche Leistung in diesen in einer Tabelle visualiesiert.

## Sakai Abgabe 2 - EKG APP
Im folgenden Bild ist ein Screenshot der EKG-App zu sehen:

![](figures\screenshot_app.png)


# Leistungskurve 2 - Abgabe 3
Ziel der Abgabe ist das Schreiben eines Skripts zur Erstellung eines Diagramms der Leistung in W über die gesamte Zeit der Activität.
Dabei soll die Eingabe aus einer CSV-Datei oder aber auch einer NPY-Datei erfolgen können.
Danach soll ein klassisches "Power Duration Curve"-Diagramm erstellt werden.

## Verwendung des Skripts main_power_figures.py
Zur Erstellung der beiden Diagramme muss die Datei main_power_figures.py ausgeführt werden.

### Beispiel Ausgaben
Aus dem Beispiel-Datensatz "activity.csv" werden folgende Diagramme erstellt:

![](figures\screenshot_leistungskurve2.png)