import pyamg
import params
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans, MiniBatchKMeans, \
    AffinityPropagation, MeanShift, \
    estimate_bandwidth, spectral_clustering, \
    AgglomerativeClustering, DBSCAN, OPTICS, Birch
from sklearn.decomposition import PCA
from itertools import groupby
import matplotlib.pyplot as plt
import sklearn.metrics
from sklearn import preprocessing


def clustering(signal_features, no_cluster=7):
    # kmeans = KMeans(n_clusters=no_cluster, random_state=0).fit(signal_features)
    # mini_kmeans = MiniBatchKMeans(n_clusters=no_cluster, random_state=0, max_iter=10).fit(signal_features)
    # af = AffinityPropagation(preference=-10).fit(signal_features)
    #
    # # --- Mean Shift
    # bandwidth = estimate_bandwidth(signal_features, quantile=0.8)
    # ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    # ms.fit(signal_features)
    # # ms.labels_.max()
    #
    # # --- Spectral Clustering
    # affinity = np.exp(-euclidean_distances(signal_features) / np.std(signal_features))
    # labels_sc = spectral_clustering(affinity, n_clusters=no_cluster, eigen_solver='arpack')

    # --- Agglomerative Clustering - Solo métrica euclidiana
    clustering_ward = AgglomerativeClustering(linkage='ward', n_clusters=no_cluster)
    clustering_ward.fit(signal_features)
    # clustering_average = AgglomerativeClustering(linkage='average', n_clusters=no_cluster)
    # clustering_average.fit(signal_features)
    # clustering_complete = AgglomerativeClustering(linkage='complete', n_clusters=no_cluster)
    # clustering_complete.fit(signal_features)
    # clustering_single = AgglomerativeClustering(linkage='single', n_clusters=no_cluster)
    # clustering_single.fit(signal_features)
    #
    # # --- DBSCAN
    # db = DBSCAN(eps=8, min_samples=6).fit(signal_features)
    #
    # # --- OPTICS
    # optics = OPTICS(min_samples=6, xi=.05, min_cluster_size=.1)
    # optics.fit(signal_features)
    #
    # # --- Birch
    # brc = Birch(branching_factor=100, n_clusters=no_cluster, threshold=20, compute_labels=True)
    # brc.fit(signal_features)
    return clustering_ward
    # [kmeans, mini_kmeans, af, ms, labels_sc, clustering_ward, clustering_average, clustering_complete, clustering_single,
    # db, optics, brc]


def componentes_principales(features):
    # features = preprocessing.normalize(features)
    pca = PCA(n_components=2)
    caract = pca.fit_transform(features)
    return caract, pca


def graficar_pca(matriz, labels, i):
    método = ['KMeans', 'Mini Batch KMeans', 'Affinity Propagation', 'Mean Shift', 'Spectral Clustering', 'Hierarchical clustering: Ward',
              'Hierarchical clustering: Average', 'Hierarchical clustering: Complete', 'Hierarchical clustering: Single',
              'DBSCAN', 'OPTICS', 'Birch']
    x = matriz[:, 0]
    y = matriz[:, 1]

    groups = {'0': {'pos': (5, 5), 'color': (0.267004, 0.004874, 0.329415)},
              '1': {'pos': (15, 55), 'color': (0.229739, 0.322361, 0.545706)},
              '2': {'pos': (-15, -15), 'color': (0.127568, 0.566949, 0.550556)},
              '3': {'pos': (200, -5), 'color': (0.369214, 0.788888, 0.382914)},
              '4': {'pos': (55, 5), 'color': (0.993248, 0.906157, 0.143936)}}

    # morado      : (0.267004, 0.004874, 0.329415)
    # azul        : (0.229739, 0.322361, 0.545706)
    # verde       : (0.127568, 0.566949, 0.550556)
    # verde pasto : (0.369214, 0.788888, 0.382914)
    # amarillo    : (0.993248, 0.906157, 0.143936)

    # etiquetas_agrupadas = [k for k, it in groupby(sorted(labels))]

    fig, ax = plt.subplots(figsize=(14, 10))
    # plt.gcf().canvas.set_window_title(f'Removing high frequency noise with DWT - Cicle {ciclo}')
    scatter = ax.scatter(x, y, c=labels, alpha=0.3)
    ax.set_title(f'PCA: {método[i]}', fontsize=18)
    ax.set_ylabel('PCA2', fontsize=16)
    ax.set_xlabel('PCA1', fontsize=16)
    # ax.set_xlim(-50, 250)
    # ax.set_ylim(-50, 150)
    ax.grid(b=True, which='major', color='#666666')
    ax.grid(b=True, which='minor', color='#999999', alpha=0.4, linestyle='--')
    ax.minorticks_on()

    for label, value in groups.items():
        plt.annotate(label,
                     value['pos'],
                     horizontalalignment='center',
                     verticalalignment='center',
                     size=15,
                     weight='bold',
                     color=value['color'],
                     backgroundcolor='black')

    legend1 = ax.legend(*scatter.legend_elements(), loc="upper right", title="Classes")
    ax.add_artist(legend1)

    plt.show()
    # path = params.ruta + '/gráficas-pca'
    # fig.savefig(f'{path}/{método[i]}.png')
    # plt.close('all')
    return


def métricas(signal_features):
    # kmeans:= 3 cluster - ss=0.92488
    # Mini Batch -Kmeans := 2 cluster - ss= 0.92398
    # Spectral Clustering := 3 - ss= 0.95910

    result = np.empty([8, 4], dtype=float)
    for i in range(2, 10):
        # cluster = KMeans(n_clusters=i, random_state=0).fit(signal_features)

        # cluster = MiniBatchKMeans(n_clusters= i, random_state=0, max_iter=10).fit(signal_features)

        # affinity = np.exp(-euclidean_distances(signal_features) / np.std(signal_features))
        # labels_sc = spectral_clustering(affinity, n_clusters=i, eigen_solver='arpack')

        # clustering_ward = AgglomerativeClustering(linkage='ward', n_clusters=i)
        # cluster = clustering_ward.fit(signal_features)

        # clustering_average = AgglomerativeClustering(linkage='average', n_clusters=i)
        # cluster = clustering_average.fit(signal_features)

        # clustering_complete = AgglomerativeClustering(linkage='complete', n_clusters=i)
        # cluster = clustering_complete.fit(signal_features)

        # clustering_single = AgglomerativeClustering(linkage='single', n_clusters=i)
        # cluster = clustering_single.fit(signal_features)

        brc = Birch(branching_factor=100, n_clusters=i, threshold=20, compute_labels=True)
        cluster = brc.fit(signal_features)

        ss = sklearn.metrics.silhouette_score(signal_features, cluster.labels_, metric='euclidean')
        ch = sklearn.metrics.calinski_harabasz_score(signal_features, cluster.labels_)
        db = sklearn.metrics.davies_bouldin_score(signal_features, cluster.labels_)
        result[i - 2, 0] = np.int(i)
        result[i - 2, 1] = np.round(ss, 3)
        result[i - 2, 2] = np.round(ch, 3)
        result[i - 2, 3] = np.round(db, 3)
        # print(f'Amount of clusters: {i} & Silhouette Score: {np.round(ss, 3)} & Calinski-Harabasz Index: {np.round(ch, 3)}')
    return result

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
# for i in range(len(all_cluster[11].labels_)):
#     if all_cluster[11].labels_[i] == 1 or all_cluster[11].labels_[i] ==2:
#         print(i)

# gof_ward = ruta + "/gof Ward clustering.txt"
# gof_ward = ruta + "/gof Mini Batch Kmeans clustering.txt"
# gof_ward = ruta + "/gof Kmeans clustering.txt"
# gof = ruta + "/gof Spectral Clustering.txt"
# gof = ruta + "/gof Single Clustering.txt"
# gof = ruta + "/gof Birch.txt"
# with open(gof, 'wb') as ward:
#     pickle.dump(resultados, ward)
