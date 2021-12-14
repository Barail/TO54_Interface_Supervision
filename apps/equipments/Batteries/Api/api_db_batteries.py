import sqlite3
import pandas as pd
from sqlite3 import Error
import csv
import os
from datetime import time


def create_connection(db_file):
    """ create assets database connection to assets SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

def create_table(conn):
    """ create assets table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: assets CREATE TABLE statement
    :return:
    """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS measurements (
                                time TEXT NOT NULL PRIMARY KEY ,
                                charger_Volt_O1 FLOAT,
                                charger_Volt_O2 FLOAT,
                                charger_Volt_O3 FLOAT,
                                charger_Current_O1 FLOAT,
                                charger_Current_O2 FLOAT,
                                charger_Current_O3 FLOAT,
                                charger_AC_Power FLOAT,
                                charger_AC_Current FLOAT,
                                grid_L1_Power FLOAT,
                                grid_L2_Power FLOAT,
                                grid_L3_Power FLOAT,
                                battery_Min_Cell_Volt FLOAT,
                                battery_Max_Cell_Volt FLOAT,
                            ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_measurement(conn, time, charger_Volt_O1, charger_Volt_O2, charger_Volt_O3, charger_Current_O1, charger_Current_O2,charger_Current_O3,charger_AC_Power,charger_AC_Current,grid_L1_Power,grid_L2_Power,grid_L3_Power,battery_Min_Cell_Volt, battery_Max_Cell_Volt):
    """
    Create assets new entry into the measurements table
    :param conn:
    :param measurement_set:
    :return: project id
    """
    cur = conn.cursor()
    measurements_set = ''' INSERT INTO measurements(time, charger_Volt_O1, charger_Volt_O2, charger_Volt_O3, charger_Current_O1, charger_Current_O2,charger_Current_O3,charger_AC_Power,charger_AC_Current,grid_L1_Power,grid_L2_Power,grid_L3_Power,battery_Min_Cell_Volt, battery_Max_Cell_Volt) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur.execute(measurements_set, (time, charger_Volt_O1, charger_Volt_O2, charger_Volt_O3, charger_Current_O1, charger_Current_O2,charger_Current_O3,charger_AC_Power,charger_AC_Current,grid_L1_Power,grid_L2_Power,grid_L3_Power,battery_Min_Cell_Volt, battery_Max_Cell_Volt))
    conn.commit()
    return cur.lastrowid

def get_latest_data(conn):
    """
    Query data rows between two ranges
    :returns: pandas dataframe object
    """

    statement = f'SELECT * FROM measurements ORDER BY time DESC LIMIT 200;'
    df = pd.read_sql_query(statement, conn)
    return df

def get_data_by_id(conn, id):
    """
    Query assets row from assets table

    :params id: assets row id
    :returns: pandas dataframe object
    """

    statement = f'SELECT * FROM measurements WHERE rowid = "{id}";'
    df = pd.read_sql_query(statement, conn)
    return df

def print_all_measurements(conn):
    """
    Query all rows in the measurements table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM measurements")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def print_today_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT time FROM measurements WHERE strftime(\"%Y-%m-%d\", time) == date() ORDER BY time ASC")
    rows = cur.fetchall()

    for row in rows:
        print(row)

def get_min_time_in_db(conn):
    statement = f"SELECT time FROM measurements WHERE ROWID IN ( SELECT min( ROWID ) FROM measurements);"
    df = pd.read_sql_query(statement, conn)
    return df['time'][0][:10]

def get_max_time_in_db(conn):
    statement = f"SELECT time FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements);"
    df = pd.read_sql_query(statement, conn)
    return df['time'][0][:10]

def print_latest_10_measurements(conn):
    """
    Query all rows in the measurements table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM measurements ORDER BY time DESC LIMIT 10;")

    rows = cur.fetchall()

    for row in rows:
        print(row)
        
def export_to_csv(conn_db):
  # Export data into CSV file
    print("Exporting data into CSV............")
    cursor = conn_db.cursor()
    cursor.execute("select * from measurements")
    with open("data_pv.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/data_pv.csv"
    print("Data exported Successfully into {}".format(dirpath))
