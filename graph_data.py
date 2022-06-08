from os import times_result
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import statistics

lines = []
values_rssi = []
t = []
timestamps = []
num_lines = 0

with open('11aq02dZ_1m_2.txt') as file:
    for line in file:
        num_lines += 1
        value_time = line.split(',')
        value = int(value_time[0])
        timestamp = int(value_time[1])
        #TODO: falta tomar datos de timestamp
        values_rssi.append(value)
        timestamps.append(timestamp)

t = np.linspace(0, num_lines - 1, num=num_lines)

# Calcular average rssi en 1 segundo
# pensando en que cada valor tiene un timestamp asociado
average_values_rssi = []
t_average = np.linspace(0, (num_lines - 1), num=int(num_lines/5))

counting = 0
average = 0
for value in values_rssi:
    counting += 1
    average += value
    if counting == 5:
        counting = 0
        average = average / 5
        average_values_rssi.append(average)
        average = 0

counting = 0
median_list = []
median_values_rssi = []
for value in values_rssi:
    counting += 1
    median_list.append(value)
    if counting == 5:
        counting = 0
        median = statistics.median(median_list)
        median_values_rssi.append(median)
        median_list = []

plt.plot(timestamps, values_rssi, 'o')
#plt.plot(t_average, average_values_rssi, 'o', color="red", markersize= 3)
#plt.plot(t_average, median_values_rssi, 'o', color="lime", markersize= 3)
plt.xlabel("time (s)")
plt.ylabel("values RSSI (dB)")
plt.legend(['valor a 1 metro', 'Filtro Promedio', 'Filtro Mediana'])

plt.ylim([-100, -30])
plt.show()


