"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine
                  learning algorithm. Finally, it calculate the tail angle depending the classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '1.0.0'
__date__ = '2019-05-21'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/'

import numpy as np
import pywt


def lowpassfilter(signal, thresh=0.63, wavelet="sym7"):
    thresh = thresh * np.nanmax(signal)
    coeff = pywt.wavedec(signal, wavelet, mode="per")
    coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
    return reconstructed_signal


data  # Resultado de la query transformada de unicode

tiempo = data['tiempo']

# Segmentación de señal por intervalos de tiempo coherentes entre ellos
# Código guillermo

n = len(tiempo)
ciclo = np.array([0])

for i in np.arange(n - 1):
    if (tiempo[i + 1] - tiempo[i]) > 0.1 / 60 / 60 / 24:
        ciclo = np.append(ciclo, [i + 1])
