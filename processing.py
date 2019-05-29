"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine
                  learning algorithm. Finally, it calculate the tail angle depending the classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '1.0.0'
__date__ = '2019-05-21'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/' \
             'https://scipy-cookbook.readthedocs.io/items/robust_regression.html' \
             'https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering'

import params
import funciones as fx
import numpy as np
import clusters as grp

# First run
consulta = fx.consulta_acellz(params.startDate, params.endDate, params.cantidad)

cont = 0
tecla = ''
signal_features = []
while cont < len(consulta):
    features = []
    signal, dates = fx.extraer_blob(consulta[cont])
    rec, list_coeff = fx.lowpassfilter(signal, params.thresh, params.wavelet_name)
    popt, pcov = fx.robust_fitting(rec)
    amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
    sine = fx.fundamental(np.linspace(0, len(signal), 540), amplitud, frecuencia, desfase, desplazamiento_y)
    # fx.grafica(signal, cont, rec, sine, params.pwd)
    for coeff in list_coeff:
        features += fx.get_features(coeff)
    signal_features.append(features)
    cont += 1

print('')
