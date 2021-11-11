import pandas as pd
from datetime import date
import time

def get_min_time_in_db(conn):
    statement = f"SELECT dateTime FROM archive WHERE ROWID IN ( SELECT min( ROWID ) FROM archive);"
    df = pd.read_sql_query(statement, conn)
    return time.strftime("%Y-%m-%d", time.gmtime(int(df['dateTime'][0])))

def get_max_time_in_db(conn):
    statement = f"SELECT dateTime FROM archive WHERE ROWID IN ( SELECT max( ROWID ) FROM archive);"
    df = pd.read_sql_query(statement, conn)
    return time.strftime("%Y-%m-%d", time.gmtime(int(df['dateTime'][0])))
