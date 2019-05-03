# Omar Iltaf
import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import numpy as np
from decimal import Decimal
from stay_points import StayPoint

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

# Clustering algorithm using DBSCAN
def cluster(stay_points):
    list = []
    for stay_point in stay_points:
        list.append([float(stay_point.latitude), float(stay_point.longitude)])
    X = np.array(list)
    clustering = DBSCAN(eps=2/6371, min_samples=5, algorithm="ball_tree", metric="haversine").fit(X)
    labels = clustering.labels_

    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    num_noise = labels.tolist().count(-1)

    clusters = pd.Series([X[labels==n] for n in range(num_clusters)])
    # for index, cluster in clusters.items():
    #     # print(cluster)
    #     write_clustered_points_to_file(cluster, "workingdata/clustered_points_data_CLUSTER" + str(index) + ".txt")
    #     print("Cluster %d with %d points written to file" % (index, len(cluster)))
    return clusters

# Locates centremost points within all clusters
def get_centremost_stay_points(clusters):
    centremost_cluster_points = clusters.map(get_centremost_point)
    centremost_stay_points = set()
    for index, (latitude, longitude) in centremost_cluster_points.items():
        # print("Cluster %d's most central point: %s, %s" % (index, latitude, longitude))
        centremost_stay_points.add(StayPoint(None, None, latitude, longitude))
    return set(centremost_stay_points)

# Helper function for above function
def get_centremost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centremost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centremost_point)

# Writes to a file the coordinates of all points in a cluster
def write_clustered_points_to_file(list, path):
    file = open(path, "w+")
    for latlong_list in list:
        file.write("%s, %s\n" % (latlong_list[0], latlong_list[1]))
