#ENABLES CORRECT DIVISION IN PYTHON
from __future__ import division

#IMPORT MODULES USED BY THE SCRIPT
import pandas as pd
import itertools
import numpy as np
import CoolProp
import CoolProp.CoolProp as CP
from itertools import product
from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import *
init_notebook_mode(connected=False)


#CREATES THE R123 DATASETS
r123_temp_1 = pd.Series(range(1,110))
r123_temp_3 = pd.Series(range(1,110))

r123_data_1 = pd.DataFrame(r123_temp_1)
r123_data_1 = r123_data_1.rename(columns = {0:'T_1'})

r123_data_3 = pd.DataFrame(r123_temp_3)
r123_data_3 = r123_data_3.rename(columns = {0:'T_3'})

r123_data_1['REFRIGERANT']= 'R123'
r123_data_3['REFRIGERANT']= 'R123'

r123_data_1['T_1_K']= r123_data_1['T_1'] + 273.15
r123_data_3['T_3_K']= r123_data_3['T_3'] + 273.15

#
r123_data = pd.concat([r123_data_1, r123_data_3], axis=1)
r123_data_randomized = pd.DataFrame(list(product(r123_data.T_1_K, r123_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r123_data_randomized.insert(0, 'REFRIGERANT', 'R123')

r123_data_randomized['T_1']= r123_data_randomized['T_1_K'] - 273.15
r123_data_randomized['T_3']= r123_data_randomized['T_3_K'] - 273.15


#CREATES THE R134a DATASETS
r134a_temp_1 = pd.Series(range(1,101))
r134a_temp_3 = pd.Series(range(1,101))

r134a_data_1 = pd.DataFrame(r134a_temp_1)
r134a_data_1 = r134a_data_1.rename(columns = {0:'T_1'})

r134a_data_3 = pd.DataFrame(r134a_temp_3)
r134a_data_3 = r134a_data_3.rename(columns = {0:'T_3'})

r134a_data_1['REFRIGERANT']= 'R134a'
r134a_data_3['REFRIGERANT']= 'R134a'

r134a_data_1['T_1_K']= r134a_data_1['T_1'] + 273.15
r134a_data_3['T_3_K']= r134a_data_3['T_3'] + 273.15

#
r134a_data = pd.concat([r134a_data_1, r134a_data_3], axis=1)
r134a_data_randomized = pd.DataFrame(list(product(r134a_data.T_1_K, r134a_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r134a_data_randomized.insert(0, 'REFRIGERANT', 'R134a')

r134a_data_randomized['T_1']= r134a_data_randomized['T_1_K'] - 273.15
r134a_data_randomized['T_3']= r134a_data_randomized['T_3_K'] - 273.15


#CREATES THE R141b DATASETS
r141b_temp_1 = pd.Series(range(1,205))
r141b_temp_3 = pd.Series(range(1,205))

r141b_data_1 = pd.DataFrame(r141b_temp_1)
r141b_data_1 = r141b_data_1.rename(columns = {0:'T_1'})

r141b_data_3 = pd.DataFrame(r141b_temp_3)
r141b_data_3 = r141b_data_3.rename(columns = {0:'T_3'})

r141b_data_1['REFRIGERANT']= 'R141b'
r141b_data_3['REFRIGERANT']= 'R141b'

r141b_data_1['T_1_K']= r141b_data_1['T_1'] + 273.15
r141b_data_3['T_3_K']= r141b_data_3['T_3'] + 273.15

#
r141b_data = pd.concat([r141b_data_1, r141b_data_3], axis=1)
r141b_data_randomized = pd.DataFrame(list(product(r141b_data.T_1_K, r141b_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r141b_data_randomized.insert(0, 'REFRIGERANT', 'R141b')

r141b_data_randomized['T_1']= r141b_data_randomized['T_1_K'] - 273.15
r141b_data_randomized['T_3']= r141b_data_randomized['T_3_K'] - 273.15


#CREATES THE R410a DATASETS
r410a_temp_1 = pd.Series(range(1,71))
r410a_temp_3 = pd.Series(range(1,71))

r410a_data_1 = pd.DataFrame(r410a_temp_1)
r410a_data_1 = r410a_data_1.rename(columns = {0:'T_1'})

r410a_data_3 = pd.DataFrame(r410a_temp_3)
r410a_data_3 = r410a_data_3.rename(columns = {0:'T_3'})

r410a_data_1['REFRIGERANT']= 'R410a'
r410a_data_3['REFRIGERANT']= 'R410a'

r410a_data_1['T_1_K']= r410a_data_1['T_1'] + 273.15
r410a_data_3['T_3_K']= r410a_data_3['T_3'] + 273.15

#
r410a_data = pd.concat([r410a_data_1, r410a_data_3], axis=1)
r410a_data_randomized = pd.DataFrame(list(product(r410a_data.T_1_K, r410a_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r410a_data_randomized.insert(0, 'REFRIGERANT', 'R410a')

r410a_data_randomized['T_1']= r410a_data_randomized['T_1_K'] - 273.15
r410a_data_randomized['T_3']= r410a_data_randomized['T_3_K'] - 273.15


#CREATES THE R113 DATASETS
r113_temp_1 = pd.Series(range(1,214))
r113_temp_3 = pd.Series(range(1,214))

r113_data_1 = pd.DataFrame(r113_temp_1)
r113_data_1 = r113_data_1.rename(columns = {0:'T_1'})

r113_data_3 = pd.DataFrame(r113_temp_3)
r113_data_3 = r113_data_3.rename(columns = {0:'T_3'})

r113_data_1['REFRIGERANT']= 'R113'
r113_data_3['REFRIGERANT']= 'R113'

r113_data_1['T_1_K']= r113_data_1['T_1'] + 273.15
r113_data_3['T_3_K']= r113_data_3['T_3'] + 273.15

#
r113_data = pd.concat([r113_data_1, r113_data_3], axis=1)
r113_data_randomized = pd.DataFrame(list(product(r113_data.T_1_K, r113_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r113_data_randomized.insert(0, 'REFRIGERANT', 'R113')

r113_data_randomized['T_1']= r113_data_randomized['T_1_K'] - 273.15
r113_data_randomized['T_3']= r113_data_randomized['T_3_K'] - 273.15


#CREATES THE R236ea DATASETS
r236ea_temp_1 = pd.Series(range(1,140))
r236ea_temp_3 = pd.Series(range(1,140))

r236ea_data_1 = pd.DataFrame(r236ea_temp_1)
r236ea_data_1 = r236ea_data_1.rename(columns = {0:'T_1'})

r236ea_data_3 = pd.DataFrame(r236ea_temp_3)
r236ea_data_3 = r236ea_data_3.rename(columns = {0:'T_3'})

r236ea_data_1['REFRIGERANT']= 'R236ea'
r236ea_data_3['REFRIGERANT']= 'R236ea'

r236ea_data_1['T_1_K']= r236ea_data_1['T_1'] + 273.15
r236ea_data_3['T_3_K']= r236ea_data_3['T_3'] + 273.15

#
r236ea_data = pd.concat([r236ea_data_1, r236ea_data_3], axis=1)
r236ea_data_randomized = pd.DataFrame(list(product(r236ea_data.T_1_K, r236ea_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r236ea_data_randomized.insert(0, 'REFRIGERANT', 'R236ea')

r236ea_data_randomized['T_1']= r236ea_data_randomized['T_1_K'] - 273.15
r236ea_data_randomized['T_3']= r236ea_data_randomized['T_3_K'] - 273.15


#CREATES THE R227ea DATASETS
r227ea_temp_1 = pd.Series(range(1,101))
r227ea_temp_3 = pd.Series(range(1,101))

r227ea_data_1 = pd.DataFrame(r227ea_temp_1)
r227ea_data_1 = r227ea_data_1.rename(columns = {0:'T_1'})

r227ea_data_3 = pd.DataFrame(r227ea_temp_3)
r227ea_data_3 = r227ea_data_3.rename(columns = {0:'T_3'})

r227ea_data_1['REFRIGERANT']= 'R227ea'
r227ea_data_3['REFRIGERANT']= 'R227ea'

r227ea_data_1['T_1_K']= r227ea_data_1['T_1'] + 273.15
r227ea_data_3['T_3_K']= r227ea_data_3['T_3'] + 273.15

#
r227ea_data = pd.concat([r227ea_data_1, r227ea_data_3], axis=1)
r227ea_data_randomized = pd.DataFrame(list(product(r227ea_data.T_1_K, r227ea_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r227ea_data_randomized.insert(0, 'REFRIGERANT', 'R227ea')

r227ea_data_randomized['T_1']= r227ea_data_randomized['T_1_K'] - 273.15
r227ea_data_randomized['T_3']= r227ea_data_randomized['T_3_K'] - 273.15


#CREATES THE R600a DATASETS
r600a_temp_1 = pd.Series(range(1,134))
r600a_temp_3 = pd.Series(range(1,134))

r600a_data_1 = pd.DataFrame(r600a_temp_1)
r600a_data_1 = r600a_data_1.rename(columns = {0:'T_1'})

r600a_data_3 = pd.DataFrame(r600a_temp_3)
r600a_data_3 = r600a_data_3.rename(columns = {0:'T_3'})

r600a_data_1['REFRIGERANT']= 'R600a'
r600a_data_3['REFRIGERANT']= 'R600a'

r600a_data_1['T_1_K']= r600a_data_1['T_1'] + 273.15
r600a_data_3['T_3_K']= r600a_data_3['T_3'] + 273.15

#
r600a_data = pd.concat([r600a_data_1, r600a_data_3], axis=1)
r600a_data_randomized = pd.DataFrame(list(product(r600a_data.T_1_K, r600a_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r600a_data_randomized.insert(0, 'REFRIGERANT', 'R600a')

r600a_data_randomized['T_1']= r600a_data_randomized['T_1_K'] - 273.15
r600a_data_randomized['T_3']= r600a_data_randomized['T_3_K'] - 273.15


#CREATES THE R245ca DATASETS
r245ca_temp_1 = pd.Series(range(1,175))
r245ca_temp_3 = pd.Series(range(1,175))

r245ca_data_1 = pd.DataFrame(r245ca_temp_1)
r245ca_data_1 = r245ca_data_1.rename(columns = {0:'T_1'})

r245ca_data_3 = pd.DataFrame(r245ca_temp_3)
r245ca_data_3 = r245ca_data_3.rename(columns = {0:'T_3'})

r245ca_data_1['REFRIGERANT']= 'R245ca'
r245ca_data_3['REFRIGERANT']= 'R245ca'

r245ca_data_1['T_1_K']= r245ca_data_1['T_1'] + 273.15
r245ca_data_3['T_3_K']= r245ca_data_3['T_3'] + 273.15

#
r245ca_data = pd.concat([r245ca_data_1, r245ca_data_3], axis=1)
r245ca_data_randomized = pd.DataFrame(list(product(r245ca_data.T_1_K, r245ca_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r245ca_data_randomized.insert(0, 'REFRIGERANT', 'R245ca')

r245ca_data_randomized['T_1']= r245ca_data_randomized['T_1_K'] - 273.15
r245ca_data_randomized['T_3']= r245ca_data_randomized['T_3_K'] - 273.15


#CREATES THE R11 DATASETS
r11_temp_1 = pd.Series(range(1,198))
r11_temp_3 = pd.Series(range(1,198))

r11_data_1 = pd.DataFrame(r11_temp_1)
r11_data_1 = r11_data_1.rename(columns = {0:'T_1'})

r11_data_3 = pd.DataFrame(r11_temp_3)
r11_data_3 = r11_data_3.rename(columns = {0:'T_3'})

r11_data_1['REFRIGERANT']= 'R11'
r11_data_3['REFRIGERANT']= 'R11'

r11_data_1['T_1_K']= r11_data_1['T_1'] + 273.15
r11_data_3['T_3_K']= r11_data_3['T_3'] + 273.15

#
r11_data = pd.concat([r11_data_1, r11_data_3], axis=1)
r11_data_randomized = pd.DataFrame(list(product(r11_data.T_1_K, r11_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r11_data_randomized.insert(0, 'REFRIGERANT', 'R11')

r11_data_randomized['T_1']= r11_data_randomized['T_1_K'] - 273.15
r11_data_randomized['T_3']= r11_data_randomized['T_3_K'] - 273.15


#CREATES THE R218 DATASETS
r218_temp_1 = pd.Series(range(1,72))
r218_temp_3 = pd.Series(range(1,72))

r218_data_1 = pd.DataFrame(r218_temp_1)
r218_data_1 = r218_data_1.rename(columns = {0:'T_1'})

r218_data_3 = pd.DataFrame(r218_temp_3)
r218_data_3 = r218_data_3.rename(columns = {0:'T_3'})

r218_data_1['REFRIGERANT']= 'R218'
r218_data_3['REFRIGERANT']= 'R218'

r218_data_1['T_1_K']= r218_data_1['T_1'] + 273.15
r218_data_3['T_3_K']= r218_data_3['T_3'] + 273.15

#
r218_data = pd.concat([r218_data_1, r218_data_3], axis=1)
r218_data_randomized = pd.DataFrame(list(product(r218_data.T_1_K, r218_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r218_data_randomized.insert(0, 'REFRIGERANT', 'R218')

r218_data_randomized['T_1']= r218_data_randomized['T_1_K'] - 273.15
r218_data_randomized['T_3']= r218_data_randomized['T_3_K'] - 273.15


#CREATES THE R245fa DATASETS
r245fa_temp_1 = pd.Series(range(1,154))
r245fa_temp_3 = pd.Series(range(1,154))

r245fa_data_1 = pd.DataFrame(r245fa_temp_1)
r245fa_data_1 = r245fa_data_1.rename(columns = {0:'T_1'})

r245fa_data_3 = pd.DataFrame(r245fa_temp_3)
r245fa_data_3 = r245fa_data_3.rename(columns = {0:'T_3'})

r245fa_data_1['REFRIGERANT']= 'R245fa'
r245fa_data_3['REFRIGERANT']= 'R245fa'

r245fa_data_1['T_1_K']= r245fa_data_1['T_1'] + 273.15
r245fa_data_3['T_3_K']= r245fa_data_3['T_3'] + 273.15

#
r245fa_data = pd.concat([r245fa_data_1, r245fa_data_3], axis=1)
r245fa_data_randomized = pd.DataFrame(list(product(r245fa_data.T_1_K, r245fa_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r245fa_data_randomized.insert(0, 'REFRIGERANT', 'R245fa')

r245fa_data_randomized['T_1']= r245fa_data_randomized['T_1_K'] - 273.15
r245fa_data_randomized['T_3']= r245fa_data_randomized['T_3_K'] - 273.15


#CREATES THE R236fa DATASETS
r236fa_temp_1 = pd.Series(range(1,125))
r236fa_temp_3 = pd.Series(range(1,125))

r236fa_data_1 = pd.DataFrame(r236fa_temp_1)
r236fa_data_1 = r236fa_data_1.rename(columns = {0:'T_1'})

r236fa_data_3 = pd.DataFrame(r236fa_temp_3)
r236fa_data_3 = r236fa_data_3.rename(columns = {0:'T_3'})

r236fa_data_1['REFRIGERANT']= 'R236fa'
r236fa_data_3['REFRIGERANT']= 'R236fa'

r236fa_data_1['T_1_K']= r236fa_data_1['T_1'] + 273.15
r236fa_data_3['T_3_K']= r236fa_data_3['T_3'] + 273.15

#
r236fa_data = pd.concat([r236fa_data_1, r236fa_data_3], axis=1)
r236fa_data_randomized = pd.DataFrame(list(product(r236fa_data.T_1_K, r236fa_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r236fa_data_randomized.insert(0, 'REFRIGERANT', 'R236fa')

r236fa_data_randomized['T_1']= r236fa_data_randomized['T_1_K'] - 273.15
r236fa_data_randomized['T_3']= r236fa_data_randomized['T_3_K'] - 273.15


#CREATES THE R600 DATASETS
r600_temp_1 = pd.Series(range(1,152))
r600_temp_3 = pd.Series(range(1,152))

r600_data_1 = pd.DataFrame(r600_temp_1)
r600_data_1 = r600_data_1.rename(columns = {0:'T_1'})

r600_data_3 = pd.DataFrame(r600_temp_3)
r600_data_3 = r600_data_3.rename(columns = {0:'T_3'})

r600_data_1['REFRIGERANT']= 'R600'
r600_data_3['REFRIGERANT']= 'R600'

r600_data_1['T_1_K']= r600_data_1['T_1'] + 273.15
r600_data_3['T_3_K']= r600_data_3['T_3'] + 273.15

#
r600_data = pd.concat([r600_data_1, r600_data_3], axis=1)
r600_data_randomized = pd.DataFrame(list(product(r600_data.T_1_K, r600_data.T_3_K)), columns=['T_1_K', 'T_3_K'])
r600_data_randomized.insert(0, 'REFRIGERANT', 'R600')

r600_data_randomized['T_1']= r600_data_randomized['T_1_K'] - 273.15
r600_data_randomized['T_3']= r600_data_randomized['T_3_K'] - 273.15




#COMBINES THE REFRIGERANT DATASETS
data = pd.concat([r134a_data_randomized, r141b_data_randomized,
                  r410a_data_randomized, r113_data_randomized,
                  r236ea_data_randomized, r227ea_data_randomized,
                  r600a_data_randomized, r245ca_data_randomized,
                  r11_data_randomized, r218_data_randomized,
                  r245fa_data_randomized, r236fa_data_randomized,
                  r600_data_randomized, r123_data_randomized])


data['T_4_K'] = data['T_1_K']

#CALCULATES THE PRESSURE VALUES AT STATE 1
def calculate_pressure_1(row):
    return (PropsSI('P', 'T', row[1], 'Q', 0, row[0]))

data.apply(calculate_pressure_1, axis=1)
data.apply(calculate_pressure_1, axis=1)

data['P_1'] = data.apply(calculate_pressure_1, axis=1)


#CALCULATES THE PRESSURE VALUES AT STATE 3
def calculate_pressure_3(row):
    return (PropsSI('P', 'T', row[2], 'Q', 0, row[0]))

data.apply(calculate_pressure_3, axis=1)

data['P_3'] = data.apply(calculate_pressure_3, axis=1)

#
data['P_4'] = data['P_1']
data['P_2'] = data['P_3']


#CALCULATE THE ENTROPY VALUES AT STATE 1
def calculate_entropy_1(row):
    return (PropsSI('S', 'T', row[1], 'Q', 0, row[0]))

data.apply(calculate_entropy_1, axis=1)
data['S_1'] = data.apply(calculate_entropy_1, axis=1)


#CALCULATE THE ENTHALPY VALUES AT STATE 1
def calculate_enthalpy_1(row):
    return (PropsSI('H', 'T', row[1], 'Q', 0, row[0]))

data.apply(calculate_enthalpy_1, axis=1)
data['H_1'] = data.apply(calculate_enthalpy_1, axis=1)
data['H_1'] = (data['H_1'] / 1000)



#CALCULATE THE ENTROPY VALUES AT STATE 3
def calculate_entropy_3(row):
    return (PropsSI('S', 'T', row[2], 'Q', 1, row[0]))

data.apply(calculate_entropy_3, axis=1)
data['S_3'] = data.apply(calculate_entropy_3, axis=1)


#CALCULATE THE ENTHALPY VALUES AT STATE 3
def calculate_enthalpy_3(row):
    return (PropsSI('H', 'T', row[2], 'Q', 1, row[0]))

data.apply(calculate_enthalpy_3, axis=1)
data['H_3'] = data.apply(calculate_enthalpy_3, axis=1)
data['H_3'] = (data['H_3'] / 1000)


#
data['S_2'] = data['S_1']
data['S_4'] = data['S_3']


#CALCULATES THE TEMPERATURE VALUES AT STATE 2
def calculate_temp_2(row):
    return PropsSI('T', 'P', row[9], 'S', row[14], row[0])

data.apply(calculate_temp_2, axis=1)
data['T_2_K'] = data.apply(calculate_temp_2, axis=1)


#CALCULATE THE ISENTROPIC ENTHALPY VALUES AT STATE 2
def calculate_isentropic_enthalpy_2(row):
    return PropsSI('H', 'P', row[9], 'S', row[14], row[0])

x = data.apply(calculate_isentropic_enthalpy_2, axis=1)

data['H_2_ISENTROPIC'] = x
data['H_2_ISENTROPIC'] = data['H_2_ISENTROPIC'] / 1000


#CALCULATES THE ISENTROPIC ENTHALPY VALUES AT STATE 4
def calculate_isentropic_enthalpy_4(row):
    return PropsSI('H', 'P', row[8], 'S', row[15], row[0])

y = data.apply(calculate_isentropic_enthalpy_4, axis=1)

data['H_4_ISENTROPIC'] = y
data['H_4_ISENTROPIC'] = data['H_4_ISENTROPIC'] / 1000


#CALCULATES THE TEMPERATURE VALUES AT STATE 4
def calculate_temp_4(row):
    return PropsSI('T', 'P', row[6], 'S', row[15], row[0])

dz2.apply(calculate_temp_4, axis=1)
dz2['T_4_K'] = dz2.apply(calculate_temp_4, axis=1)

#OUTPUTS THE DATAFRAME TO CSV
data.to_csv('/Users/nialdaly/orcprogram/refrigerant_data.csv', index=False)