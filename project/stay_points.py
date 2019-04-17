from trajectory import Trajectory, Point
from math import radians, sin, asin, cos, sqrt
from datetime import datetime, timedelta
from decimal import Decimal

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
