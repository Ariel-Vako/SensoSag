import pickle
import os.path
import params


ruta = params.ruta
señal_bckup = ruta + f'/signal- {params.startDate} - {params.endDate}.txt'
with open(señal_bckup, 'rb') as fl:
    signal = pickle.load(fl)

print('')
