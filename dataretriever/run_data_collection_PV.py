
import time as t
from datetime import datetime
import pathlib
from apps.equipments.PV.Api import api_db_pv
from apps.equipments.PV.Communication import comm_pv

# Parameters
debug = False
DB_FILENAME = "data_pv.db"
external_ip = "172.23.28.1" #"172.23.28.1" #"192.168.0.102"

# Connect to database and create table
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME).resolve()
conn_db = api_db_pv.create_connection(DB_FILE)
api_db_pv.create_table(conn_db)
#if debug:
#api_db.print_latest_10_measurements(conn_db)

# Connect to external system
client_external = comm_pv.connect_to_external_system(external_ip)
#if not client_external.is_socket_open():
    #print('Connection to external system failed.')

# Infinite loop
print('Starting infinite loop to acquire data...')
print('--- Use CTRL + C to stop ---')

while True:
    # Get current time
    time = datetime.now()
    print(time)
    #if client_external.is_socket_open():
    print('bonjour')
        # Get external system measurements
        
    PV_power = comm_pv.read_power_pv(client_external)
    
    print(PV_power)
    
    
        # Add measurements to database
    api_db_pv.add_measurement(conn_db, time, PV_power)
    #else:
        #client_external.connect()
        #print('Erreur connexion...')
    # Wait 1 second until next readings
    t.sleep(1)

    api_db_pv.export_to_csv(conn_db)

