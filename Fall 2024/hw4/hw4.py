import os
from csv import DictReader as dr
import numpy as np
from scipy.cluster.hierarchy import dendrogram as dd
import matplotlib.pyplot as plt

# Q3) Model: ChatGPT (GPT-4o), Prompt: implement a tie breaking policy the sorts the distance candidates by the i index and then by the j index
# Q3) Model: ChatGPT (GPT-4o), Prompt: update a distance matrix using single linkage and the minimum distances of the new cluster to the old clusters as they appeared before in the distance matrix
# Q3) Model: ChatGPT (GPT-4o), Prompt: correct my code for the error given by "Index out of range..." 
# Q3) Model: ChatGPT (GPT-4o), Prompt: can this code be made to run faster, such as using a different data type for something

def load_data(filepath):
    with open(os.path.join(filepath), "r") as f:
        file = dr(f)
        data = [row for row in file]
    return data


def calc_features(row):
    array = np.array([row["Population"], row["Net migration"], row["GDP ($ per capita)"], \
                     row["Literacy (%)"], row["Phones (per 1000)"], row["Infant mortality (per 1000 births)"]])
    return array.astype(np.float64)


def hac(features):
    n = len(features)
    clusters = {i: np.array(features[i]) for i in range(n)}  # Convert each item to a numpy array, stored in a dictionary
    merge_hist = []
    cluster_sizes = {i: 1 for i in range(n)}
    active_clusters = set(range(n))  # Track unmerged clusters
    
    # Initialize the distance matrix (distance is Euclidean)
    dismat = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dismat[i, j] = np.linalg.norm(features[i] - features[j])
            dismat[j, i] = dismat[i, j]

    # Set self-distances to infinity so they aren't counted when finding the least distance
    mat = dismat.copy()
    np.fill_diagonal(mat, np.inf)

    cluster_counter = n  # Counter for newly formed clusters
    while len(active_clusters) > 1:
        # Find the minimum distance among active clusters
        min_dist = np.inf
        i_min, j_min = None, None


        for i in active_clusters:
            for j in active_clusters:
                if i < j:  # Only consider i < j to avoid duplicate pairs; make it more efficient
                    distance = mat[i, j]
                    if (distance < min_dist or (distance == min_dist and i < i_min) or (distance == min_dist and i == i_min and j < j_min)):
                        min_dist = distance
                        i_min, j_min = i, j

        if i_min is None or j_min is None:
            break  # No valid pair to merge (was used for error handeling in earlier stages)
        
        # Ensure the pair is (smaller, larger)
        to_merge = (min(i_min, j_min), max(i_min, j_min))
        
        # Merge the clusters
        clusters[cluster_counter] = np.concatenate((clusters[to_merge[0]], clusters[to_merge[1]]))  # Merge clusters
        cluster_sizes[cluster_counter] = cluster_sizes[to_merge[0]] + cluster_sizes[to_merge[1]]

        # Record merge history
        merge_hist.append([to_merge[0], to_merge[1], min_dist, cluster_sizes[cluster_counter]])

        # Expand the distance matrix for the new cluster
        new_mat = np.zeros((cluster_counter + 1, cluster_counter + 1))
        new_mat[:cluster_counter, :cluster_counter] = mat[:cluster_counter, :cluster_counter]  # Copy old distances of previous m x m size
        new_mat[cluster_counter, :] = np.inf  # Initialize new row and column with infinity
        new_mat[:, cluster_counter] = np.inf

        # Update the distance matrix (single linkage: minimum distance)
        for cluster_number in active_clusters:
            if cluster_number != to_merge[0] and cluster_number != to_merge[1]:
                new_dist = min(mat[to_merge[0], cluster_number], mat[to_merge[1], cluster_number])
                new_mat[cluster_counter, cluster_number] = new_mat[cluster_number, cluster_counter] = new_dist
        
        # Mark clusters to_merge[0] and to_merge[1] as inactive by removing them from the set
        active_clusters.remove(to_merge[0])
        active_clusters.remove(to_merge[1])
        active_clusters.add(cluster_counter)

        mat = new_mat  # Update the matrix to the new one
        cluster_counter += 1  # Increment the cluster counter for new clusters to allow indicing as described by piazza
    
    return np.array(merge_hist)

def fig_hac(Z, names):
    dd(Z, labels=names, leaf_rotation = 90, no_plot = False)
    fig= plt.figure()
    return fig

def normalize_features(features):
    means = np.mean(features, axis = 0)
    std = np.std(features, axis = 0)
    mins = np.min(features, axis = 0)
    maxs = np.max(features, axis = 0)

    normalized = (features - mins) / (maxs - mins)
    normal = normalized.tolist()
    return normal