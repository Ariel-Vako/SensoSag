"""Random Forest entrenado con el clustering Ward.
Obs.: Recordar quitar la media a la señal filtrada antes de aplicar las componentes principales.
"""

import pickle
import params
import numpy as np
import clusters as grp
# ----------
from sklearn.base import BaseEstimator, clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.metaestimators import if_delegate_has_method


class InductiveClusterer(BaseEstimator):
    def __init__(self, clusterer, classifier):
        self.clusterer = clusterer
        self.classifier = classifier

    def fit(self, X, y=None):
        self.clusterer_ = clone(self.clusterer)
        self.classifier_ = clone(self.classifier)
        y = self.clusterer_.fit_predict(X)
        self.classifier_.fit(X, y)
        return self

    @if_delegate_has_method(delegate='classifier_')
    def predict(self, X):
        return self.classifier_.predict(X)

    @if_delegate_has_method(delegate='classifier_')
    def decision_function(self, X):
        return self.classifier_.decision_function(X)


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
# caract, pca = grp.componentes_principales(signal_feature2019)
signal_feature2019 -= np.mean(np.array(signal_feature2019), axis=0)
pc_señal = np.matmul(signal_feature2019, pc.transpose())
# Agrupar utilizando el clústering de las señales completas.
labels = ward.fit_predict(pc_señal)
# Graficar resultados.
grp.graficar_pca(pc_señal, labels, 5)

# INDUCTIVE CLASSIFIER
pca_caract = params.ruta + f'/PCA_CARACT - {params.startDate} - {params.endDate} : Size {params.cantidad}.txt'
with open(pca_caract, 'rb') as fp2:
    pca_caract = pickle.load(fp2)

classifier = RandomForestClassifier(random_state=10)
inductive_learner = InductiveClusterer(ward, classifier).fit(pca_caract)

probable_clusters = inductive_learner.predict(pc_señal)
print('')
# Guardado del clasificador inductivo (Random Forest)
# clasificador_inductivo = params.ruta + f'/randomForest.txt'
# with open(clasificador_inductivo, 'wb') as fn:
#     pickle.dump(inductive_learner, fn)
