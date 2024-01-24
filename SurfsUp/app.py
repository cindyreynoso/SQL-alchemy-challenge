# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#instance of the Flask class

app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Convert list of tuples into normal list
    precipitation_data = dict(results)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
   """Return a list of temperature observations for the previous year for the most active station"""
   # Find the most active station
   most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
       group_by(Measurement.station).\
       order_by(func.count(Measurement.station).desc()).first()[0]

   # Query temperature observations for the previous year for the most active station
   results = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.station == most_active_station).\
       filter(Measurement.date >= '2016-08-23').all()
   session.close()

   # Convert list of tuples into normal list
   tobs_data = list(np.ravel(results))
   return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
   """Return temperature statistics for dates greater than or equal to the start date"""
   # Query temperature statistics
   results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start).all()
   session.close()

   # Convert list of tuples into normal list
   temperature_stats = list(np.ravel(results))

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
   """Return temperature statistics for the specified date range"""
   # Query temperature statistics
   results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start).filter(Measurement.date <= end).all()
   session.close()

   # Convert list of tuples into normal list
   temperature_stats = list(np.ravel(results))
   return jsonify(temperature_stats)

if __name__ == '__main__':
    app.run(debug=True)