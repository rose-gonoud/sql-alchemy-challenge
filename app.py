import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify

# I tossed all the code for my queries into a seperate file, 
from functions import GetDateAndPrecipDict, GetStations, GetTobsData, StartDate

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """Here are all of the available API routes."""
    return (
        "/api/v1.0/precipitation"
        "/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    return GetDateAndPrecipDict(engine, Base)

@app.route("/api/v1.0/stations")
def stations():
    return GetStations(engine, Base)

@app.route("/api/v1.0/tobs")
def tobs():
    return GetTobsData(engine, Base)

@app.route("/api/v1.0/<start>")
def start(start):
    return StartDate(engine, Base, start)

if __name__ == '__main__':
    app.run(debug=True)