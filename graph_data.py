import matplotlib.pyplot as plt
import numpy as np
import statistics

lines = []
values_rssi = []
t = []
timestamps = []
num_lines = 0

time_milliseconds = 5000    #Tiempo en milisegundos <Ejemplo: 5000 = 5s >

with open('11aq02dZ_1m_2.txt') as file:
    for line in file:
        num_lines += 1
        value_time = line.split(',')
        value = int(value_time[0])
        timestamp = int(value_time[1])
        values_rssi.append(value)
        timestamps.append(timestamp)

t = np.linspace(0, num_lines - 1, num=num_lines)

# Calcular average rssi en 1 segundo
# pensando en que cada valor tiene un timestamp asociado

average_values_rssi = []
t_average = []
median_values_rssi = []

# Calculamos el valor maximo y minimo del timestamp

t_min = np.amin(timestamps)
t_max = np.amax(timestamps)

grouped_timestamps = []
grouped_values = []

while t_min < t_max:
    positions = np.where((timestamps >= t_min) & (timestamps < t_min + time_milliseconds))  # Calculamos las posiciones de los elementos que coinciden en el tiempo establecido
    _timestamp = []
    _values = []
    if(len(positions[0]) > 0):
        for pos in np.nditer(positions):
            _timestamp.append(timestamps[pos])         
            _values.append(values_rssi[pos])
    grouped_timestamps.append(_timestamp)       # agregamos a un array los tiempos agrupados en milisegundos
    grouped_values.append(_values)
    t_min += time_milliseconds

for t in grouped_timestamps:                # calculamos el promedio de los tiempos agrupados
    if(len(t) > 0 ):
        mean = np.mean(t)
        t_average.append(mean)

for value in grouped_values:
    if(len(value) > 0 ):
        mean = np.mean(value)
        median = statistics.median(value)
        average_values_rssi.append(mean)
        median_values_rssi.append(median)


plt.plot(timestamps, values_rssi, 'o')
plt.plot(t_average, median_values_rssi, 'o', color="lime", markersize= 3)
plt.plot(t_average, average_values_rssi, 'o', color="red", markersize= 3)
plt.xlabel("time (s)")
plt.ylabel("values RSSI (dB)")
plt.legend(['valor a 1 metro', 'Filtro Promedio', 'Filtro Mediana'])

plt.ylim([-100, -30])
plt.show()