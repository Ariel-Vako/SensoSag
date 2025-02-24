import matplotlib.pyplot as plt
import numpy as np


def grafica1(grados, z1, sinz, dia, hora, minutos, segundos, magaccel, accelx2, accely2, accelz2, frecfull, i):
    # Crear la figura 1
    fig1 = plt.figure()
    fig1.suptitle('Gráficas Polares')

    # Subplot 1
    ax1 = plt.subplot(231)
    ax1.plot(grados / np.pi * 180 - 90, z1, grados / np.pi * 180 - 90, sinz)
    ax1.grid(b=True, which='major', color='#666666')
    ax1.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax1.minorticks_on()
    ax1.set(title=f"{dia}, Ago {hora}:{minutos}:{segundos}")
    ax1.set_xticks(np.linspace(-90, 360, 16, dtype=int))
    ax1.set_xlim(-90, 270)
    ax1.set_ylim(-3, 3)
    ax1.tick_params(axis='both', which='major', labelsize=8)

    # Subplot 2
    ax2 = plt.subplot(232)
    ax2.plot(grados / np.pi * 180 - 90, magaccel)
    ax2.grid(b=True, which='major', color='#666666')
    ax2.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax2.minorticks_on()
    ax2.set(title=f"Frecuencia : {frecfull}")
    ax2.set_xticks(np.linspace(-90, 360, 16, dtype=int))
    ax2.set_xlim(-90, 270)
    ax2.set_ylim(0, 20)
    ax2.tick_params(axis='both', which='major', labelsize=8)

    # Subplot 3: Polar
    ax3 = plt.subplot(233, projection='polar')
    ax3.plot(grados - np.pi / 2, 20 - magaccel)
    ax3.set(title=f"Ciclo : {i}")
    ax3.set_theta_zero_location("N")

    # Subplot 4: Polar
    ax4 = plt.subplot(234, projection='polar')
    ax4.plot(grados - np.pi / 2, 20 - accelx2)
    ax4.set(title='Acel Eje X')
    ax4.set_theta_zero_location("N")
    ax4.set_ylim(0, 50)

    # Subplot 5: Polar
    ax5 = plt.subplot(235, projection='polar')
    ax5.plot(grados - np.pi / 2, 20 - accely2)
    ax5.set(title='Acel Eje Y')
    ax5.set_theta_zero_location("N")
    ax5.set_ylim(0, 50)

    # Subplot 6: Polar
    ax6 = plt.subplot(236, projection='polar')
    ax6.plot(grados - np.pi / 2, 20 - accelz2)
    ax6.set(title='Acel Eje Z')
    ax6.set_theta_zero_location("N")
    ax6.set_ylim(0, 50)

    return


def grafica2(t, x, y, z, zfilt2, cxcascindex, n, grados, x1, sinx, z1, sinz):
    # Crear la figura 2
    fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    # Gráfica de las 3 aceleraciones
    ax1.plot(t, x, t, y, t, z)
    ax1.grid(b=True, which='major', color='#666666')
    ax1.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax1.minorticks_on()
    ax1.tick_params(axis='both', which='major', labelsize=8)

    # Gráfica Aceleración en z y su filtro
    ax2.plot(t, z, t, zfilt2, cxcascindex, np.ones(len(cxcascindex)), '*')
    ax2.set_xlim(min(t), max(t))
    ax2.set_ylim(- 1.5, 1.5)
    ax2.set(title=f"Detectmax: {n}")
    ax2.grid(b=True, which='major', color='#666666')
    ax2.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax2.minorticks_on()

    # Gráfica Aceleración en x y su filtro
    ax3.plot(grados / np.pi * 180 - 90, x1, grados / np.pi * 180 - 90, sinx)
    ax3.grid(b=True, which='major', color='#666666')
    ax3.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax3.minorticks_on()
    ax3.set_xlim(-90, 270)
    ax3.set_ylim(- 1.5, 1.5)
    ax3.set_xticks(np.linspace(-90, 360, 16, dtype=int))

    # Gráfica Aceleración en y, and its filter
    # ax4.plot(grados / np.pi * 180 - 90, y1, grados / np.pi * 180 - 90, siny)
    # ax4.grid(b=True, which='major', color='#666666')
    # ax4.grid(b=True, which='minor', color='#999999', alpha=0.2)
    # ax4.set_xlim([-90, 270])
    # ax4.set_ylim([- 1.5, 1.5])
    # ax4.xticks(np.linspace(-90, 360, 12, dtype=int))

    # Gráfica Aceleración en z y su filtro
    ax4.plot(grados / np.pi * 180 - 90, z1, grados / np.pi * 180 - 90, sinz)
    ax4.grid(b=True, which='major', color='#666666')
    ax4.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax4.minorticks_on()
    ax4.set_xlim(-90, 270)
    ax4.set_ylim(- 1.5, 1.5)
    ax4.set_xticks(np.linspace(-90, 360, 16, dtype=int))

    return


def grafica3(grados, accelz2):
    # Crear la figura 2
    fig3, ax = plt.subplots()

    ax.bar(grados / np.pi * 180 - 90, abs(accelz2))
    ax.grid(b=True, which='major', color='#666666')
    ax.grid(b=True, which='minor', color='#999999', alpha=0.2, linestyle='-')
    ax.minorticks_on()
    ax.set_xlim(90, 180)
    ax.set_ylim(0, 15)
    ax.set(title='Acel Eje Z')

    plt.show()
    return
