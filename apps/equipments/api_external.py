from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient


def connect_to_external_system(ip):
    # Connect to external system via ModBus
    client = 0
    try:
        print('Connecting to ' + ip + '...')
        client = ModbusTcpClient(ip, port=502, unit_id=1, auto_open=True, auto_close=False)
        client.connect()
        print('Connection success')
    except:
        print('Connection failed.')
    return client

##def read_PV_power(client):
##    PV_power = -1
##    if client.is_socket_open():
##        result = client.read_holding_registers(502, 1)
##        print('PV power')
##        if result.isError():
##            print('Error reading status')
##            client.connect()
##            answer = result.registers
##            PV_power = int(answer[0])
##        else:
##            answer = result.registers
##            PV_power = int(answer[0])
##    else:
##        client.connect()
##        print('ERROR STATUS')
##    return PV_power

##def read_PV_power(client):
##    PV_power = -1
##    if client.is_socket_open():
##        result = client.read_holding_registers(2, 1)
##        print('etape 1')
##        print(result)
##        if result.isError():
##            print('Error reading PV power')
##            client.connect()
##            result = client.read_holding_registers(1, 1)
##            answer = result.registers
##            PV_power = int(answer[0])
##        else:
##            answer = result.registers
##            PV_power = int(answer[0])
##            print('etape 3')
##    else:
##        client.connect()
##        result = client.read_holding_registers(1, 1)
##        try:
##            answer = result.registers
##            PV_power = int(answer[0])
##        except:
##            PV_power = -1
##    return PV_power

def read_PV_power(client):
    # Read StopCode
    PV_power = -1
    if client.is_socket_open():
        PV_power = client.read_holding_registers(40501, 1) #
        print('etape 1')
        if PV_power.isError():
            print('Error reading PV power')
        else:
            print('etape 2')
            answer = PV_power.registers
            PV_power = int(answer[0])
    else:
        client.connect()
        PV_power = client.read_holding_registers(40501, 1)
        answer = PV_power.registers
        PV_power = int(answer[0])
    return PV_power

def read_total_active_power(client):
    total_active_power = -1
    if client.is_socket_open():
        total_active_power = client.read_holding_registers(0, 2)
        print('etape 1')
        print(total_active_power)
        if total_active_power.isError():
            print('Error reading total_active_power')
        else:
            print('etape 2')
            answer = total_active_power.registers
            print(answer)
            total_active_power = int(answer[0])*100
            print(total_active_power)
    else:
        client.connect()
        total_active_power = client.read_holding_registers(36871, 2)
        print(total_active_power)
        answer = total_active_power.registers
        total_active_power = int(answer[0])*100
        print(total_active_power)
    return total_active_power
        

def read_status(client): # au premier tour cette fonction fonctionne
    # Read status
    status = -1
    if client.is_socket_open():
        result = client.read_holding_registers(101, 1)
        if result.isError():
            print('Error reading status')
        else:
            answer = result.registers
            status = int(answer[0])
    else:
        client.connect()
        print('ERROR STATUS')
    return status

def read_status_HyDry(client):
    # Read status
    status_HyDry = -1
    if client.is_socket_open():
        status_HyDry = client.read_holding_registers(300, 1) # -1 
        if status_HyDry.isError():
            print('Error reading status')
        else:
            answer = status_HyDry.registers
            status_HyDry = int(answer[0])
    else:
        client.connect()
        status_HyDry = client.read_holding_registers(300, 1) # -1
        try:
            answer = status_HyDry.registers
            status_HyDry = int(answer[0])
        except:
            status_HyDry = -1
    return status_HyDry

def read_current(client):
    # Read current
    current = -1
    if client.is_socket_open():
        result = client.read_holding_registers(105, 1)
        if result.isError():
            print('Error reading current')
        else:
            answer = result.registers
            current = int(answer[0])*0.1
    else:
        client.connect()
        result = client.read_holding_registers(105, 1)
        try:
            answer = result.registers
            current = int(answer[0])*0.1
        except:
            current = -1
    return current

def read_power(client):
    # Read power
    power = -1
    if client.is_socket_open():
        result = client.read_holding_registers(108, 1)
        print('salut')
        if result.isError():
            print('Error reading power')
        else:
            answer = result.registers
            power = int(answer[0])
    else:
        client.connect()
        result = client.read_holding_registers(108, 1)
        print(result)
        print('salut')
        try:
            answer = result.registers
            power = int(answer[0])
        except:
            power = -1
    return power

def read_conductivity(client):
    # Read conductivity
    conductivity = -1
    if client.is_socket_open():
        conductivity = client.read_holding_registers(115, 1) # normalement c'est le registre 116. Il semble y avoir un problème
        if conductivity.isError():
            print('Error reading conductivity')
        else:
            answer = conductivity.registers
            conductivity = int(answer[0])*0.1
    else:
        client.connect()
        conductivity = client.read_holding_registers(115, 1)
        try:
            answer = conductivity.registers
            conductivity = int(answer[0])*0.1
        except:
            conductivity = -1
    return conductivity

def read_water_temp_out_stack(client):
    # Read water temperature out
    water_temp_out_stack = -1
    if client.is_socket_open():
        water_temp_out_stack = client.read_holding_registers(114, 1) # normalement c'est le registre 115. Il semble y avoir un problème
        if water_temp_out_stack.isError():
            print('Error reading water temperature')
        else:
            answer = water_temp_out_stack.registers
            water_temp_out_stack = int(answer[0])*0.1
    else:
        client.connect()
        water_temp_out_stack = client.read_holding_registers(114, 1)
        try:
            answer = water_temp_out_stack.registers
            water_temp_out_stack = int(answer[0])*0.1
        except:
            water_temp_out_stack = -1
    return water_temp_out_stack

def read_water_temp_in_stack(client):
    # Read Water temperature in stack
    water_temp_in_stack = -1
    if client.is_socket_open():
        water_temp_in_stack = client.read_holding_registers(113, 1) # normalement c'est le registre 114. Il semble y avoir un problème
        if water_temp_in_stack.isError():
            print('Error reading water_temp_in_stack')
        else:
            answer = water_temp_in_stack.registers
            water_temp_in_stack = int(answer[0])*0.1
    else:
        client.connect()
        water_temp_in_stack = client.read_holding_registers(113, 1)
        answer = water_temp_in_stack.registers
        water_temp_in_stack = int(answer[0])*0.1
    return water_temp_in_stack

def read_voltage(client):
    # Read voltage
    voltage = -1
    if client.is_socket_open():
        voltage = client.read_holding_registers(106, 1) # normalement c'est le registre 115. Il semble y avoir un problème
        if voltage.isError():
            print('Error reading voltage')
        else:
            answer = voltage.registers
            voltage = int(answer[0])*0.1
    else:
        client.connect()
        voltage = client.read_holding_registers(106, 1)
        answer = voltage.registers
        voltage = int(answer[0])*0.1
    return voltage

def read_stop_code(client):
    # Read StopCode
    stop_code = -1
    if client.is_socket_open():
        stop_code = client.read_holding_registers(101, 1) # normalement c'est le registre 102. Il semble y avoir un problème
        if stop_code.isError():
            print('Error reading stop_code')
        else:
            answer = stop_code.registers
            stop_code = int(answer[0])
    else:
        client.connect()
        stop_code = client.read_holding_registers(101, 1)
        answer = stop_code.registers
        stop_code = int(answer[0])
    return stop_code

def read_stop_code_HyDry(client):
    # Read StopCode
    stop_code_HyDry = -1
    if client.is_socket_open():
        stop_code_HyDry = client.read_holding_registers(301, 1) # normalement c'est le registre 102. Il semble y avoir un problème
        if stop_code_HyDry.isError():
            print('Error reading stop_code_HyDry')
        else:
            answer = stop_code_HyDry.registers
            stop_code_HyDry = int(answer[0])
    else:
        client.connect()
        stop_code_HyDry = client.read_holding_registers(301, 1)
        answer = stop_code_HyDry.registers
        stop_code_HyDry = int(answer[0])
    return stop_code_HyDry

def read_deox_temperature(client):
    # Read deox_temperature
    deox_temperature = -1
    if client.is_socket_open():
        deox_temperature = client.read_holding_registers(302, 1) 
        if deox_temperature.isError():
            print('Error reading deox_temperature')
        else:
            answer = deox_temperature.registers
            deox_temperature = int(answer[0])*0.01
    else:
        client.connect()
        deox_temperature = client.read_holding_registers(302, 1)
        try:
            answer = deox_temperature.registers
            deox_temperature = int(answer[0])*0.01
        except:
            deox_temperature = -1
    return deox_temperature

def read_condenser_temperature(client):
    # Read condenser temperature
    condenser_temperature = -1
    if client.is_socket_open():
        condenser_temperature = client.read_holding_registers(303, 1) 
        if condenser_temperature.isError():
            print('Error reading condenser_temperature')
        else:
            answer = condenser_temperature.registers
            condenser_temperature = int(answer[0])*0.1
    else:
        client.connect()
        condenser_temperature = client.read_holding_registers(303, 1)
        answer = condenser_temperature.registers
        condenser_temperature = int(answer[0])*0.1
    return condenser_temperature

def read_dry1_rem_capacity(client):
    # Read Dryer 1 remaining capacity
    dry1_rem_capacity = -1
    if client.is_socket_open():
        dry1_rem_capacity = client.read_holding_registers(305, 1) 
        if dry1_rem_capacity.isError():
            print('Error reading dry1_rem_capacity')
        else:
            answer = dry1_rem_capacity.registers
            dry1_rem_capacity = int(answer[0])
    else:
        client.connect()
        dry1_rem_capacity = client.read_holding_registers(305, 1)
        answer = dry1_rem_capacity.registers
        dry1_rem_capacity = int(answer[0])
    return dry1_rem_capacity

def read_dry2_rem_capacity(client):
    # Read Dryer 2 remaining capacity
    dry2_rem_capacity = -1
    if client.is_socket_open():
        dry2_rem_capacity = client.read_holding_registers(306, 1)
        if dry2_rem_capacity.isError():
            print('Error reading dry2_rem_capacity')
        else:
            answer = dry2_rem_capacity.registers
            dry2_rem_capacity = int(answer[0])
    else:
        client.connect()
        dry2_rem_capacity = client.read_holding_registers(306, 1)
        answer = dry2_rem_capacity.registers
        dry2_rem_capacity = int(answer[0])
    return dry2_rem_capacity

def read_system_pressure(client):
    # Read System pressure
    system_pressure = -1
    if client.is_socket_open():
        system_pressure = client.read_holding_registers(307, 1) 
        if system_pressure.isError():
            print('Error reading system_pressure')
        else:
            answer = system_pressure.registers
            system_pressure = int(answer[0])*0.1
    else:
        client.connect()
        system_pressure = client.read_holding_registers(307, 1)
        try:
            answer = system_pressure.registers
            system_pressure = int(answer[0])*0.1
        except:
            system_pressure = -1
    return system_pressure

def read_psu_current(client):
    # Read PSU current
    psu_current = -1
    if client.is_socket_open():
        psu_current = client.read_holding_registers(105, 1) # normalement c'est le registre 106. Il semble y avoir un problème
        if psu_current.isError():
            print('Error reading psu_current')
        else:
            answer = psu_current.registers
            psu_current = int(answer[0])*0.1
    else:
        client.connect()
        psu_current = client.read_holding_registers(105, 1)
        try:
            answer = psu_current.registers
            psu_current = int(answer[0])*0.1
        except:
            psu_current = -1 
    return psu_current

def read_psu_voltages(client):
    # Read PSU voltages
    psu_voltages = -1
    if client.is_socket_open():
        psu_voltages = client.read_holding_registers(107, 1) # normalement c'est le registre 108. Il semble y avoir un problème
        if psu_voltages.isError():
            print('Error reading psu_voltages')
        else:
            answer = psu_voltages.registers
            psu_voltages = int(answer[0])*0.1
    else:
        client.connect()
        psu_voltages = client.read_holding_registers(107, 1)
        answer = psu_voltages.registers
        psu_voltages = int(answer[0])*0.1
    return psu_voltages

def read_h2_production(client):
    # Read H2 production
    h2_production = -1
    if client.is_socket_open():
        h2_production = client.read_holding_registers(109, 1) # normalement c'est le registre 110. Il semble y avoir un problème
        if h2_production.isError():
            print('Error reading h2_production')
        else:
            answer = h2_production.registers
            h2_production = int(answer[0])*0.01
    else:
        client.connect()
        h2_production = client.read_holding_registers(109, 1)
        answer = h2_production.registers
        h2_production = int(answer[0])*0.01
    return h2_production


def read_h2_pressure(client):
    # Read H2 pressure
    h2_pressure = -1
    if client.is_socket_open():
        h2_pressure = client.read_holding_registers(110, 1) # normalement c'est le registre 111. Il semble y avoir un problème
        if h2_pressure.isError():
            print('Error reading h2_pressure')
        else:
            answer = h2_pressure.registers
            h2_pressure = int(answer[0])*0.01
    else:
        client.connect()
        h2_pressure = client.read_holding_registers(110, 1)
        answer = h2_pressure.registers
        h2_pressure = int(answer[0])*0.01
    return h2_pressure

def read_output_pressure(client):
    # Read output pressure
    output_pressure = -1
    if client.is_socket_open():
        output_pressure = client.read_holding_registers(111, 1) # normalement c'est le registre 112. Il semble y avoir un problème
        if output_pressure.isError():
            print('Error reading output_pressure')
        else:
            answer = output_pressure.registers
            output_pressure = int(answer[0])*0.01
    else:
        client.connect()
        output_pressure = client.read_holding_registers(111, 1)
        answer = output_pressure.registers
        output_pressure = int(answer[0])*0.01
    return output_pressure

def read_water_o2_pressure(client):
    # Read Water/O2 pressure
    water_o2_pressure = -1
    if client.is_socket_open():
        water_o2_pressure = client.read_holding_registers(112, 1) # normalement c'est le registre 113. Il semble y avoir un problème
        if water_o2_pressure.isError():
            print('Error reading water_o2_pressure')
        else:
            answer = water_o2_pressure.registers
            water_o2_pressure = int(answer[0])*0.01
    else:
        client.connect()
        water_o2_pressure = client.read_holding_registers(112, 1)
        answer = water_o2_pressure.registers
        water_o2_pressure = int(answer[0])*0.01
    return water_o2_pressure

def read_water_flow(client):
    # Read Water flow
    water_flow = -1
    if client.is_socket_open():
        water_flow = client.read_holding_registers(116, 1) # normalement c'est le registre 117. Il semble y avoir un problème
        if water_flow.isError():
            print('Error reading water flow')
        else:
            answer = water_flow.registers
            water_flow = int(answer[0])*0.1
    else:
        client.connect()
        water_flow = client.read_holding_registers(116, 1)
        answer = water_flow.registers
        water_flow = int(answer[0])*0.1
    return water_flow

def read_run_time(client):
    # Read Run time
    run_time = -1
    if client.is_socket_open():
        run_time = client.read_holding_registers(117, 1) # normalement c'est le registre 118. Il semble y avoir un problème
        if run_time.isError():
            print('Error reading run time')
        else:
            answer = run_time.registers
            run_time = int(answer[0])
    else:
        client.connect()
        run_time = client.read_holding_registers(117, 1)
        try:
            answer = run_time.registers
            run_time = int(answer[0])
        except:
            run_time = -1
    return run_time

def read_total_run_time(client):
    # Read Total run time
    total_run_time = -1
    if client.is_socket_open():
        total_run_time = client.read_holding_registers(118, 1) # normalement c'est le registre 119. Il semble y avoir un problème
        if total_run_time.isError():
            print('Error reading total run time')
        else:
            answer = total_run_time.registers
            total_run_time = int(answer[0])
    else:
        client.connect()
        total_run_time = client.read_holding_registers(118, 1)
        try:
            answer = total_run_time.registers
            total_run_time = int(answer[0])
        except:
            total_run_time = -1
    return total_run_time

def read_stop_after_pressure(client):
    # Read stop after pressure
    stop_after_pressure = -1
    if client.is_socket_open():
        stop_after_pressure = client.read_holding_registers(120, 1) # normalement c'est le registre 102. Il semble y avoir un problème
        if stop_after_pressure.isError():
            print('Error reading stop after pressure')
        else:
            answer = stop_after_pressure.registers
            stop_after_pressure = int(answer[0])*0.01
    else:
        client.connect()
        stop_after_pressure = client.read_holding_registers(120, 1)
        answer = stop_after_pressure.registers
        stop_after_pressure = int(answer[0])*0.01
    return stop_after_pressure

def read_start_below_pressure(client):
    # Read start below pressure
    start_below_pressure = -1
    if client.is_socket_open():
        start_below_pressure = client.read_holding_registers(119, 1) # normalement c'est le registre 120. Il semble y avoir un problème
        if start_below_pressure.isError():
            print('Error reading start below pressure')
        else:
            answer = start_below_pressure.registers
            start_below_pressure = int(answer[0])*0.01
    else:
        client.connect()
        start_below_pressure = client.read_holding_registers(119, 1)
        answer = start_below_pressure.registers
        start_below_pressure = int(answer[0])*0.01
    return start_below_pressure

def read_max_cell_voltage(client):
    # Read max cell voltage
    max_cell_voltage = -1
    if client.is_socket_open():
        max_cell_voltage = client.read_holding_registers(121, 1) # normalement c'est le registre 122. Il semble y avoir un problème
        if max_cell_voltage.isError():
            print('Error reading max cell voltage')
        else:
            answer = max_cell_voltage.registers
            max_cell_voltage = int(answer[0])*0.1
    else:
        client.connect()
        max_cell_voltage = client.read_holding_registers(121, 1)
        answer = max_cell_voltage.registers
        max_cell_voltage = int(answer[0])*0.1
    return max_cell_voltage


def set_mode(client):
    # set mode to 0 (OFF) or 1 (ON)
    set_mode = -1
    if client.is_socket_open():
        mode = client.write_register(102, 0) #registre 103: mode
        if mode.isError():
            print('Error set current')
            print(mode)
        else:
            print(mode)
    return set_mode

def set_current(client):
    set_current = -1
    if client.is_socket_open():
        set_current = client.write_register(103, 710) # cette valeur assets été prise dans le registre 104: I_setpoint
        if set_current.isError():
            print('Error starting')
            print(set_current)
        else:
            print(set_current)
    return set_current

##def set_stop_after_pressure(client):
##    # set "stop after" pressure
##    set_stop_after_pressure = -1
##    if client.is_socket_open():
##        set_stop_after_pressure = client.write_register(120, 4000) #registre 120: stop_after_pressure
##        if set_stop_after_pressure.isError():
##            print('Error set stop_after_pressure')
##            print(set_stop_after_pressure)
##        else:
##            print(set_stop_after_pressure)
##    return set_stop_after_pressure
    
##def set_start_below_pressure(client):
##    # set "start below" pressure
##    set_start_below_pressure = -1
##    if client.is_socket_open():
##        set_start_below_pressure = client.write_register(119, 4000) #registre 119: start_below_pressure
##        if set_start_below_pressure.isError():
##            print('Error set stop_after_pressure')
##            print(set_start_below_pressure)
##        else:
##            print(set_start_below_pressure)
##    else:
##        client.connect()
##        set_start_below_pressure = client.write_register(119, 4000) #registre 119: start_below_pressure
##        answer = set_start_below_pressure.registers
##        set_start_below_pressure = int(answer[0])*0.01
##    return set_start_below_pressure


def close(client):
    # Exit
    print('Closing connection to external system...')
    client.close()
