"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine
                  learning algorithm. Finally, it calculate the tail angle depending the classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '1.0.0'
__date__ = '2019-05-21'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/' \
             'https://scipy-cookbook.readthedocs.io/items/robust_regression.html'

import params
import funciones as fx
import numpy as np

consulta = fx.consulta_acellz(params.startDate, params.endDate, params.cantidad)

#  Split the data between train and test
# data_ecg, labels_ecg = load_ecg_data(filename)
# training_size = int(params.tamaño_entrenamiento * len(labels_ecg))
# train_data_ecg = data_ecg[:training_size]
# test_data_ecg = data_ecg[training_size:]
# train_labels_ecg = labels_ecg[:training_size]
# test_labels_ecg = labels_ecg[training_size:]

# Segmentación de señal por intervalos de tiempo coherentes entre ellos

cont = 0
tecla = ''
while cont <= len(consulta) and (tecla == ''):
    signal, dates = fx.extraer_blob(consulta[cont])
    rec = fx.lowpassfilter(signal, params.thresh, params.wavelet_name)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.
    popt = fx.robust_fitting(rec)
    coseno = fx.fundamental(t, amplitud, frecuencia, desfase,  desplazamiento_y)
    fx.grafica(signal, cont, rec, coseno)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.
    cont += 1
    tecla = input()
