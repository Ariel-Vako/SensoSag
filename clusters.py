# Clustering
from sklearn.cluster import KMeans, MiniBatchKMeans, AffinityPropagation, MeanShift


def clustering(signal_features, no_cluster=4):
    kmeans = KMeans(n_clusters=no_cluster, random_state=0).fit(signal_features)
    mini_kmeans = MiniBatchKMeans(n_clusters=no_cluster, random_state=0, max_iter=10).fit(signal_features)
    af = AffinityPropagation(preference=-50).fit(signal_features)
    return kmeans, mini_kmeans, af
