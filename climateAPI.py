# 1. import Flask and dependencies
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from operator import itemgetter
from itertools import groupby

#################################################
# 2. Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# 3. reflect an existing database into a new model
Base = automap_base()
# 4. reflect the tables
Base.prepare(engine, reflect=True)

# 5. Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 6. Create our session (link) from Python to the DB
session = Session(engine)

# 7. Create an app, being sure to pass __name__
app = Flask(__name__)

# 8. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to Climate Tracker  API!<br/>"
        f"Available Routes:<br/>"
        f"</br>"
        f"(1)  /api/v1.0/precipitation/StartDate/EndDate  (Date Format = YYYY-MM-DD)<br>"
        f"</br>"
        f"(2)  /api/v1.0/stations<br>"
        
    )


# 9. Get the date and temperature for year 2017
@app.route("/api/v1.0/precipitation/<startDate>/<endDate>")
def getTemperature(startDate,endDate):
    """Return the date and temperateure for 2017"""
    # Query all the date and the temperature details
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= startDate).filter(Measurement.date <= endDate).all()
    # Using iteg getter to declare the sort position. We are sorting by date from the list of tuples
    sortkeyfn = itemgetter(0)
    results.sort(key=sortkeyfn)
    #Create a dictionary
    result = {}
    #Iterate the sorted results after grouping and store the temperture as the values for the key
    for key,valuesiter in groupby(results, key=sortkeyfn):
        result[key] = list(v[1] for v in valuesiter)
    return jsonify(result)

# 10. Return all the station list form the dataset
@app.route("/api/v1.0/stations")
def getStations():
    """Stations List from the dataset"""
    # Query all Stations
    results = session.query(Measurement.station).distinct().all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

if __name__ == "__main__":
    app.run(debug=True)
