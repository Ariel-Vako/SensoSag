"""Gráfica de los cluster en el tiempo desde {start} hasta {n}"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.ticker import MultipleLocator
import pickle
import params
import numpy as np

# Lectura de datos
# 1.- Lectura de cluster para extraer etiquetas.
pwd_grupos = params.ruta + f"/clusters - 2018-08-01 00:00 - 2018-12-30 00:00 : Size 5.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)
# 2.- Lectura de fechas
archivo_train_fechas = params.ruta + '/Fechas/fechas.txt'
# with open(archivo_train_fechas, 'wb') as fn:
#     pickle.dump(fechas, fn)
with open(archivo_train_fechas, 'rb') as fp:
    fechas = pickle.load(fp)


dia = mdates.DayLocator(interval=2)  # Cada 7 días
dia_formato = mdates.DateFormatter('%d %b')
start = 10  # Desde que ciclo se comienza a graficar
n = 20  # número de ciclos a graficar

kolor = all_cluster.labels_
# fechas_aux = [datetime.strftime(i[0], '%d-%m-%Y %H:%M:%S') for i in fechas]
fig, ax = plt.subplots(figsize=(14, 8))

# Formato de ejes
ax.xaxis.set_major_locator(dia)
ax.xaxis.set_major_formatter(dia_formato)
ax.set_xlim([fechas[start] - timedelta(days=1), fechas[n]])
ax.set_title(f'Cluster en el tiempo para {n} ciclos', fontsize=18)
ax.set_ylabel('Grupos', fontsize=16)
ax.set_xlabel('Fechas', fontsize=16)
ax.set_yticks(np.arange(0, 5, step=1))

ax.grid(b=True, which='major', color='#666666')
ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.minorticks_on()

plt.xticks(rotation=45)

scatter = ax.scatter(fechas[start: n], kolor[start: n], c=kolor[start: n], alpha=0.3)
plt.show()
