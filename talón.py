import pickle
import numpy as np
import params
from funciones import robust_fitting, fundamental

# Cargar señales filtradas.
ruta = params.ruta + '/respaldo-datos'
señal = ruta + f'/signal_rec_dwt- {params.startDate} - {params.endDate} : {params.cantidad}.txt'
with open(señal, 'rb') as fp2:
    signal_rec = pickle.load(fp2)

pwd_grupos = ruta + f"/clusters - 2018-08-01 00:00 - 2018-12-30 00:00 : Size 5.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

labels = all_cluster.labels_
for i, dwt in enumerate(signal_rec):
    if not labels[i] == 3:
        popt, pcov = robust_fitting(dwt)
        amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
        sine = fundamental(np.linspace(0, len(dwt), 540), amplitud, frecuencia, desfase, desplazamiento_y)
        # Método JS
        raw_impacts = abs(dwt - sine)
        toe = toe_average(frecuencia, raw_impacts)

    else:
        print('Molino detenido')


def toe_average(frecuencia, raw_impacts):
    periodo = 1 / frecuencia
    j = 0
    while j + periodo <= len(raw_impacts):
        raw_impacts[j] += raw_impacts[int(periodo) + j]
        j += 1

    return toe
