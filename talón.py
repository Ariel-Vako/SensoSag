import pickle
import numpy as np
import params
from funciones import robust_fitting, fundamental
import matplotlib.pyplot as plt


def toe_average(frecuencia_, raw_impacts_, delta_theta):
    periodo = 1 / frecuencia_
    j = 0

    while j + periodo <= len(raw_impacts_):
        raw_impacts_[j] += raw_impacts_[int(periodo) + j]
        j += 1
    impactos = []
    t = 0
    inicio = int(np.ceil((np.pi - delta_theta) / (2 * np.pi * frecuencia_)))
    fin = int((3 * np.pi / 2 - delta_theta) / (2 * np.pi * frecuencia_)) + 1
    angulos = 2 * np.pi * frecuencia_ * range(inicio, fin) + delta_theta
    angulos_grad = angulos * 180 / np.pi
    toe = np.average(angulos_grad, weights=raw_impacts_[inicio: fin])
    return toe, inicio, fin, raw_impacts_


def plot_ajuste(seno, señal_rec, inicio, fin, raw_impacts_, toe_time, toe, i):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(seno, "--b", alpha=0.5, label='Seno ajustado')
    rec = señal_rec
    ax.plot(rec, 'k', label='DWT smoothing', linewidth=2)
    ax.plot(raw_impacts_, 'r', label='Suma de señales', linewidth=2, alpha=0.5)
    ax.legend()
    ax.set_title(f'Tiempo del talón {np.round(toe_time, 1)}\n Ángulo: {np.round(toe, 1)}', fontsize=18)
    ax.set_ylabel('Signal Amplitude', fontsize=16)
    ax.set_xlabel('Time', fontsize=16)
    ax.grid(b=True, which='major', color='#666666')
    ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
    ax.minorticks_on()
    ax.axvspan(inicio, fin - 1, alpha=0.5, color='#98FB98')
    plt.axvline(x=toe_time, color='NAVY')
    ax.set_xlim([0, 540])
    # plt.show()
    fig.savefig(f'{params.ruta}/ImágenesToe/Ciclo {i}.png')
    return


# Cargar señales filtradas.
ruta = params.ruta + '/respaldo-datos'
señal = ruta + f'/signal_rec_dwt- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(señal, 'rb') as fp2:
    signal_rec = pickle.load(fp2)

pwd_grupos = ruta + f"/clusters - 2018-08-01 00:00 - 2018-12-30 00:00 : Size 5.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

labels = all_cluster.labels_
all_toe = np.zeros(len(signal_rec))
all_time_toe = np.zeros(len(signal_rec))
for i, dwt in enumerate(signal_rec):
    if not labels[i] == 3:
        popt, pcov = robust_fitting(dwt)
        amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
        sine = fundamental(np.linspace(0, len(dwt), 540), amplitud, frecuencia, desfase, desplazamiento_y)
        # Método JS
        raw_impacts = abs(dwt - sine)
        toe, inicio, fin, raw_impacts_ = toe_average(frecuencia, raw_impacts, desfase)
        toe_time = (toe - (desfase * 180 / np.pi)) / (360 * frecuencia)
        plot_ajuste(sine, dwt, inicio, fin, raw_impacts_, toe_time, toe, i)
        print(f'{i}: {np.round(toe,1)}')
    else:
        print('Molino detenido')
    all_toe[i] = toe
    all_time_toe[i] = toe_time
print('')
