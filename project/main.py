# Omar Iltaf
import pprint
import csv
import data
from stay_points import detect_stay_points
from open_street_map import get_tags_from_stay_points
from stay_points_cluster import cluster, get_centremost_stay_points

pp = pprint.PrettyPrinter()

# Gets list of user ids either from server or stored text file
# data.create_data_file()
# user_ids = data.get_user_ids()
# data.write_user_ids_to_file(user_ids)
user_ids = data.get_user_ids_from_file()

# Keeps track of last position in data file to carry on where it left off
# last_index = data.get_last_entered_data_row()
last_index = 0
current_user_id_index = last_index

# Main Algorithm
for user_id in user_ids[last_index:]:
    current_user_id_index+=1
    print(current_user_id_index)

    # Get all trajectories for a user
    trajectories = data.get_user_trajectories(user_id)

    # Get all stay points for a user
    distance_thresh, time_thresh = 100, 20
    stay_points = detect_stay_points(trajectories, distance_thresh, time_thresh)
    if len(stay_points) != 0:
        clusters = cluster(stay_points)
        centremost_stay_points = get_centremost_stay_points(clusters)
        # data.write_stay_points_to_file(stay_points)

        # Get all tags for a user
        tags = get_tags_from_stay_points(centremost_stay_points)
        tags["user_id"] = "user_" + str(current_user_id_index)
        tags["num_trajectories"] = len(trajectories)
        tags["num_stay_points"] = len(stay_points)
        tags["num_clusters"] = len(centremost_stay_points)
        pp.pprint(tags)
        # data.append_to_data_file(tags)
    else:
        tags = {"user_id":"user_" + str(current_user_id_index), "num_trajectories":len(trajectories),
        "num_stay_points":0, "num_clusters":0}
        pp.pprint(tags)
        # data.append_to_data_file(tags)
