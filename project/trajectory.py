class Point:
    def __init__(self, timestamp, latitude, longitude):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude

class Trajectory:
    def __init__(self, points):
