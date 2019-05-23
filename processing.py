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
import mysql_query as myz
import params


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
 
def calculate_entropy(list_values):
    counter_values = Counter(list_values).most_common()
    probabilities = [elem[1]/len(list_values) for elem in counter_values]
    entropy=scipy.stats.entropy(probabilities)
    return entropy
 
def calculate_statistics(list_values):
    n5 = np.nanpercentile(list_values, 5)
    n25 = np.nanpercentile(list_values, 25)
    n75 = np.nanpercentile(list_values, 75)
    n95 = np.nanpercentile(list_values, 95)
    median = np.nanpercentile(list_values, 50)
    mean = np.nanmean(list_values)
    std = np.nanstd(list_values)
    var = np.nanvar(list_values)
    rms = np.nanmean(np.sqrt(list_values**2))
    return [n5, n25, n75, n95, median, mean, std, var, rms]
 
def calculate_crossings(list_values):
    zero_crossing_indices = np.nonzero(np.diff(np.array(list_values) &gt; 0))[0]
    no_zero_crossings = len(zero_crossing_indices)
    mean_crossing_indices = np.nonzero(np.diff(np.array(list_values) &gt; np.nanmean(list_values)))[0]
    no_mean_crossings = len(mean_crossing_indices)
    return [no_zero_crossings, no_mean_crossings]
 
def get_features(list_values):
    entropy = calculate_entropy(list_values)
    crossings = calculate_crossings(list_values)
    statistics = calculate_statistics(list_values)
    return [entropy] + crossings + statistics

def get_sensosag_features(ecg_data, ecg_labels, waveletname):
    list_features = []
    list_unique_labels = list(set(ecg_labels))
    list_labels = [list_unique_labels.index(elem) for elem in ecg_labels]
    for signal in ecg_data:
        list_coeff = pywt.wavedec(signal, waveletname)
        features = []
        for coeff in list_coeff:
            features += get_features(coeff)
        list_features.append(features)
    return list_features, list_labels

  
  
def fundamental(reconstructed_signal):
    return coseno

consulta = myz.consulta_acellz(params.startDate, params.endDate, params.cantidad)

data  # Resultado de la query transformada de unicode

#  Split the data between train and test
data_ecg, labels_ecg = load_ecg_data(filename)
training_size = int(0.6*len(labels_ecg))
train_data_ecg = data_ecg[:training_size]
test_data_ecg = data_ecg[training_size:]
train_labels_ecg = labels_ecg[:training_size]
test_labels_ecg = labels_ecg[training_size:]




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
    rec = lowpassfilter(signal, params.thresh, params.wavelet_name)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.
    grafica(signal, cont, rec)  # TODO: SE NECESITA REPROGRAMAR LA FUNCIÓN EN 2D PARA CONSIDERAR EL EJE TIEMPO.

    cont += 1
    tecla = input()
