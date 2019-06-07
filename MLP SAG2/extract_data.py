__source__ = 'https://matplotlib.org/gallery/api/date.html'

import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

dia = mdates.DayLocator(interval=1)  # Cada día
# dia_formato = mdates.DateFormatter('%b %d')
minutos = mdates.MinuteLocator(interval=10)  # Cada minuto

ruta = os.path.dirname(os.path.realpath(__file__))
sag2 = ruta + "/SAG2_MLP.txt"

# Lectura y guardado de datos csv a través de Pickle
if not os.path.isfile(sag2):
    misssing_values = ['[-11059] No Good Data For Calculation']
    df = pd.read_csv('SAG2 - Octubre2018.csv',
                     parse_dates=['Fecha'],
                     index_col=['Fecha'],
                     na_values=misssing_values)
    with open(sag2, 'wb') as f:
        pickle.dump(df, f)

# Lectura de datos y asignados a un dataframe (Pandas)
with open(sag2, 'rb') as fp:
    df = pickle.load(fp)

# Resumen de NA y Nulos
# df.isna().sum()
# df.isnull().sum()


# create the plot space upon which to plot the data
fig, ax = plt.subplots(figsize=(10, 15))

# add the x-axis and the y-axis to the plot
# date = np.datetime64(df['Fecha']).astype(datetime)
ax.plot(df.index.values,
        df['REND_2_REAL'])

ax.xaxis.set_major_locator(dia)
# ax.xaxis.set_major_formatter(dia_formato)
ax.xaxis.set_minor_locator(minutos)
ax.grid(b=True, which='major', color='#666666')
ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
ax.minorticks_on()


# set title and labels for axes
ax.set(xlabel="Fecha",
       ylabel="TPH (ton/h)",
       title="Tonelaje\nMLP, Agosto 2018")
plt.show()

print('')
