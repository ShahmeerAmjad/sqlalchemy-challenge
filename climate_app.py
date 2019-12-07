#import dependecies
import numpy as np 
import pandas as pd
import sqlalchemy
import datetime
from flask import Flask,jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#initialize database connection

engine= create_engine("sqlite:///hawaii.sqlite",echo=False)
Base= automap_base()
Base.prepare(engine, reflect=True)


##Create references to the Measurement and Station Tables

Measurement=Base.classes.measurement()
Station=Base.classes.station()

session=Session(engine)

#initialize Flask app

app= Flask(__name__)


##Set Flask Routes

@app.route("/")
def homepage():
           """Welcome to the Home page!."""
           return(
               f"(Note: The dataset contatins observations from 1st January2010 to August 23th 2017).<br><br>"
                f"Available Routes: <br>"

                f"/api/v1.0/precipitation<br/>"
                f"Returns dates and precipation from the last year. <br><br>"

                f"/api/v1.0/stations<br/>"
                f"Returns a json list of all the  stations. <br><br>"

                f"/api/v1.0/temperature<br/>"
                f"Returns list of Temperature observations(tobs) for previous year. <br><br>"

                f"/api/v1.0/yyyy-mm-dd/<br/>"
                f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"

                f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
                f"Returns an Average, Max, and Min temperatures for a given date range.")
           
@app.route("/api/v1.0/precipitation")
def precipitation():         
            """Returns Dates and precipitation from the last year"""
            results=session.query(Measurement.date,Measurement.tobs).\
                filter(Measurement.date<="2017,08-23",Measurement.date>="2016-08-24").all()
           #generates JSON list
            precipitation_list=[results]
           
            return jsonify(precipitation_list)
           
@app.route("/api/v1.0/stations")         
def stations():
           """Return a list of stations"""
           results=session.query(Station.statation,Station.name,Station.elevation).all()
           
           #generates JSON list of dicts
           
           station_list=[]
            for result in results:
                row={}
                row['station']=result[0]
                row['name']=result[1]
                row['elevation']=result[2]

               #Append to array
                station_list.append(row)
           
           return jsonify(station_list)
          
@app.route("/api/v1.0/temperature")
           
def tobs():
            """Returns a list of temperatutes for the previous year"""
            results=session.query(Station.name,Measurement.date,Measurement.tobs).\
                filter(Measurement.date<="2017,08-23",Measurement.date>="2016-08-24") .all()
      
           #generates JSON list of dicts
           
            tobs_list=[]
            for result in results:
                row={}
                row["Station"]=result[0]
                row["Date"]=result[1]
                row["Temperature"]=result[2]
                #Append to attay
                tobs_list.append(row)

@app.route("/api/v1.0/<start>")

def startdate(date):
    """Returns avg temp, max temp, and min temp dor the given date"""

    results=session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs)).\
    filter(Measurement.date>=date).all()

            #create JSON list of dicts
    data_list=[]

    for result in results:
        row={}
        row['Start Date'] =date
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = float(result[0])
        row['Highest Temperature'] = float(result[1])
        row['Lowest Temperature'] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date,end_date):
    """Returns the avg,max,min temp between a time period"""
    results=session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs)).\
        filter(Measurement.date >=start_date,Measurement.date <= end_date).all()
        
    #generates JSON list of dicts
    data_list=[]
    for result in results:
        row={}
        row["Start Date"]=start_date
        row["End Date"]= end_date
        row["Average Temperature"]=float(result[0])
        row['Highest Temperature']=float(result[1])
        row['Lowest Temperature']=float(result[2])
        data_list.append(row)
    return jsonify(data_list)

if __name__=='__main__':
    app.run(debug=True)
        

   
           
           
           
           
           
           
           
               