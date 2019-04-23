# Using Geopy and Overpass
import geopy.geocoders
from geopy.geocoders import Nominatim
import overpy
import pprint

api = overpy.Overpass()
geopy.geocoders.options.default_timeout = None
geolocator = Nominatim()
pp = pprint.PrettyPrinter()
osm_types_ids = dict()
relevant_tags = dict()

relevant_features = ["amenity", "craft", "historic", "leisure",
"natural", "office", "shop", "sport", "tourism"]

def get_tags_from_stay_points(stay_points):
    for stay_point in stay_points:
        location = geolocator.reverse(str(stay_point.latitude) + ", " + str(stay_point.longitude))
        add_to_types_ids_dict(location.raw["osm_type"], location.raw["osm_id"])
    # pp.pprint(osm_types_ids)
    for osm_type in osm_types_ids:
        ids_string = ""
        for osm_id in osm_types_ids[osm_type]:
            ids_string += str(osm_id) + ","
        ids_string = ids_string[:-1]
        get_tags(osm_type, ids_string)
    # pp.pprint(relevant_tags_dict)
    return relevant_tags

def add_to_types_ids_dict(osm_type, osm_id):
    if osm_type in osm_types_ids:
        osm_types_ids[osm_type].append(osm_id)
    else:
        osm_types_ids[osm_type] = []
        osm_types_ids[osm_type].append(osm_id)

def get_tags(osm_type, ids_string):
    query_string = str(osm_type) + "(id:" + str(ids_string) + ");" + "out body;"
    result = api.query(query_string)
    for way in result.ways:
        # print(way.tags)
        # print(way.tags.get("amenity", "leisure", "n/a"))
        extract_relevant_tags(way.tags)
    for relation in result.relations:
        # print(relation.tags)
        # print(relation.tags.get("amenity", "n/a"))
        extract_relevant_tags(relation.tags)
    for node in result.nodes:
        # print(node.tags)
        # print(node.tags.get("amenity", "n/a"))
        extract_relevant_tags(node.tags)

def extract_relevant_tags(tags):
    for feature in relevant_features:
        if feature in tags:
            tag_string = str(feature) + "-" + str(tags[feature])
            if tag_string in relevant_tags:
                relevant_tags[tag_string] += 1
            else:
                relevant_tags[tag_string] = 1
