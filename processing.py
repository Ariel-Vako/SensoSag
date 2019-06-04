"""processing.py: Denoising sensor data with wavelettes (MRA), it collects features to train a machine
                  learning algorithm. Finally, it calculate the tail angle depending the classification"""

__autor__ = 'Ariel Mardones'
__copyright__ = 'Copyright 2019, Highservice'
__credits__ = ['Guillermo Vidal', 'José Sanhueza', 'Ariel Mardones']

__version__ = '1.0.0'
__date__ = '2019-05-21'
__email__ = 'amardones@highservice.cl'

__source__ = 'http://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/' \
             'https://scipy-cookbook.readthedocs.io/items/robust_regression.html' \
             'https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering'

import params
import funciones as fx
import numpy as np
import pickle
import os.path
import clusters as grp

# import msql_analyzer2d as js


# First run
ruta = params.ruta
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
    while cont < len(consulta):
        # print(cont)
        if not (cont == 406 or cont == 1500):  # Se excluyen las señales con mal comportamiento.
            features = []
            signal, dates = fx.extraer_blob(consulta[cont])
            rec, list_coeff = fx.lowpassfilter(signal, params.thresh, params.wavelet_name)

            # popt, pcov = fx.robust_fitting(rec)
            # amplitud, frecuencia, desfase, desplazamiento_y = popt[0], popt[1], popt[2], popt[3]
            # sine = fx.fundamental(np.linspace(0, len(signal), 540), amplitud, frecuencia, desfase, desplazamiento_y)

            # Comparación con resultados de JS
            # p1 = js.process(signal)
            # p1[1] = p1[1] * 0.02
            # sine_js = js.fitfunc(p1, np.linspace(0, len(signal), 540))
            # fx.grafica(signal, cont, rec, sine, params.pwd, sine_js)
            # ----

            # fx.grafica(signal, cont, rec, params.pwd, dates)
            for coeff in list_coeff:
                features += fx.get_features(coeff)
            signal_features.append(features)
        cont += 1

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

for i in range(len(all_cluster)):
    if i == 4:
        grp.graficar_pca(caract, all_cluster[i], i)
    else:
        grp.graficar_pca(caract, all_cluster[i].labels_, i)
print('')
