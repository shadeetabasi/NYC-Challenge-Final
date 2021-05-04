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
import pickle
# from dotenv import load_dotenv

# Flask Setup
app = Flask(__name__)
app.static_folder = 'static'

model = pickle.load(open('finalized_model.pkl', 'rb'))

features = ['bed', 'bath', 'days_on_market', 'compass_property_type_int',
            'listed_price',
            'dom_outlier', 'walkable_false', 'walkable_true', 'health_level_dead', 'health_level_fair', 'health_level_good',
            'health_level_poor', 'ada_access_no', 'ada_access_yes', 'ada_access_partial', 
            'type_is_active_cleanup_mild_threat','type_is_active_significant_threat','type_is_completed_clean',
            'type_is_maintain_continued_threat', 'type_is_potential_threat', 'type_is_felony', 'type_is_violation', 
            'type_is_misdemeanor', 'danger_level_is_high', 'danger_level_is_low', 'lunch_eligibity_high_false_elem',
            'lunch_eligibity_high_true_elem', 'type_is_top_25th_percentile_elem', 'type_is_50th_percentile_elem',
            'type_is_75th_percentile_elem', 'type_is_bottom_25th_percentile_elem', 'lunch_eligibity_high_false_middle',
            'lunch_eligibity_high_true_middle', 'type_is_top_25th_percentile_middle', 'type_is_50th_percentile_middle',
            'type_is_75th_percentile_middle', 'type_is_bottom_25th_percentile_middle', 'lunch_eligibity_high_false_high',
            'lunch_eligibity_high_true_high', 'type_is_top_25th_percentile_high', 'type_is_50th_percentile_high',
            'type_is_75th_percentile_high', 'type_is_bottom_25th_percentile_high']

# sql_features = [i for i in features if i not in ["days_on_market", "listed_price", "bed"]]
# features.extend(["avg(listed_price) as listed_price", "avg(days_on_market) as days_on_market"])

#Create connection to sql database
connection_string = "postgres:postgres@localhost:5432/final_project"
engine = create_engine(f'postgresql://{connection_string}')
# load_dotenv()
# my_env_var = os.getenv('DB_CONNECTION_STRING')
# engine = create_engine(my_env_var)

geojson_path = "./static/data/nyc_zipcodes.geojson"
with open(geojson_path, 'r') as f:
    nyc_zipcodes = json.load(f)

#################################################
# Flask Routes
#################################################

# /
# Home page
# List all routes that are available

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    disclaimer = ""

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

    # Query the database for all the features in our model for this zipcode
    model_query = "select zipcode, " + ", ".join(features) + f""" from real_estate_final where bed = {bedrooms} and bath = {baths} and zipcode = {zip_code} and compass_property_type = '{property_type}'"""
    model_backup = "select zipcode, " + ", ".join(features) + f""" from real_estate_final where zipcode = {zip_code}"""

    # Open a connection to SQL
    connection = engine.connect()
    # Execute query and collect price per zipcode
    price_per_zip = {str(row[1]): row[0] for row in engine.execute(query)}
    
    model_data = [i for i in engine.execute(model_query)]
    if len(model_data) == 0:
        model_data = [i for i in engine.execute(model_backup)]
        disclaimer = "Not enough properties available to model your query. This is the average price for the selected zipcode."

    # Close the connection
    connection.close()

    # Engineer the features for the model
    df = pd.DataFrame(model_data, columns=["zipcode"] + features )
    # Since the database returned multiple rows for this data, take the avg of all fields (eg listed_price, days_on_market)
    X = df.groupby("zipcode").mean()
    # Prediction
    predicted_price = model.predict(X)[0]

    # Build map data
    for feature in map_data["features"]:
        zipcode = feature["properties"]["postalCode"]
        price = price_per_zip.get(zipcode, 0)
        feature["properties"]["avg_price"] = price

    

    # Return template and data
    # Note: follow this example for how to pass into a map
    # https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
    return render_template("dashboard2.html", map_data=map_data, zip_code=zip_code, baths=int(baths), bedrooms=int(bedrooms), property_type = property_type, predicted_price = predicted_price, disclaimer=disclaimer)

@app.route("/realestate")
def realestate():

    return render_template("housing_table.html")

@app.route("/crimes")
def crimes():

    return render_template("crime_table.html")

@app.route("/brownfields")
def brownfields():

    return render_template("brownfields_table.html")

@app.route("/elementaryschools")
def elementaryschools():

    return render_template("elem_table.html")

@app.route("/middleschools")
def middleschools():

    return render_template("middle_table.html")

@app.route("/highschools")
def highschools():

    return render_template("high_table.html")

@app.route("/subwaystations")
def subwaystations():

    return render_template("stations_table.html")

@app.route("/restaurants")
def restaurants():

    return render_template("restaurants_table.html")

@app.route("/trees")
def trees():

    return render_template("trees_table.html")

@app.route("/walkability")
def walkability():

    return render_template("walk_table.html")


if __name__ == "__main__":
    app.run(debug=False)
