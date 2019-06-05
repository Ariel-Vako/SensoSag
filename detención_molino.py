import pickle
import params
import matplotlib.pyplot as plt

ruta = params.ruta
señal_bckup = ruta + f'/signal- {params.startDate} - {params.endDate}.txt'
with open(señal_bckup, 'rb') as fl:
    signal = pickle.load(fl)

pwd_grupos = ruta + f"/clusters - {params.startDate} - {params.endDate} : Size {params.no_cluster}.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

etiquetas = all_cluster[5].labels_

for index, etiqueta in enumerate(etiquetas):
    if etiqueta == 3:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(signal[index])
        ax.grid(b=True, which='major', color='#666666')
        ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
        ax.minorticks_on()
        plt.show()
print('')
