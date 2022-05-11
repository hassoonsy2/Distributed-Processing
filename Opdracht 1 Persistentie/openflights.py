import psycopg2
from psycopg2 import Error
import numpy as np
import csv
import pandas as pd
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

def connect():
    """This function is the connection with the postgres db"""

    connection = psycopg2.connect(host='localhost', database='openflights', user='postgres', password='Xplod_555')
    return connection


def disconnect():
    """This function disconnects the program with the postgres db"""
    con = connect()
    return con.close()


def sql_execute(sql,value):
    """This function executes a query on the Postgres db"""
    c = connect()
    cur = c.cursor()
    cur.execute(sql,value)
    c.commit()



def sql_query(sql):
    """This function executes a query on the Postgres db """
    c = connect()
    cur = c.cursor()
    cur.execute(sql)
    c.commit()


def commit():
   """This function will cpmmit  a query on the Postgres db """
   c = connect()
   c.commit()


""" Load data """

countries = pd.read_csv("./dataopenflights/countries.dat")
airlines= pd.read_csv("./dataopenflights/airlines.dat")
airports = pd.read_csv("./dataopenflights/airports-extended.dat" )
planes = pd.read_csv("./dataopenflights/planes.dat")
routes = pd.read_csv("./dataopenflights/routes.dat")

"""Make dataframe"""

airlines.rename(columns = {'-1' : 'airline_id', 'Unknown' : 'name', r"\N" :'alias','-' :'iata_code', 'N/A': 'icao_code', r'\N.1' : 'callsing', r'\N.2' : 'country', 'Y': 'active' }, inplace = True)
countries.rename(columns = {'Bonaire, Saint Eustatius and Saba' : 'name', 'BQ' : 'iso_code', "Unnamed: 2" :'dafif_code' }, inplace = True)
planes.rename(columns = {'Aerospatiale (Nord) 262' : 'name', 'ND2' : 'iata_code', "N262" :'icao_code' }, inplace = True)
airports.rename(columns = {'1' : 'airport_id', 'Goroka Airport' : 'name', "Goroka" :'city' , 'Papua New Guinea': 'country', 'GKA': 'iata_code', 'AYGA': 'icao_code', '-6.081689834590001' : 'latitude', '145.391998291' : 'longitude', '5282': 'altitude', '10' : 'timezone', 'U' : 'dst', 'Pacific/Port_Moresby' : 'tzdatabasetimezone', 'airport' : 'type', 'OurAirports' : 'source'}, inplace = True)
routes.rename(columns = {'2B' : 'airline', '410' : 'airline_id', "AER" :'source_airport', '2965' : 'source_airport_id', 'KZN' : 'dest_airport', '2990' : 'dest_airport_id' , 'Unnamed: 6' : 'codeshare', '0' : 'stops' , 'CR2' : 'equipment'  }, inplace = True)


""" Data cleaning """

airports['airport_id'].values.astype(int)
airports.timezone = airports.timezone.replace(r'\\N', "0", regex=True)
airports.dst = airports.dst.replace(r'\\N', "Z", regex=True)
routes.codeshare.fillna('x', inplace=True)
routes.dest_airport_id = routes.dest_airport_id.replace(r'\\N', "0", regex=True)
routes.source_airport_id = routes.source_airport_id.replace(r'\\N', "0", regex=True)
routes.airline_id = routes.airline_id.replace(r'\\N', "999", regex=True)

""" Insert data into db"""
connection = connect()
cur = connection.cursor()

try:
    for i in range(len(planes)):
        sql_execute('insert into plane(iata_code, name, icao_code)values (%s ,%s , %s)',[planes.iata_code[i], planes.name[i], planes.icao_code[i]])
    print('Plane table done')


    for i in range(len(countries)):
        sql_execute('insert into country(iso_code, name, dafif_code)values (%s ,%s , %s)',[countries.iso_code[i], countries.name[i], countries.dafif_code[i]])
    print('countries table done')

    for i in range(len(airports)):
        sql_execute('insert into airports(airport_id, name, city, country, iata, icao, latitude, longitude, altitude, timezone, dest, timezone_database, type, source )values (%s ,%s , %s, %s ,%s , %s, %s ,%s , %s, %s ,%s , %s, %s , %s) ',
                    [airports.airport_id[i], airports.name[i], airports.city[i], airports.country[i] , airports.iata_code[i], airports.icao_code[i], airports.latitude[i],
                     airports.longitude[i], airports.altitude[i], airports.timezone[i], airports.dst[i], airports.tzdatabasetimezone[i], airports.type[i], airports.source[i]])
    print('airports table done')

    for i in range(len(airlines)):
        sql_execute(
            'insert into airlines(airline_id, name, iata_code, icao_code, callsign, country, active, alias)values (%s ,%s , %s, %s ,%s , %s, %s ,%s )',
            [airlines.airline_id[i], airlines.name[i], airlines.iata_code[i], airlines.icao_code[i], airlines.callsing[i],
             airlines.country[i], airlines.active[i],
             airlines.alias[i]])
    print('airlines table done')

    for i in range(len(routes)):
        sql_execute(
            'insert into routes(airline_code, airline_id, source_airport_code, source_airport_id, dest_airport_code, dest_airport_id, codeshare, stops, equipment)values (%s ,%s , %s, %s ,%s , %s, %s ,%s , %s)',
            [routes.airline[i], routes.airline_id[i], routes.source_airport[i], routes.source_airport_id[i], routes.dest_airport[i],
             routes.dest_airport_id[i], routes.codeshare[i],
             routes.stops[i], routes.equipment[i]])
    print('routes table done')


    #In case an error occures, an error-message will be shown.
except (Exception, psycopg2.DatabaseError) as error:

    print(error)

disconnect()

