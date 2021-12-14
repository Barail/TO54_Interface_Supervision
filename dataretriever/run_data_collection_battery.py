from apps.equipments.Batteries.Communication import comm_batteries
from apps.equipments.Batteries.Api import api_db_batteries

import pathlib

# Parameters
debug = False
DB_FILENAME = "data_battery.db"
external_ip = "TO DEFINED"  # "172.23.28.1" #"192.168.0.102"

# Connect to database and create table
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME).resolve()
conn_db = api_db_batteries.create_connection(DB_FILE)
api_db_batteries.create_table(conn_db)
# if debug:
# api_db.print_latest_10_measurements(conn_db)

# Connect to external system
client_external = comm_batteries.connect_to_external_system(external_ip)
# if not client_external.is_socket_open():
# print('Connection to external system failed.')

# Infinite loop
print('Starting infinite loop to acquire data...')
print('--- Use CTRL + C to stop ---')

while True:
    # Get current time
    time = datetime.now()
    # if client_external.is_socket_open():
    # Get external system measurements
    charger_Volt_O1 = comm_batteries.read_charger_Voltage_Output1(client_external)
    charger_Volt_O2 = comm_batteries.read_charger_Voltage_Output2(client_external)
    charger_Volt_O3 = comm_batteries.read_charger_Voltage_Output3(client_external)
    charger_Current_O1 = comm_batteries.read_charger_Current_Output1(client_external)
    charger_Current_O2 = comm_batteries.read_charger_Current_Output2(client_external)
    charger_Current_O3 = comm_batteries.read_charger_Current_Output3(client_external)
    charger_AC_Power = comm_batteries.read_charger_AC_Power(client_external)
    charger_AC_Current = comm_batteries.read_charger_AC_Current(client_external)
    grid_L1_Power = comm_batteries.read_grid_L1_Power(client_external)
    grid_L2_Power = comm_batteries.read_grid_L2_Power(client_external)
    grid_L3_Power = comm_batteries.read_grid_L3_Power(client_external)
    battery_Min_Cell_Volt = comm_batteries.read_minimum_cell_voltage(client_external)
    battery_Max_Cell_Volt = comm_batteries.read_maximum_cell_voltage(client_external)

    # Add measurements to database
    api_db_pv.add_measurement(conn_db, time, charger_Volt_O1, charger_Volt_O2, charger_Volt_O3, charger_Current_O1,
                              charger_Current_O2, charger_Current_O3, charger_AC_Power, charger_AC_Current,
                              grid_L1_Power, grid_L2_Power, grid_L3_Power, battery_Min_Cell_Volt, battery_Max_Cell_Volt)
    # else:
    # client_external.connect()
    # print('Erreur connexion...')
    # Wait 1 second until next readings
    t.sleep(1)

    api_db_batteries.export_to_csv(conn_db)
