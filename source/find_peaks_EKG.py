import pandas as pd
import plotly.express as px

def find_peaks(df_ekg, threshold = 0.95, min_peak_distance = 10):
    """
    Find peaks in the EKG data based on a threshold and minimum distance between peaks.
   
    Parameters:
    df (DataFrame): DataFrame containing EKG data with 'Voltage in mV' column.
    threshold (float): Threshold for peak detection as a fraction of the maximum voltage.
    min_peak_distance (int): Minimum distance between detected peaks in index units.
   
    Returns:
    list: List of indices where peaks are found.
    """
    threshold_value = threshold * df_ekg["Messwerte in mV"].max()
    last_peak_index = 0
    list_of_index_peaks = []

    for index, row in df_ekg.iterrows():
        if index < df_ekg.index.max() - 1 and index >= 1:
            if row["Messwerte in mV"] >= df_ekg.iloc[index - 1]["Messwerte in mV"] and row["Messwerte in mV"] >= df_ekg.iloc[index + 1]["Messwerte in mV"]:
                if row["Messwerte in mV"] > threshold_value and index - last_peak_index > min_peak_distance:
                    list_of_index_peaks.append(index)
                    last_peak_index = index
    return list_of_index_peaks


if __name__ == "__main__":
    df_ekg = pd.read_csv("../data/ekg_data/01_Ruhe.txt", sep="  ", names = ["Messwerte in mV", "Time in ms"])
    threshold = 0.95
    min_peak_distance = 15
    list_of_index_peaks = find_peaks(df_ekg, threshold, min_peak_distance)

    # plot the row["Messwerte in mV"] with the index as x-axis and the peaks as red dots
    fig = px.line(df_ekg, x=df_ekg.index, y="Messwerte in mV", title="EKG Data with Peaks")
    fig.add_scatter(x=list_of_index_peaks, y=df_ekg.iloc[list_of_index_peaks]["Messwerte in mV"], mode='markers', marker=dict(color='red', size=10), name='Peaks')
    fig.update_layout(xaxis_title="Index", yaxis_title="Messwerte in mV")
    fig.show()