import os
import sys
import json

base_path = "C:\\Users\\Matt\\portofportland"
print(base_path)

from flask import Flask, url_for
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import send_file
import glob

app = Flask(__name__)
CORS(app)

##############################################
##             Data Backend                 ##
##############################################

# Used to work with data backend

stateloc = os.path.join(base_path, 'assets', 'json', 'states.json')

with open(stateloc) as f:
    data = f.read()
STATES = json.loads(data)

cityloc = os.path.join(base_path, 'assets', 'json', 'worldcities.geojson')

# Load city data
with open(cityloc) as f:
    data = f.read()
CITIES = json.loads(data)

railroadloc = os.path.join(base_path, 'assets', 'json', 'us_railroads_with_states.geojson')

# Load railroad data
with open(railroadloc) as f:
    data = f.read()
RAILS = json.loads(data)


#statebbloc = os.path.join(base_path, 'assets', 'json', 'us_state_polygons.geojson')

#with open(statebbloc) as f:
    #data = f.read()
#Bstates = json.loads(data)
#print(STATES)




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
    app.run(port = 8080, debug = True)