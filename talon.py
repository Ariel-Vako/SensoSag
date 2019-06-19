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
del(signal_rec[0:37])
for i, dwt in enumerate(signal_rec):
    print(f'Etiqueta: {labels[i]}')
    if not labels[i] == 3:
        popt, pcov, res_robust = fx.robust_fitting(dwt)
        # Ajuste mínimo cuadrados normales
        amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
        sine = fx.fundamental(np.linspace(0, len(dwt), 540), amplitud, frecuencia, desfase, desplazamiento_y)
        # Ajuste mínimos cuadrados robustos
        amplitud2, frecuencia2, desfase2, desplazamiento_y2 = res_robust.x[0], res_robust.x[1], res_robust.x[2], res_robust.x[3]
        sine2 = fx.fundamental(np.linspace(0, len(dwt), 540), amplitud2, frecuencia2, desfase2, desplazamiento_y2)

        # Método JS
        raw_impacts = abs(dwt - sine2)
        toe, inicio, fin, raw_impacts_ = fx.toe_average(frecuencia2, raw_impacts, desfase2)
        toe_time = (toe - (desfase2 * 180 / np.pi)) / (360 * frecuencia2)
        fx.plot_ajuste(sine, dwt, sine2, inicio, fin, raw_impacts_, toe_time, toe, i)
        print(f'Ciclo {i}: Ángulo {np.round(toe, 1)}')
    else:
        print('Molino detenido')
    all_toe[i] = toe
    all_time_toe[i] = toe_time
print('')
