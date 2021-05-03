# Set up Dependencies 
import os.path
import os
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template, redirect, Response, request
import json
from pprint import pprint
from copy import deepcopy
from dotenv import load_dotenv

# Flask Setup
app = Flask(__name__)
app.static_folder = 'static'

#Create connection to sql database
# connection_string = "postgres:postgres@localhost:5432/final_project"
# engine = create_engine(f'postgresql://{connection_string}')
load_dotenv()
my_env_var = os.getenv('DB_CONNECTION_STRING')
engine = create_engine(my_env_var)

# geojson_path = "/Users/shadeetabasi/code/NYC-Challenge-Final/Resources/static/data/nyc_zipcodes.geojson"
geojson_path = "C:/Users/bxprd/Data Analytics Bootcamp/Git_Repos/NYC-Challenge-Final/Resources/static/data/nyc_zipcodes.geojson"
with open(geojson_path, 'r') as f:
    nyc_zipcodes = json.load(f)

#################################################
# Flask Routes
#################################################

# /
# Home page
# List all routes that are available
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/loader")
def loader():
    # 
    
    return render_template("loader.html")

@app.route('/randomForest', methods=['GET', 'POST'])
def randomForest():
    if request.method == "POST":
        db = connection.engine
        req = request.form.get

        compass_property_type = req["compass_property_type"]
        zipcode = req["zipcode"]
        bed = req["bdcount"]
        bath = req["bacount"]
        print("Request", dict(request.form))

        c=db.cursor()
        c.executemany('select * from real_estate_final where compass_property_type = %s''', request.form['search'])
        # return render_template("results.html", )
    return render_template('dashboard.html', records=c.fetchall())

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():

    # Query the user's input fields ... and set defaults to display
    zip_code = request.form.get("zip_code", 10010)
    property_type = request.form.get("property_type", "condo")
    bedrooms = request.form.get("bedrooms", 2)
    baths = request.form.get("baths", 2)
    print("Request", dict(request.form))

    # 
    map_data = deepcopy(nyc_zipcodes)
    query = f"""select avg(sold_price) as price, zipcode from real_estate 
                where bed = {bedrooms} and bath = {baths} 
                group by zipcode
            """

    # Open a connection to SQL
    connection = engine.connect()
    # Execute query and collect price per zipcode
    price_per_zip = {str(row[1]): row[0] for row in engine.execute(query)}
    # Close the connection
    connection.close()

    for feature in map_data["features"]:
        zipcode = feature["properties"]["postalCode"]
        price = price_per_zip.get(zipcode, 0)
        feature["properties"]["avg_price"] = price

    # Return template and data
    # Note: follow this example for how to pass into a map
    # https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
    return render_template("dashboard2.html", map_data=map_data, zip_code=zip_code, baths=baths, bedrooms=bedrooms, property_type = property_type)


if __name__ == "__main__":
    app.run(debug=False)
