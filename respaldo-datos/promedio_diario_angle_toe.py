import pickle
import params
import numpy as np

archivo_train_fechas = params.ruta + '/Fechas/fechas.txt'
with open(archivo_train_fechas, 'rb') as fp:
    fechas = pickle.load(fp)

promedio_diario = []
