import pickle
import params
import matplotlib.pyplot as plt

ruta = params.ruta + '/respaldo-datos'
toe_bckup = ruta + f'/toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(toe_bckup, 'rb') as fl:
    all_toe = pickle.load(fl)

time_toe_bckup = ruta + f'/time_toes- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
with open(time_toe_bckup, 'rb') as fl:
    all_time_toe = pickle.load(fl)

fig, ax = plt.subplots(figsize=(12, 8))
# ax.plot(rec, 'k', label='DWT smoothing', linewidth=2)
# ax.plot(raw_impacts_, 'r', label='Distance l1', linewidth=2, alpha=0.5)
# ax.plot(seno2, '--g', label='MCC Robusto', linewidth=1, alpha=0.7)
# ax.legend()
# ax.set_title(f'Ángulo: {np.round(toe, 1)} at {np.round(toe_time, 1)}', fontsize=18)
# ax.set_ylabel('Signal Amplitude', fontsize=16)
# ax.set_xlabel('Time', fontsize=16)
# ax.grid(b=True, which='major', color='#666666')
# ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
# ax.minorticks_on()
# ax.axvspan(inicio, fin - 1, alpha=0.5, color='#98FB98')
plt.plot(all_toe)