import matplotlib.pyplot as plt
import pickle
import params

señal_bckup = params.ruta + f'/signal- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(señal_bckup, 'rb') as fp:
    pc = pickle.load(fp)

for signal in señal_bckup:
    print(len(signal))
    plt.plot(signal)
