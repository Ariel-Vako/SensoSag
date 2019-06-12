import pickle
import params
import numpy as np
import clusters as grp

# pc = params.ruta + f'/pc.txt'
# with open(pc, 'wb') as fp:
#     pickle.dump(pca.components_, fp)

pc = params.ruta + '/pc.txt'
with open(pc, 'rb') as fp:
    pc = pickle.load(fp)

señal = params.ruta + f'/signal_features- 2019-01-01 00:00 - 2019-12-30 00:00 : 4000.txt'
with open(señal, 'rb') as fp2:
    signal_feature2019 = pickle.load(fp2)

pwd_grupos = params.ruta + f"/clusters - 2018-08-01 00:00 - 2018-12-30 00:00 : Size 5.txt"
with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

ward = all_cluster

# Aplicar la reducción de dimensión a las caráterísticas de la data de Agosto del 2018.
signal_feature2019 -= np.mean(signal_feature2019)
pc_señal = np.matmul(np.array(signal_feature2019), pc.transpose())
# Agrupar utilizando el clústering de las señales completas.
labels = ward.fit_predict(pc_señal)
# Graficar resultados.
grp.graficar_pca(pc_señal, labels, 5)

print('')

