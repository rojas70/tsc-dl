import IPython
import numpy as np
import matplotlib.pyplot as plt
from sklearn import (manifold, datasets, decomposition, ensemble, lda,
	random_projection, preprocessing, covariance, cluster, neighbors)
import utils

def encode_cluster_normalize(X):
	return encode_VLAD(X, 1, 5)

def difference_vectors(X, cluster_predictions, clusters_centers):
	PC = X.shape[1]
	K = len(clusters_centers)
	u_k = {}
	num_frms = X.shape[0]
	for frm in range(num_frms):
		frm_NN_cluster = cluster_predictions[frm]
		c = clusters_centers[frm_NN_cluster]
		diff = X[frm] - c
		if frm_NN_cluster not in u_k:
			u_k[frm_NN_cluster] = diff
		else:
			sum_k = u_k[frm_NN_cluster]
			sum_k += diff
			u_k[frm_NN_cluster] = sum_k
	vlad = u_k[0]
	for k in range(1, K):
		vlad = np.concatenate((vlad, u_k[0]), axis = 1)
	vlad = preprocessing.normalize(vlad, norm = 'l2')
	# return vlad.reshape(1, vlad.shape[0])
	return vlad

def encode_VLAD(X, K):
	# X_pca = pca(X, PC = PC)

	kmeans = cluster.KMeans(init = 'k-means++', n_clusters = K)
	kmeans.fit(X)
	clusters_centers = kmeans.cluster_centers_
	assert len(clusters_centers) == K

	neigh = neighbors.KNeighborsClassifier(n_neighbors = 1)
	Y = np.arange(K)
	neigh.fit(clusters_centers, Y)
	cluster_predictions = neigh.predict(X)
	assert len(cluster_predictions) == X.shape[0]

	return difference_vectors(X, cluster_predictions, clusters_centers)

