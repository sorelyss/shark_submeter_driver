# Measurement and report system of the generation of two sources of renewable energies at universidad del norte to the UNINOC management center
Here are the scripts of the Communication module for acquisition of the measurements from the energy meter Shark Submeter line.

## Setup the communication module
In order to replicate the module in another sources you should create a table in the database and an URL where the module will send all the acquired data. The URLs should have the following format:

```python
url = 'http://{IP}/measurements/{meter_id}_{measurement_type}/new?{msg}&created_at={date}'.format(IP=123.123.123.123,
                                                                                                  meter_id=METER_ID, 
                                                                                                  measurement_type=measurement_type, 
                                                                                                  msg=message, 
                                                                                                  date=date.now())
```
In the main.py file you should change the ```METER_ID = 'shark_NAME'``` for the name of the URL you created. You also need to change the ```data_struc``` dictionary based on the variable names of the URLs you created.

```python
# Set variables for each type of measurement
# name of measurement_type: list of variable url names, list of variable register table names
data_struc = {'powers': [['power_watt_mpk', 'power_va_mpk', 'power_var_mpk'], ['P_P', 'P_S', 'P_Q']],
              'energies': [['energy_watt_mpk', 'energy_va_mpk', 'energy_var_mpk'], ['E_P', 'E_S', 'E_Q']],
              'variables': [['voltage_mpk', 'p_voltage', 'current_mpk', 'p_current', 'freq_mpk', 'pf_mpk'], ['V_AN', 'dV_AB', 'I_A', 'dI_A', 'F', 'PF']],
              }
```

### Shark 100S
```python
register_table = {'V_AB': 1005, 'V_BC': 1007, 'V_CA': 1009,
                  'dV_AB': 4102, 'dV_BC': 4103, 'dV_CA': 4104,

                  'V_AN': 999, 'V_BN': 1001, 'V_CN': 1003,

                  'I_A': 1011, 'I_B': 1013, 'I_C': 1015,
                  'dI_A': 4099, 'dI_B': 4100, 'dI_C': 4101,

                  'P_P': 1017, 'P_Q': 1019, 'P_S': 1021,
                  'PF': 1023, 'F': 1025,
                  'E_P': 1105, 'E_Q': 1113, 'E_S': 1115
                }
```

### Shark 200S
```python
register_table = {'V_AB': 1005, 'V_BC': 1007, 'V_CA': 1009,
                  'dV_AB': 4102, 'dV_BC': 4103, 'dV_CA': 4104,

                  'V_AN': 999, 'V_BN': 1001, 'V_CN': 1003,

                  'I_A': 1011, 'I_B': 1013, 'I_C': 1015,
                  'dI_A': 4099, 'dI_B': 4100, 'dI_C': 4101,

                  'P_P': 1017, 'P_Q': 1019, 'P_S': 1021,
                  'PF': 1023, 'F': 1025,
                  'E_P': 1505, 'E_Q': 1513, 'E_S': 1515
                }
```

## Setup Raspberry Pi Zero
To launch the main.py script on each startup of the raspberry it is necessary to create a cron service. You can follow the steps of [this link](http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/).
The crontab file should look like:
```bash
@reboot sh /home/pi/Documents/lab_renovables/run_main.sh >/home/pi/logs/cronlog 2>&1
```


