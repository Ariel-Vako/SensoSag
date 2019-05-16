import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def grafica1(grados, z1, sinz, dia, hora, minutos, segundos, magaccel, accelx2, accely2, accelz2, frecfull, i):
    # Crear la figura
    fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
    fig1.suptitle('Gráficas Polares')

    # Subplot 1
    ax1.plot(grados / np.pi * 180 - 90, z1, grados / np.pi * 180 - 90, sinz)
    ax1.grid(b=True, which='major', color='#666666')
    ax1.grid(b=True, which='minor', color='#999999', alpha=0.2)
    ax1.x_lim([-90, 270])
    ax1.y_lim([-3, 3])
    ax1.set(title=f"{dia}, Ago {hora}:{minutos}:{segundos}")
    ax1.xticks(np.linspace(-90, 360, 12, dtype=int))

    # Subplot 2
    ax2.plot(grados / np.pi * 180 - 90, magaccel)
    ax2.grid(b=True, which='major', color='#666666')
    ax2.grid(b=True, which='minor', color='#999999', alpha=0.2)
    ax2.x_lim([-90, 270])
    ax2.y_lim([0, 20])
    ax2.set(title=f"Frecuencia : {frecfull}")
    ax2.xticks(np.linspace(-90, 360, 12, dtype=int))

    # Subplot 3: Polar
    ax3.polar(grados - np.pi / 2, 20 - magaccel)
    ax3.set(title=f"Ciclo : {i}")

    # Subplot 4: Polar
    ax4.polar(grados - np.pi / 2, 20 - accelx2)
    ax4.set(title='Acel Eje X')

    # Subplot 5: Polar
    ax5.polar(grados - np.pi / 2, 20 - accely2)
    ax5.set(title='Acel Eje Y')

    # Subplot 6: Polar
    ax6.polar(grados - np.pi / 2, 20 - accelz2)
    ax6.set(title='Acel Eje Z')

    plt.show()
    return


def grafica2():
    return


def grafica3():
    return
