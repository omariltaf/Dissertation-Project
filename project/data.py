import csv
import datetime
import pprint
from trajectory import Point, Trajectory

pp = pprint.PrettyPrinter()

# Assumes date file has ordered timestamps
def extract_data(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        trajectory_points = dict() # Dictionary of points indexed by date
        trajectories = set() # Set of Trajectory objects to be used in algorithm
        for row in csv_reader:
            if line_count != 0:
                date = str(get_date(row[1]))
                if date not in trajectory_points:
                    trajectory_points[date] = []
                trajectory_points[date].append(Point(row[1], row[2], row[3]))
            line_count += 1
        # pp.pprint(str(trajectory_points["2019-02-24"][0]))
        # pp.pprint(trajectory_points)
        for points in trajectory_points.values():
            trajectories.add(Trajectory(points))
        # pp.pprint(trajectories)
        # print_trajectories(trajectories)
    return trajectories

def get_date(timestamp_str):
    timestamp_obj = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp_obj.date()

def print_trajectories(trajectories):
    print(len(trajectories))
    for trajectory in trajectories:
        pp.pprint(str(trajectory))
