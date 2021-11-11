
from pyModbusTCP.client import ModbusClient

def connect_to_external_system(ip):
    c = ModbusClient(host=ip, port=502, unit_id=1, auto_open=True)
    print('connection success')
    return c

def read_frequency(c):
    regs = c.read_holding_registers(36871, 2)
    if regs:
        print(regs)
    else:
        print("read error")

    freq = int(regs[1])/1000
    return freq

def read_power_tri(c):
    regs = c.read_holding_registers(18476, 2) #puissance active totale triphasé [W]
    if regs:
        print(regs)
    else:
        print("read error")

    puissance_centrale_tri = int(regs[1])
    print(puissance_centrale_tri)
    return puissance_centrale_tri
    


def read_energy_tri(c):
    regs = c.read_holding_registers(19843, 2) #energie totale positive active triphasé [kWh]
    if regs:
        print(regs)
    else:
        print("read error")

    energie_centrale_tri = int(regs[1])
    print(energie_centrale_tri)
    return energie_centrale_tri


def read_current_tri(c):
    regs = c.read_holding_registers(18440, 2) #courant système triphasé [A]
    if regs:
        print(regs)
    else:
        print("read error")

    courant_centrale_tri = int(regs[1])/1000
    return courant_centrale_tri

def read_ph_n_voltage_tri(c):
    regs = c.read_holding_registers(18436, 2) #tension phase-neutre système triphasé [V]
    if regs:
        print(regs)
    else:
        print("read error")

    tens_ph_n_centrale_tri = int(regs[1])/100
    return tens_ph_n_centrale_tri



