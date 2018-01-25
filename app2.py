# -*- coding: utf-8 -*-
#ENABLES CORRECT DIVISION IN PYTHON
from __future__ import division

import dash
import dash_core_components as dcc
import dash_html_components as html
#import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import plotly
import base64
import urllib


app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True


df = pd.read_csv('https://github.com/ndaly06/orcprogram/blob/master/refrigerant_data.csv?raw=true')
df2 = df[['REFRIGERANT', 'T_1_K', 'T_3_K', 'H_1', 'H_2_ISENTROPIC', 'H_3', 'H_4_ISENTROPIC']]
df2 = df2.round(2)

tab1_layout = html.Div([
	html.Div([
                html.Label('ORC System Schematic'),
                html.Img(src='https://github.com/ndaly06/orcprogram/blob/master/orcschematic3.png?raw=true',
                    style={
                    'max-height': '250px',
                    'max-width': '500px',
                    'position':'relative'}),

            ],
            className='row',
                style={'margin-bottom': '20'}

            ),

	])


tab2_layout = html.Div([

	html.H6('Input Parameters'),
	html.Hr(style={'margin': '0', 'margin-bottom': '2'}),

	html.Label('Organic Rankine Cycle Configuration:'),
                dcc.Dropdown(
                    id='dropdown_1',
                    placeholder='Subcritical',
                    disabled=True,
                ),

    html.Label('Heat Source:'),
                dcc.Dropdown(
                    id='dropdown_2',
                    placeholder='Geothermal Water',
                    disabled=True,
                ),

    html.Label('Select Refrigerant:'),
                dcc.Dropdown(
                    id='dropdown_3',
                    options=[{'label': i, 'value': i} for i in df.REFRIGERANT.unique()],
                    placeholder='Select Refrigerant',
                    multi=True,
                    value=['R134a', 'R141b', 'R410a', 'R113'],
                ),

    html.Label('Mass Flow Rate (kg/s)',style={'width': '200'}),
                dcc.Input(
                            id='input_1',
                            type='number',
                            value='12',
                            min='1',
                            style={'max-width': '150px'}
                        ),

    html.Label(id='pump_temp_value'),
           dcc.Slider(
                        id='slider_1',
                        min=1,
                        max=200,
                        step=1,
                        value=10
                        ),

    html.Label(id='turbine_temp_value'),
                    dcc.Slider(
                        id='slider_2',
                        min=1,
                        max=200,
                        value=60,
                    ),

                html.Label(
                        id='pump_eff_value'),
                    dcc.Slider(
                        id='slider_3',
                        min=1,
                        max=100,
                        value=60,
                    ),

                html.Label(
                        id='turbine_eff_value'),
                    dcc.Slider(
                        id='slider_4',
                        min=1,
                        max=100,
                        value=80,
                    ),

                html.Hr(style={'margin': '2', 'margin-bottom': '2'}),

                html.H6('Model Results'),

                html.Hr(style={'margin': '2', 'margin-bottom': '2'}),


                html.Div([




                html.Div([
                	dcc.Graph(id='graph1', config={'displayModeBar': False}, style={'max-height': '350', 'height': '40vh'}),
                	],
                	className='five columns'
                	),

                html.Div([
                	dcc.Graph(id='graph2', config={'displayModeBar': False}, style={'max-height': '350', 'height': '40vh'}),
                	],
                	className='seven columns'
                	),

                ],
                className='row',
                style={'margin-bottom': '20'}
                )
                ]),


tab3_layout = html.Div([

	html.H6('Parametric Analysis'),
	html.Hr(style={'margin': '0', 'margin-bottom': '2'}),

    html.Label('Select Refrigerant:'),
                dcc.Dropdown(
                    id='dropdown_3',
                    options=[{'label': i, 'value': i} for i in df.REFRIGERANT.unique()],
                    placeholder='Select Refrigerant',
                    multi=True,
                    value=['R134a', 'R141b', 'R410a', 'R113'],
                ),

    html.Label('Mass Flow Rate (kg/s)',style={'width': '200'}),
                dcc.Input(
                            id='input_1',
                            type='number',
                            value='12',
                            min='1',
                            style={'max-width': '150px'}
                        ),

    html.Label(id='pump_temp_value'),
           dcc.Slider(
                        id='slider_1',
                        min=1,
                        max=200,
                        step=1,
                        value=10
                        ),

    html.Label(id='turbine_temp_value'),
                    dcc.Slider(
                        id='slider_2',
                        min=1,
                        max=200,
                        value=60,
                    ),

                html.Label(
                        id='pump_eff_value'),
                    dcc.Slider(
                        id='slider_3',
                        min=1,
                        max=100,
                        value=60,
                    ),

                html.Label(
                        id='turbine_eff_value'),
                    dcc.Slider(
                        id='slider_4',
                        min=1,
                        max=100,
                        value=80,
                    ),

                html.Label('Select Variable Parameter:'),
	html.Div([
                dcc.Dropdown(
                    id='dropdown_4',
                    placeholder='Select Parameter',
                    options=[
                    {'label': 'Turbine Power (kW)', 'value': 'TURBINE_POWER'},
                    {'label': 'Pump Power (kW)', 'value': 'PUMP_POWER'},
                    {'label': 'Net Power (kW)', 'value': 'NET_POWER'},
                    {'label': 'Heat Input (kJ/K)', 'value': 'HEAT_INPUT'},
                    {'label': 'Thermal Efficiency (%)', 'value': 'EFFICIENCY'}
                    ],
                    value='TURBINE_POWER'
                )
                ],
                className='row'),

	html.Div([
            dcc.Graph(id='graph3', config={'displayModeBar': False}, style={'max-height': '380', 'height': '60vh'}),

        ],
            className='row',
            style={'margin-bottom': '15'}
        ),

	])

tab4_layout = html.Div([

	])





#
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


app.layout = html.Div(
    [
        html.Div([
            html.Img(
                src="http://www.qub.ac.uk/qol/qollogin-files/Queens-shield-logo-red.png",
                className='two columns',
                style={
                    'height': '60px',
                    'width': '180px',
                    'float': 'left',
                    'position': 'relative',
                },
            ),
            html.H1(
                'ORCAnalysis',
                className='seven columns',
                style={'text-align': 'center', 'font-size': '2.65em'}
            )
        ],
            className='row'
        ),
        html.Hr(style={'margin': '0', 'margin-bottom': '4'}),


        dcc.Tabs(
            tabs=[
                {'label': 'ORC Schematic', 'value': 1},
                {'label': 'System Modelling', 'value': 2},
                {'label': 'Parametric Analysis', 'value': 3},
                {'label': 'Modelling Results', 'value': 4}
              ],
            value=2,
            id='tabs',
            #vertical=vertical
        ),
        html.Div(id='tab-layout'),






    ],
    style={
        'width': '85%',
        'max-width': '1000',
        'max-height': '3500',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '10',
        'padding-bottom': '10',
    },
)



@app.callback(dash.dependencies.Output('tab-layout', 'children'),
	[dash.dependencies.Input('tabs', 'value')])

def call_tab_layout(tab_value):
	if tab_value == 1:
		return tab1_layout
	elif tab_value == 2:
		return tab2_layout
	elif tab_value == 3:
		return tab3_layout
	else:
		html.Div()


#sending data to hidden div from tab1
@app.callback(dash.dependencies.Output('graph-data-json-dump', 'children'),
              [dash.dependencies.Input('store-data-hidden-div', 'n_clicks')])

def store_data_to_hidden_div(nclick):
	if nclick >0:
		df = pd.DataFrame({'x_axis':[6,4,9],
			'y_axis':[4,2,7]})
		return df.to_json(orient = 'split')




#PUMP TEMPERATURE CALLBACK
@app.callback(Output('pump_temp_value', 'children'),
              [Input('slider_1', 'value')])

def compute_amount(slider_1):
    return u'Condenser Outlet Temperature, T1: {} (°C)'.format(slider_1)


#TURBINE TEMPERATURE CALLBACK
@app.callback(Output('turbine_temp_value', 'children'),
              [Input('slider_2', 'value')])

def compute_amount(slider_2):
    return u'Turbine Inlet Temperature, T3: {} (°C)'.format(slider_2)

#PUMP ISENTROPIC EFFICIENCY CALLBACK
@app.callback(Output('pump_eff_value', 'children'),
              [Input('slider_3', 'value')])

def compute_amount(slider_3):
    return u'Pump Isentropic Efficiency: {} (%)'.format(slider_3)

#TURBINE ISENTROPIC EFFICIENCY CALLBACK
@app.callback(Output('turbine_eff_value', 'children'),
              [Input('slider_4', 'value')])

def compute_amount(slider_4):
    return u'Turbine Isentropic Efficiency: {} (%)'.format(slider_4)

#ORC MODEL TABLE CALLBACK FUNCTION
@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [dash.dependencies.Input('slider_1', 'value'),
    dash.dependencies.Input('slider_2', 'value'),
    dash.dependencies.Input('slider_3', 'value'),
    dash.dependencies.Input('slider_4', 'value'),
    dash.dependencies.Input('dropdown_3', 'value'),
    dash.dependencies.Input('input_1', 'value'),
    #dash.dependencies.Input('table', 'selected_row_indices')

    ])

def display_table(slider_1, slider_2, slider_3, slider_4, dropdown_3, input_1):
    if dropdown_3 is None:

        return dff3.to_dict('records')

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)
    x = float(slider_1)
    y = float(slider_2)

    dff2 = dff

    dff2 = dff[dff.REFRIGERANT.str.contains('|'.join(dropdown_3))]

    dff3 = dff2
    #CALCULATES ENTHALPY AT STATE 2
    #dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) / (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    #dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - ((TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC'])))

    #TURBINE POWER CALCULATION (kW)
    dff3['TURBINE_POWER'] = MFR * (dff3['H_3'] - dff3['H_4'])

    #PUMP POWER CALCULATION (kW)
    dff3['PUMP_POWER'] = MFR * (dff3['H_2'] - dff3['H_1'])

    #NET POWER (kW)
    dff3['NET_POWER'] = dff3['TURBINE_POWER'] - dff3['PUMP_POWER']

    #SYSTEM HEAT INPUT
    dff3['HEAT_INPUT'] = MFR * (dff3['H_3'] - dff3['H_2'])

    #THERMAL EFFICIENCY
    dff3['EFFICIENCY'] = (dff3['NET_POWER'] / dff3['HEAT_INPUT']) * 100

    dff3 = dff3[dff3['EFFICIENCY'] > 0]

    dff3 = dff3[dff3['T_1'] == x]
    dff3 = dff3[dff3['T_3'] == y]

    dff3['PUMP_EFF'] = PUMP_EFF
    dff3['TURBINE_EFF'] = TURBINE_EFF
    dff3['MFR'] = MFR


    dff3 = dff3.round(2)

    #
    dff3 = dff3[['REFRIGERANT', 'MFR', 'T_1', 'T_3', 'PUMP_EFF', 'TURBINE_EFF', 'TURBINE_POWER', 'PUMP_POWER', 'NET_POWER','HEAT_INPUT', 'EFFICIENCY']]

    dff3 = dff3.round(3)

    #RETURNS CALCULATED DATA TO THE TABLEFRAME
    return dff3.to_dict('records')




@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('slider_1', 'value'),
    dash.dependencies.Input('slider_2', 'value'),
    dash.dependencies.Input('slider_3', 'value'),
    dash.dependencies.Input('slider_4', 'value'),
    dash.dependencies.Input('dropdown_3', 'value'),
    dash.dependencies.Input('input_1', 'value')
    ])

def produce_graph(slider_1, slider_2, slider_3, slider_4, dropdown_3, input_1):

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    dff2 = dff[dff['T_1'] == slider_1]
    dff3 = dff2[dff2['T_3'] == slider_2]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)

    #CALCULATES ENTHALPY AT STATE 2
    #dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) / (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    #dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - (TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC']))

    #TURBINE POWER CALCULATION (kW)
    dff3['TURBINE_POWER'] = MFR * (dff3['H_3'] - dff3['H_4'])

    #PUMP POWER CALCULATION (kW)
    dff3['PUMP_POWER'] = MFR * (dff3['H_2'] - dff3['H_1'])

    #NET POWER (kW)
    dff3['NET_POWER'] = dff3['TURBINE_POWER'] - dff3['PUMP_POWER']

    #SYSTEM HEAT INPUT
    dff3['HEAT_INPUT'] = MFR * (dff3['H_3'] - dff3['H_2'])

    #THERMAL EFFICIENCY
    dff3['EFFICIENCY'] = (dff3['NET_POWER'] / dff3['HEAT_INPUT']) * 100

    dff3 = dff3.round(2)

    dz1 = dff3[dff3['REFRIGERANT'] == 'R11']
    dz2 = dff3[dff3['REFRIGERANT'] == 'R141b']
    dz3 = dff3[dff3['REFRIGERANT'] == 'R218']
    dz4 = dff3[dff3['REFRIGERANT'] == 'R134a']
    dz5 = dff3[dff3['REFRIGERANT'] == 'R113']
    dz6 = dff3[dff3['REFRIGERANT'] == 'R410a']
    dz7 = dff3[dff3['REFRIGERANT'] == 'R236ea']
    dz8 = dff3[dff3['REFRIGERANT'] == 'R227ea']
    dz9 = dff3[dff3['REFRIGERANT'] == 'R245ca']



    return {
    'data': [
                {'x': dz1['EFFICIENCY'], 'y': dz1['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R11'},
                {'x': dz2['EFFICIENCY'], 'y': dz2['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R141b'},
                {'x': dz3['EFFICIENCY'], 'y': dz3['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R218'},
                {'x': dz4['EFFICIENCY'], 'y': dz4['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R134a'},
                {'x': dz5['EFFICIENCY'], 'y': dz5['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R113'},
                {'x': dz6['EFFICIENCY'], 'y': dz6['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R410a'},
                {'x': dz7['EFFICIENCY'], 'y': dz7['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R236ea'},
                {'x': dz8['EFFICIENCY'], 'y': dz8['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R227ea'},
                {'x': dz9['EFFICIENCY'], 'y': dz9['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R245ca'}


                ],
                'layout': {
                        'title': 'Refrigerant Thermal Efficiency Comparison',
                        "xaxis": { "title": "Thermal Efficiency (%)", "fixedrange": True, 'zeroline':True, 'showline':True},
                        "yaxis": { "title": "Refrigerant", "fixedrange": True, 'zeroline':True, 'showline':True}
                        }
}


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('slider_1', 'value'),
    dash.dependencies.Input('slider_2', 'value'),
    dash.dependencies.Input('slider_3', 'value'),
    dash.dependencies.Input('slider_4', 'value'),
    dash.dependencies.Input('dropdown_3', 'value'),
    dash.dependencies.Input('input_1', 'value')
    ])

def produce_graph(slider_1, slider_2, slider_3, slider_4, dropdown_3, input_1):

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    dff2 = dff[dff['T_1'] == slider_1]
    dff3 = dff2[dff2['T_3'] == slider_2]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)

    #CALCULATES ENTHALPY AT STATE 2
    #dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) / (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    #dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - (TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC']))

    #TURBINE POWER CALCULATION (kW)
    dff3['TURBINE_POWER'] = MFR * (dff3['H_3'] - dff3['H_4'])

    #PUMP POWER CALCULATION (kW)
    dff3['PUMP_POWER'] = MFR * (dff3['H_2'] - dff3['H_1'])

    #NET POWER (kW)
    dff3['NET_POWER'] = dff3['TURBINE_POWER'] - dff3['PUMP_POWER']

    #SYSTEM HEAT INPUT
    dff3['HEAT_INPUT'] = MFR * (dff3['H_3'] - dff3['H_2'])

    #THERMAL EFFICIENCY
    dff3['EFFICIENCY'] = (dff3['NET_POWER'] / dff3['HEAT_INPUT']) * 100


    dff3 = dff3.round(2)


    return {
    'data': [
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_1'], 'type': 'bar', 'name': 'State 1'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_2'], 'type': 'bar', 'name': 'State 2'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_3'], 'type': 'bar', 'name': 'State 3'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_4'], 'type': 'bar', 'name': 'State 4'}

                ],
                'layout': {
                        'title': 'Refrigerant State Enthalpy Comparison',
                        "xaxis": { "title": "Refrigerant", "fixedrange": True, 'zeroline':True, 'showline':True},
                        "yaxis": { "title": "Enthalpy (kJ/kg)", "fixedrange": True, 'zeroline':True, 'showline':True}
    }
    }


@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('slider_1', 'value'),
    dash.dependencies.Input('slider_2', 'value'),
    dash.dependencies.Input('slider_3', 'value'),
    dash.dependencies.Input('slider_4', 'value'),
    dash.dependencies.Input('dropdown_3', 'value'),
    dash.dependencies.Input('dropdown_4', 'value'),
    dash.dependencies.Input('input_1', 'value')
    ])

def produce_graph(slider_1, slider_2, slider_3, slider_4, dropdown_3, dropdown_4, input_1):

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)
    x = float(slider_1)
    y = dropdown_4

    dff2 = dff

    dff2 = dff[dff.REFRIGERANT.str.contains('|'.join(dropdown_3))]

    dff3 = dff2
    #CALCULATES ENTHALPY AT STATE 2
    #dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) / (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    #dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - ((TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC'])))

    #TURBINE POWER CALCULATION (kW)
    dff3['TURBINE_POWER'] = MFR * (dff3['H_3'] - dff3['H_4'])

    #PUMP POWER CALCULATION (kW)
    dff3['PUMP_POWER'] = MFR * (dff3['H_2'] - dff3['H_1'])

    #NET POWER (kW)
    dff3['NET_POWER'] = dff3['TURBINE_POWER'] - dff3['PUMP_POWER']

    #SYSTEM HEAT INPUT
    dff3['HEAT_INPUT'] = MFR * (dff3['H_3'] - dff3['H_2'])

    #THERMAL EFFICIENCY
    dff3['EFFICIENCY'] = (dff3['NET_POWER'] / dff3['HEAT_INPUT']) * 100

    dff3 = dff3[dff3['EFFICIENCY'] > 0]

    dff3 = dff3[dff3['T_1'] == x]


    dff3 = dff3.round(2)

    dz1 = dff3[dff3['REFRIGERANT'] == 'R11']
    dz2 = dff3[dff3['REFRIGERANT'] == 'R141b']
    dz3 = dff3[dff3['REFRIGERANT'] == 'R218']
    dz4 = dff3[dff3['REFRIGERANT'] == 'R134a']
    dz5 = dff3[dff3['REFRIGERANT'] == 'R113']
    dz6 = dff3[dff3['REFRIGERANT'] == 'R410a']
    dz7 = dff3[dff3['REFRIGERANT'] == 'R236ea']
    dz8 = dff3[dff3['REFRIGERANT'] == 'R227ea']
    dz9 = dff3[dff3['REFRIGERANT'] == 'R245ca']

    return {
        'data': [
            {'x': dz1['T_3'], 'y': dz1[y], 'type': 'line', 'name': 'R11'},
            {'x': dz2['T_3'], 'y': dz2[y], 'type': 'line', 'name': 'R141b'},
            {'x': dz3['T_3'], 'y': dz3[y], 'type': 'line', 'name': 'R218'},
            {'x': dz4['T_3'], 'y': dz4[y], 'type': 'line', 'name': 'R134a'},
            {'x': dz5['T_3'], 'y': dz5[y], 'type': 'line', 'name': 'R113'},
            {'x': dz6['T_3'], 'y': dz6[y], 'type': 'line', 'name': 'R410a'},
            {'x': dz7['T_3'], 'y': dz7[y], 'type': 'line', 'name': 'R236ea'},
            {'x': dz8['T_3'], 'y': dz8[y], 'type': 'line', 'name': 'R227ea'},
            {'x': dz9['T_3'], 'y': dz9[y], 'type': 'line', 'name': 'R245ca'}

            ],
        'layout':
        {
        'title': 'Refrigerant Performance Comparison',
        "xaxis": { "title": "Turbine Inlet Temperature, T3 (°C)", "fixedrange": True, 'showline':False, 'zeroline':True},
        "yaxis": { "title": dropdown_4, "fixedrange": True, 'zeroline':True, 'showline':True}
        }
}








if __name__ == '__main__':
    app.run_server(debug=True)
