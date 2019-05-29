# Clustering
from sklearn.cluster import KMeans, MiniBatchKMeans, \
    AffinityPropagation, MeanShift, \
    estimate_bandwidth, spectral_clustering, \
    AgglomerativeClustering, DBSCAN, OPTICS, Birch

import pyamg
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances


def clustering(signal_features, no_cluster=4):
    kmeans = KMeans(n_clusters=no_cluster, random_state=0).fit(signal_features)
    mini_kmeans = MiniBatchKMeans(n_clusters=no_cluster, random_state=0, max_iter=10).fit(signal_features)
    af = AffinityPropagation(preference=-500).fit(signal_features)

    # --- Mean Shift
    bandwidth = estimate_bandwidth(signal_features, quantile=0.8)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(signal_features)
    # ms.labels_.max()

    # --- Spectral Clustering
    affinity = np.exp(-euclidean_distances(signal_features) / np.std(signal_features))
    labels_sc = spectral_clustering(affinity, n_clusters=no_cluster, eigen_solver='amg')

    # --- Agglomerative Clustering - Solo métrica euclidiana
    clustering_ward = AgglomerativeClustering(linkage='ward', n_clusters=no_cluster)
    clustering_ward.fit(signal_features)
    clustering_average = AgglomerativeClustering(linkage='average', n_clusters=no_cluster)
    clustering_average.fit(signal_features)
    clustering_complete = AgglomerativeClustering(linkage='complete', n_clusters=no_cluster)
    clustering_complete.fit(signal_features)
    clustering_single = AgglomerativeClustering(linkage='single', n_clusters=no_cluster)
    clustering_single.fit(signal_features)

    # --- DBSCAN
    db = DBSCAN(eps=8, min_samples=6).fit(signal_features)

    # --- OPTICS
    optics = OPTICS(min_samples=6, xi=.05, min_cluster_size=.1)
    optics.fit(signal_features)

    # --- Birch
    brc = Birch(branching_factor=100, n_clusters=no_cluster, threshold=20, compute_labels=True)
    brc.fit(signal_features)
    return kmeans, mini_kmeans, af, ms, labels_sc, clustering_ward, clustering_average, \
           clustering_complete, clustering_single, db, optics, brc

# labels = mini_kmeans.labels_
# labels = kmeans.labels_
# labels = clustering_ward.labels_
# labels = clustering_average.labels_
# labels = clustering_complete.labels_
# labels = clustering_single.labels_
# labels = db.labels_
# labels = optics.labels_
# labels = brc.labels_
# counts = {}
# for label in np.unique(labels):  # (af.labels_):
#     counts[label] = np.count_nonzero(labels == label)
#
# print('Features counts: ', counts)
