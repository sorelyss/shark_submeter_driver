"""Main file for acquisition and sending of SharkMeter data"""
import os
import time
import minimalmodbus
import requests
from datetime import datetime as date

def get_data_from_shark(variable):
    """Get the data from SharkMeter"""
    if 'd' in variable:
        return SharkMeter.read_register(register_table[variable], 2, 3, True)
    elif 'E_' in variable:
        return SharkMeter.read_long(register_table[variable], 3, True)/1000.0
    elif 'P_' in variable:
        return SharkMeter.read_float(register_table[variable], 3, 2)/1000.0
    else:
        return SharkMeter.read_float(register_table[variable], 3, 2)

def get_data(variable):
    """Get the data from SharMeter clean"""
    success = 0
    for i in range(10):
       try:
          data = get_data_from_shark(variable)
          print('data',data)
       except Exception as e:
          print('Exception getting the data: ',variable,', try: ', i)
          print('Exception: ', e)
          time.sleep(i+1)
       else:
          success += 1
          # Case: even though it reads, the buffer is not refreshed.
          if success>1:
              return data
    #If after 3 times do not work, retun None

def send_data(measurement_type, message):
    """Send the data from SharkMeter to UniNOC"""
    url = 'http://138.197.104.91/measurements/{meter_id}_{measurement_type}/new?{msg}&created_at={date}'.format(meter_id=METER_ID, 
                                                                                                               measurement_type=measurement_type, 
                                                                                                               msg=message, 
                                                                                                               date=date.now())
    response = requests.get(url, auth=requests.auth.HTTPBasicAuth('admin', 'uninorte'))
    if response.status_code != 200:
        DATA_BUFFER.append(url)
    elif len(DATA_BUFFER)>0:
        for data in DATA_BUFFER:
            requests.get(data, auth=requests.auth.HTTPBasicAuth('admin', 'uninorte'))
        DATA_BUFFER = []
    return response


def main(SharkMeter, data_struc):
    for measurement_type in data_struc.keys():
        message = ''
        for i, variable in enumerate(data_struc[measurement_type][1]):
            meassure = get_data(variable)
            print('--------',variable, meassure)
            if i==0:
                start = ''
            else:
                start = '&'
            message += '{conj}{var_name}={meassure}'.format(conj=start, var_name=data_struc[measurement_type][0][i], meassure=meassure)
        status = send_data(measurement_type, message)
        print('-- Sending status:',status)


if __name__ == "__main__":
    # ID of the meter for UniNOC
    METER_ID = 'shark_panels'

    register_table = {'V_AB': 1005, 'V_BC': 1007, 'V_CA': 1009,
                      'dV_AB': 4102, 'dV_BC': 4103, 'dV_CA': 4104,

                      'V_AN': 999, 'V_BN': 1001, 'V_CN': 1003,

                      'I_A': 1011, 'I_B': 1013, 'I_C': 1015,
                      'dI_A': 4099, 'dI_B': 4100, 'dI_C': 4101,

                      'P_P': 1017, 'P_Q': 1019, 'P_S': 1021,
                      'PF': 1023, 'F': 1025,
                      'E_P': 1505, 'E_Q': 1513, 'E_S': 1515
                    }
    
    # Data buffer that handles no internet case
    DATA_BUFFER = []
    
    # Create instance of SharkMeter
    SharkMeter = minimalmodbus.Instrument('/dev/serial0', 1) # port name, slave add$

    # Set variables for each type of measurement
    # name of measurement_type: list of variable url names, list of variable register table names
    data_struc = {'power': [['power_watt', 'power_va', 'power_var'], ['P_P', 'P_S', 'P_Q']],
                  'energy': [['energy_watt', 'energy_va', 'energy_var'], ['E_P', 'E_S', 'E_Q']],
                  'frequency': [['freqy', 'pfactor'], ['F', 'PF']],
                  'phase_voltages': [['voltage_a', 'voltage_b', 'voltage_c'], ['V_AN', 'V_BN', 'V_CN']],
                  'line_voltages': [['voltage_ab', 'phase_ab', 'voltage_bc', 'phase_bc', 'voltage_ca', 'phase_ca'], ['V_AB', 'dV_AB', 'V_BC', 'dV_BC', 'V_CA', 'dV_CA']],
                  'currents': [['current_a', 'phase_a', 'current_b', 'phase_b', 'current_c', 'phase_c'], ['I_A', 'dI_A', 'I_B', 'dI_B', 'I_C', 'dI_C']]
                  }

    while True:
        try:
            main(SharkMeter, data_struc)
        except Exception as e:
            SharkMeter = minimalmodbus.Instrument('/dev/serial0', 1) # port name, slave add$
            print('----Alert: An exception occurred. The communication was restore.----')
        else:
            time.sleep(50)
