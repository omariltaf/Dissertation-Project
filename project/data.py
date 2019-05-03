# Omar Iltaf
import mysql.connector
import csv
from datetime import datetime
import pprint
from trajectory import Point, Trajectory

pp = pprint.PrettyPrinter()
# Seta Database credentials
mydb = mysql.connector.connect(
    host="seta-vm1.shef.ac.uk",
    user="testbed_user",
    passwd="Awz2HUYMp8Gkq3cCF",
    database="seta_app_prod"
    )
mycursor = mydb.cursor()

############################################## GETTING DATA FROM MYSQL DATABASE
# Gets all user ids with at least 1000 data entries
def get_user_ids():
    all_user_ids = []
    mycursor.execute("SELECT userID,COUNT(*) FROM locations GROUP BY userID HAVING COUNT(*) > 10000;")
    myresult = mycursor.fetchall()
    counter = 0
    for row in myresult:
        all_user_ids.append(row[0])
    return all_user_ids

def get_user_trajectories(user_id):
    query = "SELECT timestamp, latitude, longitude FROM locations WHERE userID='" + user_id + "';"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    trajectory_points = dict() # Dictionary of points indexed by date
    trajectories = [] # Set of Trajectory objects to be used in algorithm
    for row in myresult:
        date = str(row[0].date())
        if date not in trajectory_points:
            trajectory_points[date] = []
        trajectory_points[date].append(Point(row[0], row[1], row[2]))
    for points in trajectory_points.values():
        trajectories.append(Trajectory(points))
    return trajectories

#################################################### GETTING DATA FROM CSV FILE
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
        for points in trajectory_points.values():
            trajectories.append(Trajectory(points))
    return trajectories

def get_date(timestamp_str):
    timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp_obj.date()

########################################################### DATA FILE HANDLING
def write_stay_points_to_file(stay_points):
    file = open("workingdata/stay_point_data.txt", "a")
    for stay_point in stay_points:
        file.write("%s, %s\n" % (stay_point.latitude, stay_point.longitude))
    print("Stay Points in file")

def create_data_file():
    with open('workingdata/data.csv', mode='w+') as data_file:
        field_names = ['user_id', 'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'num_trajectories', 'num_stay_points', 'num_clusters']
        writer = csv.DictWriter(data_file, fieldnames=field_names)
        writer.writeheader()

def append_to_data_file(data_dict):
    with open('workingdata/data.csv', mode='a') as data_file:
        field_names = ['user_id', 'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'num_trajectories', 'num_stay_points', 'num_clusters']
        writer = csv.DictWriter(data_file, fieldnames=field_names)
        writer.writerow(data_dict)

def get_last_entered_data_row():
    with open("workingdata/data.csv") as data_file:
        reader = csv.reader(data_file, delimiter=',')
        line_count = 0
        for row in reader:
            line_count += 1
        return line_count - 1

def write_user_ids_to_file(user_ids):
    file = open("workingdata/user_ids.txt", "w+")
    for user_id in user_ids:
        file.write("%s\n" % (user_id))
    print(str(len(user_ids)) + " user ids written to file")

def get_user_ids_from_file():
    user_ids = []
    file = open("workingdata/user_ids.txt", "r")
    for line in file:
        user_ids.append(line.strip())
    print(str(len(user_ids)) + " user ids read from file")
    return user_ids

def get_relevant_stay_point_tags():
    relevant_tag_names = set()
    file = open("relevant_tags.txt", "r")
    for line in file:
        relevant_tag_names.add(line.strip())
    return relevant_tag_names
