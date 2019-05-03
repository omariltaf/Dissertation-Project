# Omar Iltaf
import csv
import pprint

pp = pprint.PrettyPrinter()

tags = dict()
statistics = dict()
statistics["empty_rows"] = 0
statistics["num_trajectories"] = 0
statistics["num_stay_points"] = 0
statistics["num_clusters"] = 0
statistics["num_users"] = 1093

def read_data_csv():
    with open("workingdata/data.csv") as data_file:
        reader = csv.reader(data_file, delimiter=',')
        line_count = 0
        for row in reader:
            line_count += 1
            if line_count == 1:
                continue
            # print(row)
            for i in range(1, 6):
                if row[i] != "":
                    add_to_dict(row[i])
            statistics["num_trajectories"] += int(row[6])
            statistics["num_stay_points"] += int(row[7])
            statistics["num_clusters"] += int(row[8])
            if row[1] == "":
                statistics["empty_rows"] += 1

def add_to_dict(tag):
    separator = ":"
    tag = tag.split(separator, 1)[0]
    if tag in tags:
        tags[tag] += 1
    else:
        tags[tag] = 1

def sort_dict():
    sorted_tags = {k: v for k, v in sorted(tags.items(), key=lambda x: x[1], reverse=True)}
    return sorted_tags

def write_data(sorted_tags):
    with open('results/tags.csv', mode='w+') as data_file:
        writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Tag Name", "Tag Frequency"])
        for tag in sorted_tags:
            writer.writerow([tag, sorted_tags[tag]])

def write_stats():
    with open('results/statistics.csv', mode='w+') as data_file:
        writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Total number of Users:", statistics["num_users"]])
        writer.writerow(["Total number of Users with no Tags Found:", statistics["empty_rows"]])
        writer.writerow([])
        writer.writerow(["Total number of Trajectories:", statistics["num_trajectories"]])
        writer.writerow(["Average number of Trajectories per user:", statistics["num_trajectories"]/statistics["num_users"]])
        writer.writerow([])
        writer.writerow(["Total number of Stay Points:", statistics["num_stay_points"]])
        writer.writerow(["Average number of Stay Points per user:", statistics["num_stay_points"]/statistics["num_users"]])
        writer.writerow([])
        writer.writerow(["Total number of Clusters:", statistics["num_clusters"]])
        writer.writerow(["Average number of Clusters per user:", statistics["num_clusters"]/statistics["num_users"]])

read_data_csv()
sorted_tags = sort_dict()
# print(sorted_tags)
write_data(sorted_tags)
write_stats()
