import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Code zum Assignment 3

def analyse_heart_rate(FILE_PATH = "data/activity.csv", max_hr = 200):
    '''
    Analysiert Herzfrequenzdaten und ordnet sie Herzfrequenzzonen zu.
    Eingabeparameter: 
        FILE_PATH (str): Pfad zur CSV-Datei
        max_hr (int): Maximale Herzfrequenz
    Ausgabeparameter: DataFrame mit Spalte 'CurrentZone'
    '''
    df_hr = pd.read_csv(FILE_PATH)

    hr_zones = {}
    counter = 1

    for percent in range(50, 100, 10):
        hr_zones["Zone " + str(counter)] = max_hr * percent / 100
        counter += 1

    current_zone = []
    for row in df_hr.iterrows():
        current_hr = row[1]["HeartRate"]
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
    df_hr["CurrentZone"] = current_zone

    return df_hr

def plot_analysed_hr(df_hr, max_hr = 200):
    '''
    Erstellt ein kombiniertes Diagramm der Herzfrequenz und Leistung über die Zeit.
    Eingabeparameter: 
        df_hr (DataFrame): Ergebnis aus analyse_heart_rate
        max_hr (int): Maximale Herzfrequenz
    Ausgabeparameter: Plotly-Figure-Objekt
    '''
    df_hr["Time"] = df_hr.index 
    df_hr["Time_min"] = df_hr["Time"] / 60

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=df_hr["Time_min"],
        y=df_hr["HeartRate"],
        name="Heart Rate",
        line=dict(color="blue"),
        yaxis="y1"
    ))

    fig1.add_trace(go.Scatter(
        x=df_hr["Time_min"],
        y=df_hr["PowerOriginal"],
        name="Power",
        line=dict(color="orange"),
        yaxis="y2"
    ))

    fig1.update_layout(
        title="Heart Rate and Power over Time",
        xaxis=dict(
            title="Time [min]",
            tickmode="array",
            tickvals=[0, 5, 10, 15, 20, 25, 30],
            ticktext=["0", "5", "10", "15", "20", "25", "30"],
            range=[0, 30],
            showgrid=False
        ),
        yaxis=dict(
            title="Heart Rate (bpm)",
            range=[80, max_hr],
            showgrid=False
        ),
        yaxis2=dict(
            title="Power (W)",
            overlaying="y",
            side="right",
            range=[0, 440],
            showgrid=False
        ),
        legend=dict(
            x=0.01, y=0.99,
            bgcolor="rgba(255,255,255,0.5)"
        )
    )

    fig1.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1, y0=0, y1=max_hr * 0.6,
        fillcolor="rgba(173,216,230,0.2)", opacity=0.99, layer="below", line_width=0
    )

    fig1.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1, y0=max_hr * 0.6, y1= max_hr * 0.7,
        fillcolor="rgba(144,238,144,0.2)", opacity=0.99, layer="below", line_width=0
    )

    fig1.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1, y0=max_hr * 0.7, y1=max_hr * 0.8,
        fillcolor="rgba(255,255,102,0.2)", opacity=0.99, layer="below", line_width=0
    )

    fig1.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1, y0=max_hr * 0.8, y1=max_hr * 0.9,
        fillcolor="rgba(255,165,0,0.2)", opacity=0.99, layer="below", line_width=0
    )

    fig1.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1, y0=max_hr * 0.9, y1=max_hr,
        fillcolor="rgba(255, 99, 71, 0.2)", opacity=0.99, layer="below", line_width=0
    )
    return fig1

def calculate_time_per_zone(df_hr):
    '''
    Berechnet die verbrachte Zeit und durchschnittliche Leistung pro Herzfrequenzzone.
    Eingabeparameter: 
        df_hr (DataFrame): Ergebnis aus analyse_heart_rate
    Ausgabeparameter: Plotly-Tabelle mit Zeit und Leistung je Zone
    '''
    zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]
    zone_counts = df_hr["CurrentZone"].value_counts().reindex(zones, fill_value=0)
    time_per_zone = zone_counts.rename("Anzahl Messpunkte").to_frame()
    time_per_zone["Zeit [s]"] = time_per_zone["Anzahl Messpunkte"]
    time_per_zone["Zeit [min]"] = (time_per_zone["Zeit [s]"] / 60).round(2)
    time_per_zone["Leistung [W]"] = df_hr.groupby("CurrentZone")["PowerOriginal"].mean().reindex(zones).round(2)
    time_per_zone.drop(columns=["Anzahl Messpunkte"], inplace=True)
    time_per_zone.reset_index(inplace=True)
    time_per_zone.rename(columns={"index": "Zone"}, inplace=True)

    fig = ff.create_table(time_per_zone)
    return fig

if __name__ == "__main__":
    my_fig = plot_analysed_hr(analyse_heart_rate(),)
    calculate_time_per_zone(analyse_heart_rate())
    my_fig.show(render_mode='browser')
    fig = calculate_time_per_zone(analyse_heart_rate())
    fig.show()
