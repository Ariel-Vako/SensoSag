import params
import pickle
import numpy as np

# Lectura de los ángulos del talón
ruta = params.ruta + '/respaldo-datos'
toe_bckup = ruta + f'/toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(toe_bckup, 'rb') as fl:
    all_toe = pickle.load(fl)

# Lectura de etiquetas
etiquetas = ruta + f'/etiquetas- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(etiquetas, 'rb') as fp2:
    labels = pickle.load(fp2)

estadísticos_per_cluster = {}
for i in range(5):
    index = np.where(labels == i)
    sujeto = [all_toe[i] for i in index[0]]
    promedio = np.average(sujeto)
    desv_st = np.std(sujeto)
    estadísticos_per_cluster[f'{i}'] = {'promedio': promedio, 'std': desv_st}
print('')