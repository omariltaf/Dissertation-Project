from trajectory import Point, Trajectory
import math
import numpy as np
from decimal import Decimal

def trajectory_partitioning(trajectory):
    characteristic_points = set()
    characteristic_points.add(trajectory.points[0])
    start_index = 0
    length = 1
    counter = 0
    # Looping over every point in trajectory
    while (start_index + length) < trajectory.length():
        # print()
        # print(counter)
        current_index = start_index + length
        cost_par = mdl_par(trajectory, start_index, current_index)
        cost_nopar = mdl_nopar(trajectory, start_index, current_index)
        # print(cost_par)
        # print(cost_nopar)

        if cost_par > cost_nopar:
            # print("haah")
            characteristic_points.add(trajectory.points[current_index - 1])
            start_index = current_index - 1
            length = 1
        else:
            # print("lool")
            length = length + 1
        counter += 1
    characteristic_points.add(trajectory.points[trajectory.length() - 1])
    return characteristic_points


def mdl_par(trajectory, start_index, current_index):
    # print("start_index="+str(start_index) + " current_index="+str(current_index))
    start_point = trajectory.points[start_index]
    current_point = trajectory.points[current_index]
    euclidean_distance = calc_euclidean_distance(start_point, current_point)
    if euclidean_distance < 1.0:
        euclidean_distance = 1.0
    hypothesis = math.log2(euclidean_distance)

    segment_start_index = start_index
    segment_end_index = start_index + 1
    total_perpendicular_distance = 0
    total_angular_distance = 0
    while segment_end_index <= current_index:
        segment_start_point = trajectory.points[segment_start_index]
        segment_end_point = trajectory.points[segment_end_index]
        perpendicular_distance = calc_perpendicular_distance(start_point, current_point,
                                        segment_start_point, segment_end_point)
        angular_distance = calc_angular_distance(start_point, current_point,
                                        segment_start_point, segment_end_point)
        if perpendicular_distance == 0:
            # print("perp:"+str(perpendicular_distance))
            perpendicular_distance = 1.0
        if angular_distance == 0:
            # print("ang:"+str(angular_distance))
            angular_distance = 1.0

        total_perpendicular_distance += perpendicular_distance
        total_angular_distance += angular_distance
        segment_start_index += 1
        segment_end_index += 1
    # print(total_perpendicular_distance)
    encoding = math.log2(total_perpendicular_distance) + math.log2(total_angular_distance)
    return hypothesis + encoding

def mdl_nopar(trajectory, start_index, current_index):
    start_point = trajectory.points[start_index]
    current_point = trajectory.points[current_index]
    euclidean_distance = calc_euclidean_distance(start_point, current_point)
    if euclidean_distance < 1.0:
        euclidean_distance = 1.0
    hypothesis = math.log2(euclidean_distance)
    return hypothesis

def calc_euclidean_distance(start_point, end_point):
    squared_latitude = math.pow(end_point.latitude - start_point.latitude, 2)
    squared_longitiude = math.pow(end_point.longitude - start_point.longitude, 2)
    return math.sqrt(squared_latitude + squared_longitiude)

def calc_angular_distance(s1, e1, s2, e2):
    (shorter_s, shorter_e, longer_s, longer_e) = find_shorter_and_longer_lines(s1, e1, s2, e2)
    shorter_vector = Point(0, shorter_e.latitude - shorter_s.latitude, shorter_e.longitude - shorter_s.longitude)
    longer_vector = Point(0, longer_e.latitude - longer_s.latitude, longer_e.longitude - longer_s.longitude)
    shorter_vector_square_sum = math.pow(shorter_vector.latitude, 2) + math.pow(shorter_vector.longitude, 2)
    longer_vector_square_sum = math.pow(longer_vector.latitude, 2) + math.pow(longer_vector.longitude, 2)
    shorter_vector_length = math.sqrt(shorter_vector_square_sum)
    longer_vector_length = math.sqrt(longer_vector_square_sum)
    if shorter_vector_length == 0.0 or longer_vector_length == 0.0:
        return 0.0

    inner_product = (shorter_vector.latitude * longer_vector.latitude) + (shorter_vector.longitude * longer_vector.longitude)
    cos_theta = inner_product / Decimal(shorter_vector_length * longer_vector_length)
    if cos_theta > 1.0:
        cos_theta = 1.0
    if cos_theta < -1.0:
        cos_theta = -1.0
    sin_theta = math.sqrt(1 - math.pow(cos_theta, 2))
    return shorter_vector_length * sin_theta

# Parameters are start/end points forming two line segments
def calc_perpendicular_distance(s1, e1, s2, e2):
    # Determines which line segment is shorter to know which line should project onto the other
    (shorter_s, shorter_e, longer_s, longer_e) = find_shorter_and_longer_lines(s1, e1, s2, e2)

    distance_s = calc_point_to_line_distance(shorter_s, longer_s, longer_e)
    distance_e = calc_point_to_line_distance(shorter_e, longer_s, longer_e)
    if distance_s == 0.0 and distance_e == 0.0:
        return 0.0
    top = math.pow(distance_s, 2) + math.pow(distance_e, 2)
    bottom = distance_s + distance_e
    if bottom == 0.0:
        return 0.0
    return Decimal(top) / Decimal(bottom)

def calc_point_to_line_distance(s1, s2, e2):
    (x0, x1, x2) = (s1.latitude, s2.latitude, e2.latitude)
    (y0, y1, y2) = (s1.longitude, s2.longitude, e2.longitude)
    top = abs((y2 - y1) * x0 - (x2 - x1) * y0 + (x2 * y1) - (y2 * x1))
    bottom = math.sqrt(math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2))
    if bottom == 0.0:
        return 0
    return Decimal(top)/Decimal(bottom)

def find_shorter_and_longer_lines(s1, e1, s2, e2):
    line_length_1 = calc_euclidean_distance(s1, e1)
    line_length_2 = calc_euclidean_distance(s2, e2)
    if (line_length_1 < line_length_2):
        return (s1, e1, s2, e2)
    else:
        return (s2, e2, s1, e1)
