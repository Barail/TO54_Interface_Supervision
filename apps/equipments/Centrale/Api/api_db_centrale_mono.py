import sqlite3
import pandas as pd
from sqlite3 import Error
import csv
import os


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
                                puissance_centrale_mono FLOAT ,
                                energie_centrale_mono FLOAT ,
                                courant_centrale_mono FLOAT ,
                                tens_ph_n_centrale_mono FLOAT
                            ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_measurement(conn, time, puissance_centrale_mono, energie_centrale_mono, courant_centrale_mono, tens_ph_n_centrale_mono):
    """
    Create assets new entry into the measurements table
    :param conn:
    :param measurement_set:
    :return: project id
    """
    cur = conn.cursor()
    measurements_set = ''' INSERT INTO measurements(time, puissance_centrale_mono, energie_centrale_mono, courant_centrale_mono, tens_ph_n_centrale_mono) VALUES(?,?,?,?,?)'''
    cur.execute(measurements_set, (time, puissance_centrale_mono, energie_centrale_mono, courant_centrale_mono, tens_ph_n_centrale_mono))
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
    with open("data_centrale_mono.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/data_centrale_mono.csv"
    print("Data exported Successfully into {}".format(dirpath))
