import pickle
import params
import numpy as np
import csv

archivo_train_fechas = params.ruta + '/Fechas/fechas.txt'
with open(archivo_train_fechas, 'rb') as fp:
    fechas = pickle.load(fp)

ruta = params.ruta + '/respaldo-datos'
toe_bckup = ruta + f'/toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(toe_bckup, 'rb') as fl:
    all_toe = pickle.load(fl)

# all_toe = at.trans_angulo(all_toe)
diccionario_promedio_angulo = {}
j = 0
while j < len(fechas):
    date = fechas[j].date()
    promedio_diario = [all_toe[j]]
    while date == fechas[j + 1].date():
        promedio_diario.append(all_toe[j + 1])
        j += 1
        if j + 1 >= len(fechas):
            break
    j += 1
    alfa_medio = np.round(np.average(promedio_diario), 2)
    diccionario_promedio_angulo[f'{date} 19:00:00'] = alfa_medio

with open(f'{ruta}/test.csv', 'w') as f:
    w = csv.writer(f)
    for key, value in diccionario_promedio_angulo.items():
        w.writerow([key, value])
print('')
