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
import matplotlib.pyplot as plt

def get_data()


def lowpassfilter(signal, thresh=0.63, wavelet="sym7"):
    thresh = thresh * np.nanmax(signal)
    coeff = pywt.wavedec(signal, wavelet, mode="per")
    coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
    return reconstructed_signal


def grafica(signal, ciclo, reconstructed_signal):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(signal, color="b", alpha=0.5, label='original signal')
    rec = reconstructed_signal
    ax.plot(rec, 'k', label='DWT smoothing}', linewidth=2)
    ax.legend()
    ax.set_title('Removing High Frequency Noise with DWT', fontsize=18)
    ax.set_ylabel('Signal Amplitude', fontsize=16)
    ax.set_xlabel(f'Cicle {ciclo}', fontsize=16)
    plt.show()
    return fig


def fundamental(reconstructed_signal):
    return coseno


data  # Resultado de la query transformada de unicode

tiempo = data['tiempo'].values
accelz = data['accelz'].values

# Segmentación de señal por intervalos de tiempo coherentes entre ellos
# Código guillermo

n = len(tiempo)
ciclo = np.array([0])
contador_ciclo = 1

for i in np.arange(n - 1):
    if (tiempo[i + 1] - tiempo[i]) > 0.1 / 60 / 60 / 24:
        contador_ciclo += 1
        ciclo = np.append(ciclo, [i + 1])

cont = 0
while cont <= len(contador_ciclo) and (tecla == ''):
    signal = accelz[cont]
    rec = lowpassfilter(signal, 0.4)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.
    grafica(signal, cont, rec)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.

    cont += 1
    tecla = input()
