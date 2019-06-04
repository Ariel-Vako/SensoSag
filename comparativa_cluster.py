import pickle

list_gof = ['gof Average Clustering.text',
            'gof Birch.text',
            'gof Complete Clustering.text',
            'gof Kmeans clustering.text',
            'gof Mini Batch Kmeans clustering.text',
            'gof Single Clustering.text',
            'gof Spectral Clustering.text',
            'gof Ward clustering.text']

cluster_gof = []
for gof in list_gof:
    with open(gof, 'rb') as f:
        cluster_gof.append(pickle.load(f))

