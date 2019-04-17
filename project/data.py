import csv
from datetime import datetime
import pprint
from trajectory import Point, Trajectory

pp = pprint.PrettyPrinter()

# Assumes date file has ordered timestamps
def extract_data(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        trajectory_points = dict() # Dictionary of points indexed by date
        trajectories = [] # Set of Trajectory objects to be used in algorithm
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
            trajectories.append(Trajectory(points))
        # pp.pprint(trajectories)
        # print_trajectories(trajectories)
    return trajectories

def get_date(timestamp_str):
    timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp_obj.date()

def print_trajectories(trajectories):
    print(len(trajectories))
    for trajectory in trajectories:
        pp.pprint(str(trajectory))

# def writetofile():
#     trajectories = extract_data("data/locations.csv")
#     file = open("trajdata.txt", "w")
#     dimensions = 2
#     num_trajectories = len(trajectories)
#     file.write("%d\n" % dimensions)
#     file.write("%d\n" % num_trajectories)
#     index = 0
#     for trajectory in trajectories:
#         # print(trajectory.points[0].timestamp)
#         file.write("%d %d" % (index, trajectory.length()))
#         index += 1
#         for point in trajectory.points:
#             file.write(" %f %f" % (point.latitude, point.longitude))
#         file.write("\n")
