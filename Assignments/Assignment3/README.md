# Assignment 3 - Flask Spatial API
## Matt Stanley
## Description: 
This program uses Flask as a back end API to collect and organize data, and then feed that information into a front end webpage. This webpage will initially use Mapbox 
to generate a Map of the Earth. Next, the user will be able to click somewhere on the map and the five closest cities to that 
point will be determined and shown. A KD-Tree is used in order to determine these five points. I provided two data sets: one of US cities, and one of all cities
in the world. Either one may be used in this program by changing the path name to match that file.

### Files
| #  | File                  | Description                                                                                    |
|:--:|-----------------------|------------------------------------------------------------------------------------------------|
|  1 |kdtree.py              | Main driver of program. Reads in a data file and uses Flask to create webpage.                 |
|  2 |mapbox.html            | Template that Flask will use to create the webpage. Front end code.                            |
|  3 |UScities.geojson       | Orignal geojson data file of major cities. Has unnecessary info.                               |
|  4 |citieslonlat.geojson   | Modified data file. Only contains longitude and latitude of major US cities.                   |
|  5 |cityfilter.py          | File that I used to filter cities.json into worldcities.geojson                                |
|  6 | cities.json (not mine)|https://github.com/lutangar/cities.json/blob/master/cities.json Original world cities data file.|
|  7 |worldcities.geojson    | This was too big to put on github. You can run cityfilter.py on cities.json to make it, though.|  

### Instructions
- Make sure the following python libraries are installed in your environment or wherever you want to run the code: 
     - Flask 
     - Flask-cors 
     -  Scipy 
     -  GeoJson
- Make sure you have all the files listed in the same folder, with your data set of choice.
- In gitbash run the following command in the directory with the listed files: python kdtree.py
- Open a web browser and go to the stated URL: http://127.0.0.1:8080
- Click on the map and the five nearest cities to the point will be shown. (You may need to refresh after clicking.)
- To try another point, you will have to stop the server with ctrl+c and start over.
