import pickle
import params
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import numpy as np


def sma(data, periodo):
    sma1 = np.zeros(len(data) - periodo)
    for step in range(len(sma1)):
        sma1[step] = np.mean(data[step:periodo + step + 1])
    return sma1


def trans_angulo(toes):
    angle_toe = []
    for angulo in toes:
        if 0 <= angulo <= 90:
            beta = 90 - angulo
        else:
            beta = abs(450 - angulo)
        angle_toe.append(beta)
    return angle_toe


if __name__ == '__main__':
    ruta = params.ruta + '/respaldo-datos'
    toe_bckup = ruta + f'/toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    with open(toe_bckup, 'rb') as fl:
        all_toe = pickle.load(fl)

    # all_toe = trans_angulo(all_toe)
    #
    # with open(toe_bckup, 'wb') as fp2:
    #     pickle.dump(all_toe, fp2)

    # Lectura del tiempo en el cual se encuentra el talón
    time_toe_bckup = ruta + f'/time_toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    with open(time_toe_bckup, 'rb') as fl:
        all_time_toe = pickle.load(fl)

    # Lectura de etiquetas
    etiquetas = ruta + f'/etiquetas- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    with open(etiquetas, 'rb') as fp2:
        labels = pickle.load(fp2)

    # Guardado de etiquetas
    # ruta = params.ruta + '/respaldo-datos'
    # etiquetas = ruta + f'/etiquetas- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    #
    # with open(etiquetas, 'wb') as fp2:
    #     pickle.dump(labels, fp2)

    # Lectura de fechas de cada señal
    archivo_train_fechas = params.ruta + '/Fechas/fechas.txt'
    with open(archivo_train_fechas, 'rb') as fp:
        fechas = pickle.load(fp)

    dia = mdates.DayLocator(interval=2)
    dia_formato = mdates.DateFormatter('%b%d-%H:%M')
    start = 100  # Desde que ciclo se comienza a graficar
    n = 2000  # número de ciclos a graficar

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.xaxis.set_major_locator(dia)
    ax.xaxis.set_major_formatter(dia_formato)
    ax.set_xlim([fechas[start], fechas[n]])  # - timedelta(days=1)

    ax.grid(b=True, which='major', color='#666666')
    ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.minorticks_on()
    plt.xticks(rotation=45)

    ax.set_ylabel('Angle (°)', fontsize=16)
    ax.set_title(f'Toe Angle', fontsize=18)

    scatter = ax.scatter(fechas[start: n], all_toe[start: n], alpha=0.3)

    periodo = 15
    media_movil = sma(all_toe[start: n + periodo], periodo)

    ax.plot(fechas[start: n], media_movil, c='r')
    plt.show()
    # ax.plot(rec, 'k', label='DWT smoothing', linewidth=2)
    # ax.plot(raw_impacts_, 'r', label='Distance l1', linewidth=2, alpha=0.5)
    # ax.plot(seno2, '--g', label='MCC Robusto', linewidth=1, alpha=0.7)
    # ax.legend()
    # ax.set_title(f'Ángulo: {np.round(toe, 1)} at {np.round(toe_time, 1)}', fontsize=18)
    # ax.set_ylabel('Signal Amplitude', fontsize=16)
    # ax.set_xlabel('Time', fontsize=16)
    # ax.axvspan(inicio, fin - 1, alpha=0.5, color='#98FB98')
