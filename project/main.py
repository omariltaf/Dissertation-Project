from data import extract_data
from stay_points import detect_stay_points
import pprint
pp = pprint.PrettyPrinter()

# All trajectories for a user
trajectories = extract_data("mydata/locations.csv")

# All stay points for a user
distance_thresh = 200
time_thresh = 30
stay_points = detect_stay_points(trajectories, distance_thresh, time_thresh)
for stay_point in stay_points:
    stay_point.display()
    print()
print("There are " + str(len(stay_points)) + " Stay Points")
