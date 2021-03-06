import os
import sys
import json
import geojson


base_path = "C:\\Users\\Matt\\5443-Spatial-DS-Stanley\\Assignments\\Assignment4"
print(base_path)

from flask import Flask, url_for
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import send_file
from scipy.spatial import KDTree
import glob

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

##############################################
##             Data Backend                 ##
##############################################

# Used to work with data backend

stateloc = os.path.join(base_path, 'assets', 'data', 'states.json')

with open(stateloc) as f:
    data = f.read()
STATES = json.loads(data)

cityloc = os.path.join(base_path, 'assets', 'data', 'worldcities.geojson')

# Load city data
with open(cityloc) as f:
    data = f.read()
CITIES = json.loads(data)

volcanoloc = os.path.join(base_path, 'assets', 'data', 'volcanos.geojson')
# Load volcano data
with open(volcanoloc) as f:
    data = f.read()
VOLCANOS = json.loads(data)

railroadloc = os.path.join(base_path, 'assets', 'data', 'us_railroads_with_states.geojson')
# Load railroad data
'''
with open(railroadloc) as f:
    data = f.read()
RAILS = json.loads(data)
'''

#statebbloc = os.path.join(base_path, 'assets', 'json', 'us_state_polygons.geojson')

#with open(statebbloc) as f:
    #data = f.read()
#Bstates = json.loads(data)
#print(STATES)


######################################
# Creating the kd-tree for neighbors #
######################################
def makeTree():
    coordinates = []

    for feature in VOLCANOS['features']:
        coordinates.append(feature["geometry"]["coordinates"])

    tree = KDTree(coordinates)

    return tree, coordinates

###############################################
#              Flask Routes                   #
###############################################

@app.route("/", methods=["GET"])
def getRoutes():
    # gets all the routes

    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes,indent=4,sort_keys=True)
    response = response.replace("\n","<br>")
    return "<pre>"+response+"<pre>"

# Returns a list of US states
@app.route('/states', methods=["GET"])
def states():
    # Takes requests off the URL (things after question mark)
    filter = request.args.get('filter', None)

    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state["name"][:len(filter)].lower():
                results.append(state)
    
    else:
        results = STATES

    return handle_response(results)

# Returns a list of all cities
@app.route('/cities', methods = ["GET"])
def cities():
    # Take request off URL
    filter = request.args.get('filter', None)

    if filter:
        results = []
        for city in CITIES["features"]:
            if filter.lower() == city["properties"]["name"][:len(filter)].lower():
                results.append(city)

    else:
        results = CITIES

    return handle_response(results)

'''
@app.route('/railroads', methods = ["GET"])
def railroads():
    # Take request off URL
    filter = request.args.get('filter', None)

    if filter:
        results = []
        for road in RAILS["features"]:
            if filter in road["properties"]["states"]:
                results.append(road)
    
    # Return an empty list (file is way too big to return everything)
    else:
        results = []

    return handle_response(results)
'''
@app.route('/geodata', methods = ["GET","POST"])
def geodata():
    content = request.get_json()
    print(content)

    content = str(content)

    f = open("demo.txt", 'a')
    f.write(content)
    f.close()
    
    return handle_response(content)

@app.route('/neighbors', methods=["GET"])
def neighbors():
    global tree
    global coordinates

    lon = float(request.args.get('lon',None))
    lat = float(request.args.get('lat',None))
    num = int(request.args.get('num',None))

    search = [lon,lat]

    distances, neighborsList = tree.query(search, k=num, distance_upper_bound = 200)

    neighbors = []

    for i in neighborsList:
        point = geojson.Point(coordinates[i])
        neighbors.append(geojson.Feature(geometry=point))
    neighbors = geojson.FeatureCollection(neighbors)

    return handle_response(neighbors)



###################################
##          Functions             #
###################################

def handle_response(data, params = None, error = None):
    # This function will handle responses

    success = True
    if data:
        # If data is not a list, make it a list
        if not isinstance(data,list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"

    result = {"success":success,"count":count,"results":data,"params":params}

    if error:
        success = False
        result['error'] = error

    return jsonify(result)

def formatHelp(route):
    help = globals().get(str(route)).__doc__
    if help != None:
        help = help.split("\n")
        clean_help = []

        for i in range(len(help)):
            help[i] = help[i].rstrip()
            if len(help[i]) > 0:
                clean_help.append(help[i])

    else:
        clean_help = "No Help."

    return clean_help


def isFloat(string):
    # See if value can be converted into a float.
    # if not, return false, otherwise true.
    try:
        float(string)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    tree, coordinates = makeTree()
    app.run(port = 8080, debug = True)
