import matplotlib.pyplot as plt
import pickle
import params

señal_bckup = params.ruta + f'/signal- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(señal_bckup, 'rb') as fp:
    señal_bckup = pickle.load(fp)

for signal in señal_bckup:
    print(len(signal))

    fig, ax = plt.subplots(figsize=(14, 10))
    plt.plot(signal)
    ax.grid(b=True, which='major', color='#666666')
    ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
    ax.minorticks_on()
    plt.show()