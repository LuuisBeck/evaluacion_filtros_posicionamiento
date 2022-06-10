import matplotlib.pyplot as plt
import numpy as np
import statistics
from pykalman import KalmanFilter
import copy

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

# Kalman Filter
observation_matrix = np.asarray([[1, 0]])
x = timestamps
dx = [np.mean(np.diff(x))] + list(np.diff(x))
transition_matrices = np.asarray([[[1, each_dx],[0,1]] for each_dx in dx])

# observations
y = np.transpose(np.asarray([values_rssi]))
y = np.ma.array(y)

leave_1_out_cov = []

for i in range(len(y)):
    y_masked = np.ma.array(copy.deepcopy(y))
    y_masked[i] = np.ma.masked

    kf1 = KalmanFilter(transition_matrices = transition_matrices,
                   observation_matrices = observation_matrix)

    kf1 = kf1.em(y_masked)

    leave_1_out_cov.append(kf1.observation_covariance[0,0])

kf1 = KalmanFilter(transition_matrices=transition_matrices,
                    observation_matrices=observation_matrix)
kf1 = kf1.em(y)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(y)


plt.plot(timestamps, values_rssi, 'o', color='grey')
plt.plot(t_average, median_values_rssi, '-', color="green", markersize= 3)
plt.plot(t_average, average_values_rssi, '-', color="red", markersize= 3)
plt.plot(x, smoothed_state_means[:,0], '-', color="blue")
plt.xlabel("time (s)")
plt.ylabel("values RSSI (dB)")
plt.legend(['valor a 1 metro', 'Filtro Mediana', 'Filtro Promedio', 'Filtro Kalman'])

plt.ylim([-100, -30])
plt.show()