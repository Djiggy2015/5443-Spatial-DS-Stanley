import scipy
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS # For local requests

import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    print("Main page")
    return render_template('mapbox.html')

@app.route("/token")
def token():
    token = "secret"
    return token

if __name__ == '__main__':
    app.run(debug=True, port=8080)
