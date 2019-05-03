# Omar Iltaf
import overpy
import pprint
import time
import data
from stay_points import StayPoint

# Allows access to OpenStreetMap data
api = overpy.Overpass()

pp = pprint.PrettyPrinter()

# Approved tag categories (map features)
relevant_features = ["amenity", "craft", "historic", "leisure",
"natural", "shop", "sport", "tourism"]

# Only selects the approved tags
def extract_relevant_tags(relevant_tags, tags):
    relevant_tag_names = data.get_relevant_stay_point_tags()
    for feature in relevant_features:
        if feature in tags:
            if tags[feature] in relevant_tag_names:
                tag_string = str(feature) + "-" + str(tags[feature])
                # tag_string = str(tags[feature])
                if tag_string in relevant_tags:
                    relevant_tags[tag_string] += 1
                else:
                    relevant_tags[tag_string] = 1

# Queries the Overpass API to get OSM tag data
def get_tags_from_stay_points(stay_points):
    relevant_tags = dict()
    for stay_point in stay_points:
        radius = "50"
        latitude, longitude = str(stay_point.latitude), str(stay_point.longitude)
        query_string = "data=[out:json];(node(around:" + radius + "," + latitude + "," + longitude +");"
        query_string += "way(around:" + radius + "," + latitude + "," + longitude +");"
        query_string += "relation(around:" + radius + "," + latitude + "," + longitude +"););out;>;"
        result = api.query(query_string)
        for way in result.ways:
            extract_relevant_tags(relevant_tags, way.tags)
        for relation in result.relations:
            extract_relevant_tags(relevant_tags, relation.tags)
        for node in result.nodes:
            extract_relevant_tags(relevant_tags, node.tags)
    sorted_tags = sorted(relevant_tags, key=relevant_tags.get, reverse=True)[:5]
    results_dict = dict()
    i = 0
    for tag in sorted_tags:
        i += 1
        results_dict["tag_" + str(i)] = str(tag) + ": " + str(relevant_tags[tag])
    return results_dict
