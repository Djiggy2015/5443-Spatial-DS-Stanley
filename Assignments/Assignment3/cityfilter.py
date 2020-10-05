# This code was used to filter the coordinates from the major us cities 
# geojson file.

import os
import json
import pprint
import copy

path = 'Assignment3/uscities.geojson'
if os.path.isfile(path):
    with open(path, 'r') as f:
         data = f.read()
         data = json.loads(data)
else:
    print("Error: Data was not found!")

newdata = {"type":"FeatureCollection","features":[]}
lonlat = {"type": "Feature", "geometry":{"type": "Point", "coordinates":[]}, "properties":{}}

for feature in data['features']:

    lonlat["geometry"]["coordinates"].append(feature['geometry']['coordinates'][0])
    lonlat["geometry"]["coordinates"].append(feature['geometry']['coordinates'][1])
    newlonlat = copy.deepcopy(lonlat)
    newdata["features"].append(newlonlat)
    lonlat["geometry"]["coordinates"] = []


jdata = json.dumps(newdata, indent = 4)

f = open("citieslonlat.geojson", "w")
f.write(jdata)
f.close()
