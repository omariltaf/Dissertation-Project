from decimal import Decimal

class Point:
    def __init__(self, timestamp, latitude, longitude):
        self.timestamp = str(timestamp)
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    def __str__(self):
        return self.timestamp + ", " + self.latitude + ", " + self.longitude

class Trajectory:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return str(self.points)

    def display(self):
        print("This trajectory has " + str(self.length()) + " points")
        for point in self.points:
            print("Timestamp:" + point.timestamp + " Latitude:" + str(point.latitude) +
                " Longitude:" + str(point.longitude))
