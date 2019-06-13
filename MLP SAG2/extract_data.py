"""Se leen datos desde csv y luego se grafican variables del molino SAG2 : Agosto del 2018"""

__source__ = 'https://matplotlib.org/gallery/api/date.html'

import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dia = mdates.DayLocator(interval=1)  # Cada día
dia_formato = mdates.DateFormatter('%d %b')


ruta = os.path.dirname(os.path.realpath(__file__))
sag2 = ruta + "/SAG2_MLP.txt"

# Lectura y guardado de datos csv a través de Pickle
if not os.path.isfile(sag2):
    misssing_values = ['[-11059] No Good Data For Calculation']
    df = pd.read_csv('SAG2 - Octubre2018.csv',
                     na_values=misssing_values)
    df['Fecha'] = [datetime.strptime(i, '%d-%m-%Y %H:%M:%S') for i in df['Fecha']]
    with open(sag2, 'wb') as f:
        pickle.dump(df, f)

# Lectura de datos y asignados a un dataframe (Pandas)
with open(sag2, 'rb') as fp:
    df = pickle.load(fp)

# create the plot space upon which to plot the data
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df['Fecha'],
        df['REND_2_REAL'])

# Formato de ejes
ax.xaxis.set_major_locator(dia)
ax.xaxis.set_major_formatter(dia_formato)

ax.set_xlim([df['Fecha'][0], df['Fecha'].iloc[-1]])
ax.grid(b=True, which='major', color='#666666')
ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
ax.minorticks_on()

plt.xticks(rotation=45)

# set title and labels for axes
ax.set(xlabel="Fecha",
       ylabel="TPH (ton/h)",
       title="Tonelaje SAG2\nMLP, Agosto 2018")
plt.show()

print('')
