# Set up Dependencies 
import os.path
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template, redirect, Response
import json
from pprint import pprint

# Flask Setup
app = Flask(__name__)
app.static_folder = 'static'

#Create connection to sql database
connection_string = "postgres:postgres@localhost:5432/final_project"
engine = create_engine(f'postgresql://{connection_string}')

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

@app.route("/dashboard")
def dashboard():
    # 
    map_data = []
    query = """SELECT lat, long, mls_property_type, borough
                FROM public.real_estate"""
    # Open a connection to SQL
    connection = engine.connect()
    # Execute query
    result = engine.execute(query)
    # Append each result to our list
    for row in result:
        map_data.append({
            "lat": row[0],
            "long": row[1],
            "mls_property_type": row[2],
            "borough": row[3]
        })
    # Close the connection
    connection.close()

    # Return template and data
    # Note: follow this example for how to pass into a map
    # https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
    return render_template("dashboard2.html", map_data=map_data)


if __name__ == "__main__":
    app.run(debug=True)
