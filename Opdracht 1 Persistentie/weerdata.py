import psycopg2
from psycopg2 import Error
import numpy as np
import csv
import pandas as pd


from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

def connect():
    """This function is the connection with the postgres db"""

    connection = psycopg2.connect(host='localhost', database='weer ', user='postgres', password='Xplod_555')
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
weer = pd.read_table("./knmidata/etmgeg_260.txt", sep=',' )
weer_df = weer[['YYYYMMDD', '   TG', '   TN', '   TX']]
weer_df.rename(columns = {'   TG': 'TG', '   TN': 'TN', '   TX' : 'TX'}, inplace = True)
weer_df.TG = weer_df.TG.apply(lambda x : x /10)
weer_df.TN = weer_df.TN.apply(lambda x : x /10)
weer_df.TX = weer_df.TX.apply(lambda x : x /10)

connection = connect()
cur = connection.cursor()
print(len(weer_df))
try:
    for i in range(len(weer_df)):
        sql_execute('insert into orgnieel_data(YYYYMMDD, TG, TN, TX)values (%s ,%s , %s,%s)',[weer_df.YYYYMMDD[i], weer_df.TG[i], weer_df.TN[i], weer_df.TX[i]])

    print('orgnieel_data table done')


    for i in range(len(weer_df)):
        for j in weer_df.YYYYMMDD:
            jaar = (str(j)[:4])
            maand = (str(j)[4:6])
            dag = (str(j)[6:8])
            sql_execute(
                'insert into dagelijkse_data(dag, maand, jaar ,YYYYMMDD, TG, TN, TX)values (%s ,%s , %s,%s, %s ,%s , %s)',
                [dag, maand, jaar, weer_df.YYYYMMDD[i], weer_df.TG[i], weer_df.TN[i], weer_df.TX[i]])

    print('dagelijkse_data table done')





except (Exception, psycopg2.DatabaseError) as error:

    print(error)

disconnect()
