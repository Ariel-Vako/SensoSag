import numpy as np
import pywt
import matplotlib.pyplot as plt
import MySQLdb
import scipy
import collections


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
    counter_values = collections.Counter(list_values).most_common()
    probabilities = [elem[1] / len(list_values) for elem in counter_values]
    entropy = scipy.stats.entropy(probabilities)
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
    rms = np.nanmean(np.sqrt(list_values ** 2))
    return [n5, n25, n75, n95, median, mean, std, var, rms]


def calculate_crossings(list_values):
    zero_crossing_indices = np.nonzero(np.diff(np.array(list_values) > 0))[0]
    no_zero_crossings = len(zero_crossing_indices)
    mean_crossing_indices = np.nonzero(np.diff(np.array(list_values) > np.nanmean(list_values)))[0]
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


def consulta_acellz(start_date, end_date, cantidad=5000):
    db = MySQLdb.connect("hstech.sinc.cl", "jsanhueza", "Hstech2018.-)", "ssi_mlp_sag2")
    cursor = db.cursor()
    cursor.execute("SELECT dataZ , fecha_reg FROM Data_Sensor WHERE id_sensor_data IN (1) AND estado_data = 134217727 AND fecha_reg BETWEEN %s AND %s ORDER BY fecha_reg ASC LIMIT %s", (start_date, end_date, cantidad))
    results = cursor.fetchall()
    db.close()
    return results


def extraer_blob(datos):
    dates = []
    speeds = []
    hist2d = []
    impacts = []
    toe = []
    toe_std = []
    n = len(datos[0])

    for row in datos:
        sample = []

        for x in range():
            sample.append(float((ord(row[0][x * 2]) << 8) + ord(row[0][x * 2 + 1]) - 2 ** 15) / 2 ** 8)
        # date = row[1]
        dates.append(row[1])

        ######################################################################

        for i in range(len(sample) - 1):
            if i == 0:
                virtual_impacts[i] = np.abs(sample[i])
            else:
                virtual_impacts[i] = np.abs(sample[i - 1] - sample[i])

        ##binarize sample to isolate impactless interval
        impacts_mask = np.where(virtual_impacts > threshold, 0, 1)

        # clip data between 1 [G] and -2 [G] range
        for i in range(len(sample) - 1):
            if sample[i] > 1:
                clipped_data[i] = 0
            elif sample[i] < -2:
                clipped_data[i] = -2
            else:
                clipped_data[i] = sample[i]
    return expanded_blob


def fundamental(reconstructed_signal):
    return  # coseno
