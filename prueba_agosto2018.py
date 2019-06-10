import pickle
import params
import numpy as np
import clusters as grp

pc = params.ruta + '/pc.txt'
with open(pc, 'rb') as fp:
    pc = pickle.load(fp)

señal = params.ruta + f'/signal_features- {params.startDate} - {params.endDate} : {params.cantidad}.txt'
with open(señal, 'rb') as fp2:
    signal_520agosto2018 = pickle.load(fp2)

pwd_grupos = params.ruta + f"/clusters - {params.startDate} - 2018-12-31 00:00 : Size 5.txt"

with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

ward = all_cluster[5]

# Aplicar la reducción de dimensión a las caráterísticas de la data de Agosto del 2018.
pc_señal = np.matmul(signal_520agosto2018, pc.transpose())
# Agrupar utilizando el clústering de las señales completas.
labels = ward.fit_predict(pc_señal)
# Graficar resultados.
grp.graficar_pca(pc_señal, labels, 5)
print('')
