from data import extract_data
from stay_points import detect_stay_points, cluster_stay_points
from open_street_map import get_tags_from_stay_points
import pprint

pp = pprint.PrettyPrinter()

def write_to_file(stay_point):
    file = open("stay_point_data.txt", "a")
    file.write("%s, %s\n" % (stay_point.latitude, stay_point.longitude))

# All trajectories for a user
trajectories = extract_data("mydata/locations.csv")

# All stay points for a user
distance_thresh = 200
time_thresh = 30
stay_points = detect_stay_points(trajectories, distance_thresh, time_thresh)
print("There are " + str(len(stay_points)) + " Stay Points")
# stay_points_list = []
# for stay_point in stay_points:
#     # stay_point.display()
#     # print()
#     # write_to_file(stay_point)
#     stay_points_list.append([stay_point.latitude, stay_point.longitude])

# All tags associated with the stay_points
tags = get_tags_from_stay_points(stay_points)
print("There are " + str(len(tags)) + " Tags")
pp.pprint(tags)

# cluster_stay_points(stay_points_list)
