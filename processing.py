"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine learning algorithm.
                  Finally, calculate the tail angle depends on classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '1.0.0'
__date__ = '2019-05-21'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/'

import numpy as np
import pywt

data  # Resultado de la query transformada de unicode

tiempo = data['tiempo']
accelz = datosabc['accelz']

# Segmentación de señal por intervalos de tiempo coherentes entre ellos
# Código guillermo

n = len(tiempo)
ciclo = np.array([0])

for i in np.arange(n - 1):
    if (tiempo[i + 1] - tiempo[i]) > 0.1 / 60 / 60 / 24:
        ciclo = np.append(ciclo, [i + 1])

# MRA
waveletname = 'sym5'

for fila_z in accelz:
    signal_z = accelz[fila_z]
    coeffs = pywt.wavedec(signal_z, waveletname, level=7)
