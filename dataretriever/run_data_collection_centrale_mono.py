
import time as t
from datetime import datetime
import pathlib
from databases.DatabaseFunctions import api_db
import comm_stack

# Parameters
debug = False
DB_FILENAME = "data.db"
external_ip = "192.168.0.102"

# Connect to database and create table
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME).resolve()
conn_db = api_db.create_connection(DB_FILE)
api_db.create_table(conn_db)
#if debug:
#api_db.print_latest_10_measurements(conn_db)

# Connect to external system
client_external = comm_stack.connect_to_external_system(external_ip)
if not client_external.is_socket_open():
    print('Connection to external system failed.')

#set_current = api_external.set_current(client_external)
#start = api_external.start(client_external)


# Infinite loop
print('Starting infinite loop to acquire data...')
print('--- Use CTRL + C to stop ---')

while True:
    # Get current time
    time = datetime.now()
    print(time)
    if client_external.is_socket_open():
        print('bonjour')
        # Get external system measurements
        status = comm_stack.read_status(client_external)
        print(f'Status: {status}')
        
        current = comm_stack.read_current(client_external)
        print(f'Stack current: {current}')
    
        conductivity = comm_stack.read_conductivity(client_external)
        print(f'Water conductivity: {conductivity}')
    
        water_temp_out_stack = comm_stack.read_water_temp_out_stack(client_external)
        print(f'Water Temperature out: {water_temp_out_stack}')
        
        water_temp_in_stack = comm_stack.read_water_temp_in_stack(client_external)
        print(f'Water temperature in stack: {water_temp_in_stack}')
    
        power = comm_stack.read_power(client_external)
        print(f'Stack power: {power}')

        voltage = comm_stack.read_voltage(client_external)
        print(f'Stack voltage: {voltage}')

        stop_code = comm_stack.read_stop_code(client_external)
        print(f'StopCode: {stop_code}')

        psu_current = comm_stack.read_psu_current(client_external)
        print(f'PSU current: {psu_current}')

        psu_voltages = comm_stack.read_psu_voltages(client_external)
        print(f'PSU voltages: {psu_voltages}')

        h2_production = comm_stack.read_h2_production(client_external)
        print(f'H2 production: {h2_production}')

        h2_pressure = comm_stack.read_h2_pressure(client_external)
        print(f'H2 pressure: {h2_pressure}')

        output_pressure = comm_stack.read_output_pressure(client_external)
        print(f'Output pressure: {output_pressure}')

        water_o2_pressure = comm_stack.read_water_o2_pressure(client_external)
        print(f'Water/O2 pressure: {water_o2_pressure}')

        water_flow = comm_stack.read_water_flow(client_external)
        print(f'Water flow: {water_flow}')

        run_time = comm_stack.read_run_time(client_external)
        print(f'Run time: {run_time}')

        total_run_time = comm_stack.read_total_run_time(client_external)
        print(f'Total run time: {total_run_time}')

        

##        set_below_pressure = comm_stack.set_start_below_pressure(client_external)
##        print(f'start below pressure: {set_below_pressure}')

##        stop_after_pressure = api_external.read_stop_after_pressure(client_external)
##        print(f'Stop after pressure: {stop_after_pressure}')
##
##        start_below_pressure= api_external.read_stop_after_pressure(client_external)
##        print(f'Start below pressure: {start_below_pressure}')

        max_cell_voltage = comm_stack.read_max_cell_voltage(client_external)
        print(f'Max cell voltage: {max_cell_voltage}')

        status_HyDry = comm_stack.read_status_HyDry(client_external)
        print(f'Hydry Status: {status_HyDry}')
        
        stop_code_HyDry = comm_stack.read_stop_code_HyDry(client_external)
        print(f'STOP CODE HYDRY: {stop_code_HyDry}')

        deox_temperature = comm_stack.read_deox_temperature(client_external)        
        print(f'deox_temperature: {deox_temperature}')
        condenser_temperature = comm_stack.read_condenser_temperature(client_external)
        print(f'condenser_temperature: {condenser_temperature}')
        dry1_rem_capacity = comm_stack.read_dry1_rem_capacity(client_external)
        print(f'dry1_rem_capacity: {dry1_rem_capacity}')
        dry2_rem_capacity = comm_stack.read_dry2_rem_capacity(client_external)
        print(f'dry2_rem_capacity: {dry2_rem_capacity}')
        system_pressure = comm_stack.read_system_pressure(client_external)
        print(f'PRESSURE: {system_pressure}')

        # Add measurements to database
        api_db.add_measurement(conn_db, time, current, conductivity, water_temp_out_stack, water_temp_in_stack, power, voltage, stop_code, psu_current, psu_voltages, h2_production, h2_pressure, output_pressure, water_o2_pressure, water_flow, run_time, total_run_time, max_cell_voltage, status, status_HyDry, stop_code_HyDry, deox_temperature, condenser_temperature, dry1_rem_capacity, dry2_rem_capacity, system_pressure)
    else:
        client_external.connect()
        print('Erreur connexion...')
    # Wait 1 second until next readings
    t.sleep(1)

    api_db.export_to_csv(conn_db)
