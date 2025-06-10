# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# %%
def load_data(FILE_PATH):
    """
    Lädt die Daten aus einer CSV- oder NPY-Datei und gibt sie als df_power zurück
    """
    _ , ext = os.path.splitext(FILE_PATH) #spaltet den Dateinamen in Name und Dateiformat
    if ext == ".csv":
        df = pd.read_csv(FILE_PATH)
        df_power = df[["Duration", "PowerOriginal"]].copy()
    elif ext == ".npy":
        arr = np.load(FILE_PATH)
        df_power = pd.DataFrame(arr, columns=["Duration", "PowerOriginal"])
    else:
        raise ValueError("FILE_PATH muss auf eine csv oder npy Datei zeigen.")

    return df_power


def plot_power(df_power):
    """
    Visualisiert den Leistungsverlauf über die Zeit als Liniendiagramm.
    Und gibt dieses zurück.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_power["PowerOriginal"], label='Power', color='blue')
    ax.set_title('Power over Time')
    ax.set_xlabel('Time in [s]')
    ax.set_ylabel('Power in [W]')
    ax.legend()
    ax.grid()
    return fig

def plot_power_duration_curve(df_power):
    """
    Plottet für jede mögliche Zeitdauer (in Sekunden) die maximal über diesen Zeitraum
    im Mittel erbrachte Leistung (Power Duration Curve).
    """
    df_power = df_power["PowerOriginal"]
    
    max_durations = np.arange(1, min(1801, len(df_power)))  # Array mit Zeitdauern von 1 Sekunde bis 1800 Sekunden: [1, 2, 3, ..., 1800]
    max_avg_power = [] # Liste zum SPeichern der maximalen Durchschnittsleistungen dür jede Zeitdauer

    for duration in max_durations: # Iteration über alle Zeitdauern, die in max_durations gespeichert sind
        # .rolling(window=duration).mean() berechnet den Durchschnitt aus allen Leistungswerten(geht einmal über gesamte Leistungskurve), die in einem Fenster mit der Länge "duration" liegen.
        rolling_avg = df_power.rolling(window=duration).mean()
        max_avg = rolling_avg.max() # Speicher den maximal Durchschnittswert für das aktuelle Fenster
        max_avg_power.append(max_avg) # Fügt den maximalen Durchschnittswert der Liste max_average_power an, so wird die Maximale Leistung für 1 Sekunde, 2 Sekunden dann 3 Sekunden usw in dieser aufsteigenen Reihenfolge gespeichert.

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(max_durations, max_avg_power, color='green')
    ax.set_title('Power Duration Curve')
    ax.set_xlabel('Zeitdauer [s]')
    ax.set_ylabel('Leistung [W]')
    ax.grid()
    return fig

# %%
if __name__ == "__main__":
    fig1 = plot_power(load_data("../data/activity.csv"))
    plt.show(fig1)
    fig2 = plot_power_duration_curve(load_data("../data/activity.csv"))
    plt.show(fig2)
    # FILE_PATH = "../data/activity.csv"
    # df_power = load_data(FILE_PATH)
    # plot_power(df_power)