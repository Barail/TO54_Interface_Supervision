from pyModbusTCP.client import ModbusClient

def connect_to_external_system(ip):
    c = ModbusClient(host=ip, port=502, unit_id=1, auto_open=True)
    print('connection success')
    return c

def read_number_of_batteries(c):
    regs = c.read_holding_registers(1286, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_number_of_batteries_parallel(c):
    regs = c.read_holding_registers(1287, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_number_of_batteries_series(c):
    regs = c.read_holding_registers(1288, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_number_of_cells_per_batteries(c):
    regs = c.read_holding_registers(1289, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_minimum_cell_voltage(c):
    regs = c.read_holding_registers(1290, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_maximum_cell_voltage(c):
    regs = c.read_holding_registers(1291, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_battery_state(c):
    regs = c.read_holding_registers(1282, 3)
    if regs:
        if regs == 0:
            return "Init - Wait Start"
        elif regs == 1:
            return "Init - Before Boot"
        elif regs == 2:
            return "Init - Before Boot Delay"
        elif regs == 3:
            return "Init - Wait Boot"
        elif regs == 4:
            return "Init - Initializing"
        elif regs == 5:
            return "Init - Measure Battery Voltage"
        elif regs == 6:
            return "Init - Calculate Battery Voltage"
        elif regs == 7:
            return "Init - Wait Bus Voltage"
        elif regs == 8:
            return "Init - Wait for lynx shunt"
        elif regs == 9:
            return "Running"
        elif regs == 10:
            return "Error"
        elif regs == 11:
            return "Unused"
        elif regs == 12:
            return "Shutdown"
        elif regs == 13:
            return "Slave updating"
        elif regs == 14:
            return "Standby"
        elif regs == 15:
            return "Going to run"
        elif regs == 15:
            return "Pre-charging"
        print(regs)

    return "regs not read !"

def read_charger_Voltage_Output1(c):
    regs = c.read_holding_registers(2307, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_Current_Output1(c):
    regs = c.read_holding_registers(2308, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_Voltage_Output2(c):
    regs = c.read_holding_registers(2309, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_Current_Output2(c):
    regs = c.read_holding_registers(2310, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_Voltage_Output3(c):
    regs = c.read_holding_registers(2311, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_Current_Output3(c):
    regs = c.read_holding_registers(2312, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_AC_Current(c):
    regs = c.read_holding_registers(2314, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_AC_Power(c):
    regs = c.read_holding_registers(2315, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_charger_AC_Current_Limit(c):
    regs = c.read_holding_registers(2316, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_evcharger_chargingtime(c):
    regs = c.read_holding_registers(3822, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_grid_L1_Power(c):
    regs = c.read_holding_registers(2600, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_grid_L2_Power(c):
    regs = c.read_holding_registers(2601, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs

def read_grid_L3_Power(c):
    regs = c.read_holding_registers(2602, 3)
    if regs:
        print(regs)
    else:
        print("read error")

    return regs
