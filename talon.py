# -*- coding: utf-8 -*-
import pickle
import numpy as np
import params
import funciones as fx

# Cargar señales filtradas.
ruta = params.ruta + '/respaldo-datos'
signal = ruta + f'/signal_rec_dwt- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(signal, 'rb') as fp2:
    signal_rec = pickle.load(fp2)

pwd_grupos = ruta + f"/clusters - 2018-08-01 00:00 - 2018-12-30 00:00 : Size 5.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

labels = all_cluster.labels_
all_toe = np.zeros(len(signal_rec))
all_time_toe = np.zeros(len(signal_rec))
for i, dwt in enumerate(signal_rec):
    print(f'Etiqueta: {labels[i]}')
    if not labels[i] == 3:
        popt, pcov = fx.robust_fitting(dwt)
        amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
        sine = fx.fundamental(np.linspace(0, len(dwt), 540), amplitud, frecuencia, desfase, desplazamiento_y)
        # Método JS
        raw_impacts = abs(dwt - sine)
        toe, inicio, fin, raw_impacts_ = fx.toe_average(frecuencia, raw_impacts, desfase)
        toe_time = (toe - (desfase * 180 / np.pi)) / (360 * frecuencia)
        fx.plot_ajuste(sine, dwt, inicio, fin, raw_impacts_, toe_time, toe, i)
        print(f'Ciclo {i}: Ángulo {np.round(toe, 1)}')
    else:
        print('Molino detenido')
    all_toe[i] = toe
    all_time_toe[i] = toe_time
print('')
