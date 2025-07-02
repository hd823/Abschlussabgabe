import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data_power(FILE_PATH = "data/activity.csv"):
    """
    Lädt Leistungsdaten aus CSV- oder NPY-Dateien.
    Eingabeparameter: 
        FILE_PATH (str): Pfad zur Datei
    Ausgabeparameter: DataFrame mit 'Duration' und 'PowerOriginal'
    """
    _ , ext = os.path.splitext(FILE_PATH)
    if ext == ".csv":
        with open(FILE_PATH) as file:
            df = pd.read_csv(FILE_PATH)
            df_power = df[["Duration", "PowerOriginal"]].copy()
        return df_power
    elif ext == ".npy":
        with open(FILE_PATH) as file:
            arr = np.load(FILE_PATH)
            df_power = pd.DataFrame(arr, columns=["Duration", "PowerOriginal"])
        return df_power
    else:
        raise ValueError("FILE_PATH muss auf eine csv oder npy Datei zeigen.")

def plot_power(df_power):
    """
    Plottet den Leistungsverlauf über die Zeit als Liniendiagramm.
    Eingabeparameter: 
        df_power (DataFrame): Ergebnis aus load_data_power
    Ausgabeparameter: Matplotlib-Figure-Objekt
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
    Erstellt eine Power Duration Curve (maximale Durchschnittsleistung über Zeitintervalle).
    Eingabeparameter:
        df_power (DataFrame): Ergebnis aus load_data_power
    Ausgabeparameter: Matplotlib-Figure-Objekt
    """
    df_power = df_power["PowerOriginal"]
    max_durations = np.arange(1, min(1801, len(df_power)))
    max_avg_power = []

    for duration in max_durations:
        rolling_avg = df_power.rolling(window=duration).mean()
        max_avg = rolling_avg.max()
        max_avg_power.append(max_avg)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(max_durations, max_avg_power, color='green')
    ax.set_title('Power Duration Curve')
    ax.set_xlabel('Zeitdauer [s]')
    ax.set_ylabel('Leistung [W]')
    ax.grid()
    return fig

if __name__ == "__main__":
    fig1 = plot_power(load_data_power("../data/activity.csv"))
    plt.show(fig1)
    fig2 = plot_power_duration_curve(load_data_power("../data/activity.csv"))
    plt.show(fig2)
