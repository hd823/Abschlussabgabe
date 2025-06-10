import pandas as pd
from plotly import express as px
import plotly.graph_objects as go

# Load the heartrate date into a DataFrame
FILE_PATH = "../data/activity.csv"
df = pd.read_csv(FILE_PATH) # ".." Befehl zum Wechsel in das übergeordnete Verzeichnis, danach geht der Pfad in data weiter
df # Variablen ohne weitere Verarbeitungen werden direkt angezeigt

# Erstellen aller Zonen als neue Spalte
df["Zone"] = None

max_hr = int(input("Geben Sie Ihre maximale Herzfrequenz ein: ")) # Eingabe der maximalen Herzfrequenz
hr_zones = {}
counter = 1
for percent in range(50, 100, 10):
    hr_zones["Zone " + str(counter)] = max_hr * percent / 100
    counter += 1

current_zone = []
for row in df.iterrows():
    # print(row[1]["HeartRate"])
    current_hr = row[1]["HeartRate"]
    print(current_hr)

    if current_hr > hr_zones["Zone 5"]:
        current_zone.append("Zone 5")
    elif current_hr > hr_zones["Zone 4"]:
        current_zone.append("Zone 4")
    elif current_hr > hr_zones["Zone 3"]:
        current_zone.append("Zone 3")
    elif current_hr > hr_zones["Zone 2"]:
        current_zone.append("Zone 2")
    else:
        current_zone.append("Zone 1")

df["CurrentZone"] = current_zone

df_zone5 = df.groupby("CurrentZone").mean()

# Unbedingt nötig, damit Plotly die Zeitachse korrekt anzeigt
df["Time"] = df.index 
# Zeit in Minuten als neue Spalte
df["Time_min"] = df["Time"] / 60

# Basis-Plot für HeartRate
fig1 = go.Figure()

# HeartRate-Linie (linke Y-Achse)
fig1.add_trace(go.Scatter(
    x=df["Time_min"],
    y=df["HeartRate"],
    name="Heart Rate",
    line=dict(color="blue"),
    yaxis="y1"
))

# Power-Linie (rechte Y-Achse)
fig1.add_trace(go.Scatter(
    x=df["Time_min"],
    y=df["PowerOriginal"],
    name="Power",
    line=dict(color="orange"),
    yaxis="y2"
))

# Layout für zwei Y-Achsen
fig1.update_layout(
    title="Heart Rate and Power over Time",
    xaxis=dict(
        title="Time [min]",
        tickmode="array",
        tickvals=[0, 5, 10, 15, 20, 25, 30],
        ticktext=["0", "5", "10", "15", "20", "25", "30"],
        range=[0, 30],
        showgrid=False  # Entfernt vertikale Gridlines auf linker Achse
    ),
    yaxis=dict(
        title="Heart Rate (bpm)",
        range=[80, max_hr],
        showgrid=False  # Entfernt horizontale Gridlines
    ),
    yaxis2=dict(
        title="Power (W)",
        overlaying="y",
        side="right",
        range=[0, 440],
        showgrid=False  # Entfernt horizontale Gridlines auf rechter Achse
    ),
    legend=dict(
        x=0.01, y=0.99,
        bgcolor="rgba(255,255,255,0.5)"
    )
)

# einfärben: Zone 1
fig1.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, x1=1, y0=0, y1=max_hr * 0.6,
    fillcolor="rgba(173,216,230,0.2)", opacity=0.3, layer="below", line_width=0
)

# einfärben: Zone 2
fig1.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, x1=1, y0=max_hr * 0.6, y1= max_hr * 0.7,
    fillcolor="rgba(144,238,144,0.2)", opacity=0.3, layer="below", line_width=0
)

# einfärben: Zone 3
fig1.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, x1=1, y0=max_hr * 0.7, y1=max_hr * 0.8,
    fillcolor="rgba(255,255,102,0.2)", opacity=0.3, layer="below", line_width=0
)

# einfärben: Zone 4, 
fig1.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, x1=1, y0=max_hr * 0.8, y1=max_hr * 0.9,
    fillcolor="rgba(255,165,0,0.2)", opacity=0.3, layer="below", line_width=0
)

# einfärben: Zone 5
fig1.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, x1=1, y0=max_hr * 0.9, y1=max_hr,
    fillcolor="rgba(255, 99, 71, 0.2)", opacity=0.9, layer="below", line_width=0
)

fig1.show()



time_per_zone = df["CurrentZone"].value_counts().sort_index().rename("Anzahl Messpunkte").to_frame()
time_per_zone["Zeit [s]"] = time_per_zone["Anzahl Messpunkte"]
time_per_zone["Zeit [min]"] = (time_per_zone["Zeit [s]"] / 60).round(2)
time_per_zone["Leistung [W]"] = df.groupby("CurrentZone")["PowerOriginal"].mean().round(2)
time_per_zone.drop(columns=["Anzahl Messpunkte"], inplace=True)
 
print(time_per_zone)