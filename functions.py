import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
from flask import jsonify

# Defining a 
def GetDateAndPrecipDict(engine, Base):

    # Saving references to tables in a function-specific way to make code more generalizable.
    Measurement = Base.classes.measurement

    session = Session(engine)
    dateAndPrecip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    session.close()

    precipData = pd.DataFrame(dateAndPrecip)
    precipData = precipData.set_index(["date"])

    precipData = precipData.sort_index(ascending=False)
    precipData = precipData.dropna()
    
    return precipData.to_dict()["prcp"]

def GetStations(engine, Base):

    Station = Base.classes.station

    session = Session(engine)
    allStations = session.query(Station.station, Station.name).all()
    session.close()

    allStations = pd.DataFrame(allStations)
    allStations = allStations.set_index("station")

    return allStations.to_dict()["name"]

def GetTobsData(engine, Base):

    Measurement = Base.classes.measurement

    session = Session(engine)

    temp12months = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23', Measurement.station == 'USC00519281').order_by(Measurement.date).all()

    session.close()

    return temp12months

# Remember to put in a try, except error handling statement!
def StartDate(engine, Base, date):

    Measurement = Base.classes.measurement

    session = Session(engine)

    lowestTemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date).group_by(Measurement.station).all()

    highestTemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date).group_by(Measurement.station).all()

    avgTemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date).group_by(Measurement.station).all()

    session.close()

    return ({"Highest Temp" : highestTemp[0][0],
            "Lowest Temp" : lowestTemp[0][0],
            "Average Temp" : avgTemp[0][0]})

def StartAndEndDates(engine, Base, date1, date2):

    Measurement = Base.classes.measurement

    session = Session(engine)

    lowestTemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date1).\
        filter(Measurement.date <= date2).group_by(Measurement.station).all()

    highestTemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date1).\
        filter(Measurement.date <= date2).group_by(Measurement.station).all()

    avgTemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date1).\
        filter(Measurement.date <= date2).group_by(Measurement.station).all()

    session.close()

    return ({"Highest Temp" : highestTemp[0][0],
            "Lowest Temp" : lowestTemp[0][0],
            "Average Temp" : avgTemp[0][0]})