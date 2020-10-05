# This code was used to filter the coordinates from the major cities in the world.
# The output of this will be worldcities.geojson, which is pretty large (40MB).

import os
import json
import pprint
import copy

path = 'Assignment3/cities.json'
if os.path.isfile(path):
    with open(path, 'r', encoding="utf-8") as f:
         data = f.read()
         data = json.loads(data)
else:
    print("Error: Data was not found!")

newdata = {"type":"FeatureCollection","features":[]}
lonlat = {"type": "Feature", "geometry":{"type": "Point", "coordinates":[]}, "properties":{"name":"none"}}

for item in data:
    # Get the longitude and latitude of each city, name as well.
    lonlat["geometry"]["coordinates"].append(float(item["lng"]))
    lonlat["geometry"]["coordinates"].append(float(item["lat"]))
    lonlat["properties"]["name"] = item["name"]

    # Make a copy that will be added to our dictionary of features.
    newlonlat = copy.deepcopy(lonlat)
    newdata["features"].append(newlonlat)

    # Reset the dictionary so it will be ready to read the next city's info.
    lonlat["geometry"]["coordinates"] = []
    lonlat["properties"]["name"] = " "


# Make our geojson data. Indent 4 makes it look pretty.
jdata = json.dumps(newdata, indent = 4)

# Write our data out to a file.
f = open("worldcities.geojson", "w")
f.write(jdata)
f.close()

        
