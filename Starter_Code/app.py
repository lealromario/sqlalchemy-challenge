#!/usr/bin/env python
# coding: utf-8

# In[7]:


# Import the dependencies
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect


from flask import Flask, jsonify


# In[ ]:


#################################################
# Database Setup
#################################################


# In[8]:


# Create the engine
path = r"C:\Users\lealr\OneDrive\Desktop\sqlalchemy_challenge\Starter_Code\Resources\hawaii.sqlite"
engine = create_engine(f"sqlite:///{path}")
connection = engine.connect()


# In[9]:


# Printing the available tables
inspector = inspect(engine)
table_names = inspector.get_table_names()
print(table_names)


# In[10]:


# Create a base
# reflect an existing database into a new model
Base = automap_base()

Base.prepare(engine, reflect=True)


# In[11]:


# Saving measurement and station tables in the database
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[ ]:


#################################################
# Flask Setup
#################################################


# In[12]:


# The Flask startup
app = Flask(__name__)


# In[ ]:


#################################################
# Flask Routes
#################################################


# In[13]:


# Flask root route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Convert the query results for the past 12 months from the precipitation analysis to a dictionary using date as the key and prcp as the value"""
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").    filter(Measurement.date <= "2017-08-23").    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Return the JSON of the dictionary
    prcp_data = {date: prcp for date, prcp in prcp_data}

    return jsonify(prcp_data)


# In[ ]:


@app.route("/api/v1.0/stations")
def station():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    stations_data = session.query(Station.station).    order_by(Station.station).all()

    # Close Session
    session.close()

    total_stations = list(np.ravel(stations_data))

    return jsonify(total_stations)


# In[ ]:


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    previous = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).    filter(Measurement.station == "USC00519281").filter(Measurement.date >= previous).all()

    # Close Session
    session.close()

    # Return a JSON list of temperature observations for the previous year.
    total_tobs = []
    for date, tobs, prcp in results:
        result_dict = {}
        result_dict["date"] = date
        result_dict["prcp"] = prcp
        result_dict["tobs"] = tobs
        total_tobs.append(result_dict)

    return jsonify(total_tobs)


# In[ ]:


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_tobs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Close Session
    session.close()

    start_tobs_list = []
    for min, max, avg in start_tobs:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        start_tobs_list.append(start_dict)
    return jsonify(start_tobs_list)


# In[ ]:


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    start_end_data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Close Session
    session.close()

    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    start_end_list = []
    for min, max, avg in start_end_data:
        start_end_dict = {}
        start_end_dict["minimum"] = min
        start_end_dict["Average"] = avg
        start_end_dict["Max"] = max
        start_end_list.append(start_end_dict)
    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:





# In[ ]:




