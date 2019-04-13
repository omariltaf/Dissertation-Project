class Point:
    def __init__(self, timestamp, latitude, longitude):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return self.timestamp + ", " + self.latitude + ", " + self.longitude

class Trajectory:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return str(self.points)
