import pickle
import numpy as np

list_gof = [#'gof Average Clustering.text',
            # 'gof Birch.text',
            #'gof Complete Clustering.text',
            'gof Kmeans clustering.text',
            # 'gof Mini Batch Kmeans clustering.text',
            # 'gof Single Clustering.text',
            # 'gof Spectral Clustering.text',
            'gof Ward clustering.text'] # Best Performance

cluster_gof = np.array([[2, 3, 4, 5, 6, 7, 8, 9]]).T
for gof in list_gof:
    with open(gof, 'rb') as f:
        temp = pickle.load(f)
    cluster_gof = np.hstack([cluster_gof, temp[:, 1:4]])

ss = cluster_gof[:, 1: cluster_gof.shape[1]: 3]
ch = cluster_gof[:, 2: cluster_gof.shape[1]: 3]
db = cluster_gof[:, 3: cluster_gof.shape[1]: 3]

print('')
