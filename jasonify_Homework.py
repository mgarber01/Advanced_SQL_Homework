import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
import datetime as dt 

## Db setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

##session = Session(engine)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)


## setup flask

app = Flask(__name__)

## app routes

@app.route('/')
def home():
    return (
        "<h1> Available Routes </h1>"
        "<h1> /api/v1.0/precipitation </h1>"
        "<h1> /api/v1.0/stations </h1>"
        "<h1> /api/v1.0/tobs </h1>"
        "<h1> /api/v1.0/start </h1>"
        "<h1> Enter start date in Y-M-D format </h1>" 
        "<h1> /api/v1.0/start/end </h1>"
        "<h1>Enter start/end date in Y-M-D format </h1>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    
    date = dt.datetime(2016,8,23)
    precip = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date).all()

    precip_list = []
    for x in precip:
        precip_dict = {}
        precip_dict[x.date] = x.prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)
    

@app.route('/api/v1.0/stations')

def stations():
    station = session.query(Station).all()

    station_list = []
    for x in station:
        station_dict = {}
        station_dict['ID'] = x.id
        station_dict['Station'] = x.station
        station_dict['Station Name'] = x.name 
        station_dict['Latitude'] = x.latitude 
        station_dict['Longitude'] = x.longitude 
        station_dict['Elevation'] = x.elevation 
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    date = dt.datetime(2016,8,23)
    tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date).all()
    tobs_list = []
    for x in tobs:
        tobs_dict = {}
        tobs_dict["Date"] = x.date
        tobs_dict["Temperature"] = x.tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list) 

@app.route('/api/v1.0/<start>')
def starts(start):
    
    TMIN = func.min(Measurement.tobs)
    TAVG = func.avg(Measurement.tobs)
    TMAX = func.max(Measurement.tobs)
    query = session.query(TMIN,TAVG,TMAX,Measurement.date)\
    .filter(func.strftime('%Y-%m-%d',Measurement.date )>= start)\
    .group_by(Measurement.date).all()
    start_list = []
    for x in query: 
        start_dict = {}
        start_dict['TMIN'] = x[0]
        start_dict['TAVG'] = x[1]
        start_dict['TMAX'] = x[2]
        start_dict['Date'] = x[3]
        start_list.append(start_dict)
    return jsonify(start_list)



@app.route('/api/v1.0/<start>/<end>')
def startend(start,end):
    
    TMIN = func.min(Measurement.tobs)
    TAVG = func.avg(Measurement.tobs)
    TMAX = func.max(Measurement.tobs)
    query = session.query(TMIN,TAVG,TMAX,Measurement.date)\
    .filter(func.strftime('%Y-%m-%d',Measurement.date )>= start)\
    .filter(func.strftime('%Y-%m-%d',Measurement.date) <= end).group_by(Measurement.date).all()
    start_list = []
    for x in query: 
        start_dict = {}
        start_dict['TMIN'] = x[0]
        start_dict['TAVG'] = x[1]
        start_dict['TMAX'] = x[2]
        start_dict['Date'] = x[3]
        start_list.append(start_dict)
    return jsonify(start_list)



    
   



if __name__ == '__main__':
    app.run(debug =True)