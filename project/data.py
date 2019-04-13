import csv
import datetime

startDate = []
endDate = []

def read_file(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (line_count < 5):
                print(row[3] + "\t" + row[4])
                if line_count != 0:
                    startDate.append(row[3])
                    endDate.append(row[4])
                line_count += 1;
            else:
                break

        # print(line_count)
        print(startDate)
        print(endDate)

def parse_date():
    for date in startDate:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        print(date_obj.date())

read_file("data/segments.csv")
parse_date()

# Do sortings tings###############################################
