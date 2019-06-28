"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine
                  learning algorithm. Finally, it calculate the tail angle depending the classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '2.0.0'
__date__ = '2019-06-28'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/' \
             'https://scipy-cookbook.readthedocs.io/items/robust_regression.html' \
             'https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering' \
             'https://scikit-learn.org/stable/auto_examples/cluster/plot_inductive_clustering.html#sphx-glr-auto-examples-cluster-plot-inductive-clustering-py'

import params
import funciones as fx
import numpy as np
import pickle
import os.path
import clusters as grp


# First run
ruta = params.ruta
ruta += '/respaldo-datos'
query = ruta + f"/consulta - {params.startDate} - {params.endDate} : {params.cantidad}.txt"
if not os.path.isfile(query):
    consulta = fx.consulta_acellz(params.startDate, params.endDate, params.cantidad)
    with open(query, 'wb') as fp:
        pickle.dump(consulta, fp)

características = ruta + f'/signal_features- {params.startDate} - {params.endDate} : {params.cantidad}.txt'
if not os.path.isfile(características):
    with open(query, 'rb') as fp:
        consulta = pickle.load(fp)

    cont = 0
    tecla = ''
    signal_features = []
    señales = []
    fechas = []
    señal_filtrada = []
    while cont < len(consulta):
        features = []
        signal, dates = fx.extraer_blob(consulta[cont])
        n=len(signal)
        rec, list_coeff = fx.lowpassfilter(signal, params.thresh, params.wavelet_name)

        res_robust = fx.robust_fitting(rec)
        amplitud, frecuencia, desfase, desplazamiento_y = res_robust.x[0], res_robust.x[1], res_robust.x[2], res_robust.x[3]
        sine = fx.fundamental(np.linspace(0, n, n), amplitud, frecuencia, desfase, desplazamiento_y)

        fx.grafica(signal, cont, rec, dates)
        for coeff in list_coeff:
            features += fx.get_features(coeff)
        signal_features.append(features)
        señales.append(signal)
        fechas.append(dates[0])
        señal_filtrada.append(rec)
        cont += 1

    señal_bckup = ruta + f'/signal- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    with open(señal_bckup, 'wb') as fl:
        pickle.dump(señales, fl)

    señal_reconstruida = ruta + f'/signal_rec_dwt- {params.startDate} - {params.endDate}: {params.cantidad}.txt'
    with open(señal_reconstruida, 'wb') as fl:
        pickle.dump(señal_filtrada, fl)

    with open(características, 'wb') as fp:
        pickle.dump(signal_features, fp)

with open(características, 'rb') as fp:
    signal_features = pickle.load(fp)

caract, pca = grp.componentes_principales(signal_features)
print(f'Varianza Explicada: {100 * np.round(np.sum(pca.explained_variance_ratio_), 4)}%')

# Comparativa de resultado y testeo de número de clusters
# resultados = grp.métricas(caract)
# First run
pwd_grupos = ruta + f"/clusters - {params.startDate} - {params.endDate} : Size {params.no_cluster}.txt"
if not os.path.isfile(pwd_grupos):
    all_cluster = grp.clustering(caract, no_cluster=params.no_cluster)
    with open(pwd_grupos, 'wb') as fp2:
        pickle.dump(all_cluster, fp2)

with open(pwd_grupos, 'rb') as fp2:
    all_cluster = pickle.load(fp2)

grp.graficar_pca(caract, all_cluster.labels_, 5)
# for i in range(len(all_cluster)):
#     if i == 4:
#         grp.graficar_pca(caract, all_cluster[i], i)
#     else:
#         grp.graficar_pca(caract, all_cluster[i].labels_, i)
print('')

# INDUCTIVE CLASSIFIER
# Solo una vez para entrenar al Random Forest
# pca_caract = params.ruta + f'/PCA_CARACT - {params.startDate} - {params.endDate} : Size {params.cantidad}.txt'
# with open(pca_caract, 'wb') as fp:
#     pickle.dump(caract, fp)
