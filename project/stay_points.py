from trajectory import Trajectory, Point
from math import radians, sin, asin, cos, sqrt
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class StayPoint:
    def __init__(self, arrival_time, leave_time, latitude, longitude):
        self.arrival_time = arrival_time
        self.leave_time = leave_time
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    def display(self):
        print("Arrival Time:" + self.arrival_time + " Leave Time:" + str(self.leave_time))
        print("Latitude:" + str(self.latitude) + " Longitude:" + str(self.longitude))

def calculate_haversine_distance(point1, point2):
    lat1, long1, lat2, long2 = map(radians, [point1.latitude, point1.longitude, point2.latitude, point2.longitude])
    long_difference = long2 - long1
    lat_difference = lat2 - lat1
    a = sin(lat_difference/2)**2 + cos(lat1) * cos(lat2) * sin(long_difference/2)**2
    c = 2 * asin(sqrt(a))
    R = 6378100 # Radius of Earth in m
    d = R * c
    return d

def calculate_time_span(point1, point2):
    point1_timestamp = datetime.strptime(point1.timestamp, "%Y-%m-%d %H:%M:%S")
    point2_timestamp = datetime.strptime(point2.timestamp, "%Y-%m-%d %H:%M:%S")
    time_delta = point2_timestamp - point1_timestamp
    return time_delta.total_seconds()

# def get_arrival_leave_times(point1, point2):
#     arrival_time = datetime.strptime(point1.timestamp, "%Y-%m-%d %H:%M:%S").time()
#     leave_time = datetime.strptime(point2.timestamp, "%Y-%m-%d %H:%M:%S").time()
#     return arrival_time, leave_time

def calculate_mean_coordinates(points):
    sum_latitude, sum_longitiude = Decimal(0.0), Decimal(0.0)
    num_points = len(points)
    for point in points:
        sum_latitude += point.latitude
        sum_longitiude += point.longitude
    mean_latitude, mean_longitiude = sum_latitude/num_points, sum_longitiude/num_points
    return Decimal(mean_latitude), Decimal(mean_longitiude)

# Parameter Units: Distance in m, Time in minutes
def detect_stay_points(trajectories, distance_thresh, time_thresh):
    stay_points = set() # List of sets each containing stay points for a trajectory
    for trajectory in trajectories:
        i = 0
        points = trajectory.points
        point_num = len(points)
        while i < point_num:
            j = i + 1
            token = 0
            while j < point_num:
                distance = calculate_haversine_distance(points[i], points[j])
                if distance > distance_thresh:
                    time_difference = calculate_time_span(points[i], points[j])
                    if time_difference > (time_thresh * 60):
                        arrival_time, leave_time = points[i].timestamp, points[j].timestamp
                        latitude, longitude = calculate_mean_coordinates(points[i:j + 1])
                        stay_points.add(StayPoint(arrival_time, leave_time, latitude, longitude))
                        i = j
                        token = 1
                    break
                j = j + 1
            if token != 1:
                i = i + 1
    return stay_points

def cluster_stay_points(data):
    print(__doc__)

    import numpy as np

    from sklearn.cluster import DBSCAN
    from sklearn import metrics
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.preprocessing import StandardScaler
    # #############################################################################
    # Generate sample data
    centers = [[1, 1], [-1, -1], [1, -1]]
    X, labels_true = make_blobs(n_samples=750, centers=data, cluster_std=0.4,
                                random_state=0)

    X = StandardScaler().fit_transform(X)

    # #############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=100, min_samples=4).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(labels_true, labels))
    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels))

    # #############################################################################
    # Plot result
    import matplotlib.pyplot as plt

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
