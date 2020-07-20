import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# inspector = inspect(engine)
# inspector.get_table_names()

# columns = inspector.get_columns('measurement')
# for c in columns:
# print(c['name'], c['type'])

# columns = inspector.get_columns('station')
# for column in columns:
# print(column['name'], column['type'])

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f" Hawaii Climate API Surf's Up <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation for the last year."""
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Date and precipitation from last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
    # Create dictionary and jsonify
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Get data on stations
    station_count = session.query(Station.station).all()
    # Make 1D array and turn into a list
    stations = list(np.ravel(station_count))
    # Jsonify results
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def monthlytemperature():
    # Temperature observations
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Calculate for most active station with tobs
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous_year).all()
    # Make 1D array and turn into a list
    temperatures = list(np.ravel(results))
    # Jsonify results
    return jsonify(temperatures=temperatures)


@app.route("/api/v1.0/<start>")
def start(start):
    # Calculate for TMIN, TAVG, TMAX
    # Start
    # Calculate for dates greater than start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    # results = session.query(*sel).\
        # filter(Measurement.date >= dt.date(2016, 10, 17)).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures=temperatures)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Calculate for dates with start and end
    # sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures=temperatures)

if __name__ == '__main__':
    app.run(debug=True)