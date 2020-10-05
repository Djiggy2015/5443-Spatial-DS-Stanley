from scipy.spatial import KDTree
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS # For local requests
import os
import geojson

import json

app = Flask(__name__)
CORS(app)

geojcoords = [] # Used to hold our geojson neighbors
citynames = []

def getdata():
    path = 'worldcities.geojson'
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = f.read()
    else:
        print("Data not found!")

    return json.loads(data)

# This function will take the coordinates from the data file and 
# put them into a KDTree. The tree will automatically sort them.
def maketree(data):
    treecoordinates = [] # list of coordinates
    for feature in data["features"]:
        treecoordinates.append(feature["geometry"]["coordinates"])
    mytree = KDTree(treecoordinates) # make the tree.

    return mytree, treecoordinates

# This function will get the name of every city from the 
# properties section of a feature.
def getcitynames(data):
    citynames = []
    for feature in data["features"]:
        citynames.append(feature["properties"]["name"])

    return citynames
# This page will display the map.
@app.route("/")
def index():
    print("Main page")
    return render_template('mapbox.html')

# Will return the token to the front end. 
@app.route("/token")
def token():
    token = 'pk.eyJ1IjoiZGppZ2d5MjAxNSIsImEiOiJja2Z0bW80dmowbzI5MnpzMzI4N2Z0MWZ2In0.Cf21PjpcVqK9tRheXXrJTQ'
    return token

# When the user click on page.
@app.route("/click/")
def click():
    global geojcoords
    clickedcoords = [] # Holds coordinates where user clicked on map.

    # Used to get the coordinates of where the user clicked from 
    # the front end.
    lon, lat = request.args.get("lngLat", None).split(",")

    clickedcoords.append(float(lon))
    clickedcoords.append(float(lat))

    # This query will return the 5 closest neighbors and their distances
    # from the request point. (clickedcoords)
    # Distances is not really used.
    distances, neighbors = mytree.query(clickedcoords, k=5)

    # Make a geojson object that contains the neighbors
    for n in neighbors:
        # Neighbors is basically where in our coordinates list the 
        # neighbor is. So we can use our orignal list of coordinates.
        point = geojson.Point(treecoordinates[n]) # Make a point based off coordinates.
        geojcoords.append(geojson.Feature(geometry=point,properties={'name':citynames[n]}))

    # Store the geojson coordinates into our geojcoords list
    geojcoords = geojson.FeatureCollection(geojcoords) 


    return "User clicked!"

# Make the geojson object created from clicking available for the front end.
@app.route("/neighbors")
def neighbors():
    global geojcoords
    
    # The front end complains when a list is sent, so I convert 
    # the list of geojson features into a dictionary.
    return dict(geojcoords)

if __name__ == '__main__':
    data = getdata()
    mytree, treecoordinates = maketree(data)
    citynames = getcitynames(data)
    app.run(debug=True, port=8080)
