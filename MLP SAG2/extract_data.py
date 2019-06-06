import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt

ruta = os.path.dirname(os.path.realpath(__file__))
sag2 = ruta + "/SAG2_MLP.txt"

# Lectura y guardado de datos csv a través de Pickle
if not os.path.isfile(sag2):
    df = pd.read_csv('SAG2 - Octubre2018.csv',
                     parse_dates=['Fecha'],
                     index_col=['Fecha'])
    with open(sag2, 'wb') as f:
        pickle.dump(df, f)

# Lectura de datos y asignados a un dataframe (Pandas)
with open(sag2, 'rb') as fp:
    df = pickle.load(fp)

# Resumen de NA y Nulos
# df.isna().sum()
# df.isnull().sum()


# create the plot space upon which to plot the data
fig, ax = plt.subplots(figsize=(10, 10))

# add the x-axis and the y-axis to the plot
ax.plot(df.index.values,
        df['REND_2_REAL'])

# rotate tick labels
plt.setp(ax.get_xticklabels(), rotation=45)

# set title and labels for axes
ax.set(xlabel="Fecha",
       ylabel="Temperature (Fahrenheit)",
       title="Precipitation\nBoulder, Colorado in July 2018")

df.plot(kind='scatter', x='Fecha', y='REND_"_REAL')
plt.show()

print('')
