from load_data import load_data
import numpy as np
import matplotlib.pyplot as plt
from sort import sort_and_invert, invert_array, bubble_sort


#Importiert Daten und speichert diese unter dem Namen expamle_data, speichert die 'PowerOriginal' Spalte seperat unter exapmle_data
example_data_ges = load_data('data/activity.csv')
example_power = example_data_ges['PowerOriginal']
weight = 70
#print(example_data)

# Sortiert die daten und speichert diese unter dem Namen sorted_power
sorted_power = sort_and_invert(example_power)
#print(sorted_power)

# Erstellt ein Diagramm aus den sortierten Daten und speichert dieses unter dem Namen power_curve
time_steps = np.arange(len(sorted_power))
x_ticks = np.arange(0, len(time_steps), step=300)
x_labels = x_ticks // 60



plt.plot(time_steps, sorted_power/weight, color='blue', linewidth=2)
plt.xticks(ticks=x_ticks, labels=x_labels)
plt.grid()
plt.xlabel('Zeit (min)')
plt.ylabel('Leistung pro kg (W/kg)')
plt.title('Leistungskurve 1')
plt.savefig('figures/power_curve.png')