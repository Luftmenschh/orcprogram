# -*- coding: utf-8 -*-
#ENABLES CORRECT DIVISION IN PYTHON
from __future__ import division

#IMPORTS THE MODULES/PACKAGES USED BY THE COMPUTER PROGRAM
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

#INITIATES THE PROGRAM
app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True

#READS THE ORC REFRIGERANT DATASET FROM GITHUB(ONLINE LOACTION WHERE THE DATASET IS HOSTED)
df = pd.read_csv('https://github.com/ndaly06/orcprogram/blob/master/refrigerant_data.csv?raw=true')
df2 = df[['REFRIGERANT', 'T_1_K', 'T_3_K', 'H_1', 'H_2_ISENTROPIC', 'H_3', 'H_4_ISENTROPIC']]
df2 = df2.round(2)

#EXTERNAL CSS FOR STYLING THE PROGRAM'S GUI
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

#
app.layout = html.Div(
    [
    html.Div([
        #ADDS THE QUB LOGO TO THE PROGRAM
        html.Img(
            src="http://www.qub.ac.uk/qol/qollogin-files/Queens-shield-logo-red.png",
            className='two columns',
            style={
            'height': '60px',
            'width': '170px',
            'float': 'left',
            'position': 'relative',
            }
            ),
        #SETS PROGRAM TITLE
        html.H1(
            'ORCAnalysis',
            className='seven columns',
            style={'text-align': 'center', 'font-size': '2.65em'}
            )
        ],
        className='row'
    ),
    #ADDS HORIZONTAL (SEPARATES HEADER FROM THE DATA INPUT SECTION)
    html.Hr(style={'margin': '0', 'margin-bottom': '4'}),

    html.Div([
        html.Div([
            #ADDS THE LABEL FOR DROPDOWN 1 (ORC CONFIGURATION SELECTION)
            html.Label('Organic Rankine Cycle Configuration:'),
            #ADDS DROPDOWN 1
            dcc.Dropdown(
                id='dropdown_1',
                #SETS THE PLACEHOLDER (FIXED NAME)
                placeholder='Subcritical',
                #SETS THE DROPDOWN AS UNACTIONABLE
                disabled=True,
                ),
            #ADDS THE LABEL FOR DROPDOWN 2 (HEAT SOURCE SELECTION)
            html.Label('Heat Source:'),
            #ADDS DROPDOWN 2
            dcc.Dropdown(
                id='dropdown_2',
                #SETS THE PLACEHOLDER (FIXED NAME)
                placeholder='Geothermal Water',
                #SETS THE DROPDOWN AS UNACTIONABLE
                disabled=True
                ),
            html.Div([
                #ADDS THE LABEL FOR DROPDOWN 3 (REFRIGERANT SELECTION)
                html.Label('Select Refrigerant:'),
                #ADDS DROPDOWN 3
                dcc.Dropdown(
                    id='dropdown_3',
                    #SEARCHES THE ORC REFRIGERANT DATASET AND ADDS EACH UNIQUE REFRIGERANT NAME TO THE DROPDOWN SELECTION
                    options=[{'label': i, 'value': i} for i in df.REFRIGERANT.unique()],
                    #SETS THE PLACEHOLDER (FIXED NAME)
                    placeholder='Select Refrigerant',
                    #ALLOWS MULTIPLE FLUIDS TO BE SELECTED
                    multi=True,
                    #SETS THE INITIAL FLUID SELECTION TO BE SET
                    value=['R134a', 'R141b', 'R410a', 'R113']
                    ),
                #ADDS THE LABEL FOR INPUT BOX 1 (MASS FLOW RATE)
                html.Label('Mass Flow Rate (kg/s)',
                    #SETS THE INPUT BOX WIDTH
                    style={'width': '200'}
                    ),
                #ADDS INPUT BOX 1
                dcc.Input(id='input_1',
                    type='number',
                    #SETS THE INITIAL VALUE AT 12
                    value='12',
                    #SETS A MINIMUM VALUE AT 1
                    min='1',
                    #SETS THE MAX-WIDTH OF THE INPUT BOX AS 150px
                    style={'max-width': '150px'}
                    )
                ]
                ),
            #ADDS THE LABEL FOR SLIDER 1 (REFRIGERANT TEMPERATURE VALUE)
            html.Label(id='pump_temp_value'),
            #ADDS SLIDER 1
            dcc.Slider(id='slider_1',
                #SETS THE MINIMUM SLIDER VALUE AT 1
                min=1,
                #SETS THE MAXIMUM SLIDER VALUE AT 200
                max=200,
                #SETS THE STEP VALUE AT 1
                step=1,
                #SETS THE INITIAL VALUE AT 10
                value=10
                ),
            #ADDS THE LABEL FOR SLIDER 2 (TURBINE TEMPERATURE VALUE)
            html.Label(id='turbine_temp_value'),
            #ADDS SLIDER 2
            dcc.Slider(id='slider_2',
                #SETS TNE MINIMUM SLIDER VALUE AT 1
                min=1,
                #SETS THE MAXIMUM SLDER VALUE AT 200
                max=200,
                #SETS THE INITIAL VALUE AT 60
                value=60
                ),
            #ADDS THE LABEL FOR SLIDER 3 (REFRIGERANT PUMP EFFICIENCY VALUE)
            html.Label(id='pump_eff_value'),
            #ADDS SLIDER 3
            dcc.Slider(id='slider_3',
                #SETS THE MINIMUM SLIDER VALUE AT 1
                min=1,
                #SETS THE MAXIMUM SLIDER VALUE AT 100
                max=100,
                #SETS THE INITIAL SLIDER VALUE AT 60
                value=60
                ),
            #ADDS THE LABEL FOR SLIDER 4 (TURBINE EFFICIENCY VALUE)
            html.Label(id='turbine_eff_value'),
            #ADDS SLIDER 4
            dcc.Slider(id='slider_4',
                #SETS THE MINIMUM SLIDER VALUE AT 1
                min=1,
                #SETS THE MAXIMUM SLIDER VALUE AT 100
                max=100,
                #SETS THE INITIAL SLIDER VALUE AT 80
                value=80
                )
            ],
            className='six columns'
            ),

html.Div([
    #ADDS THE ORC SYSTEM SCHEMATIC LABEL
    html.Label('ORC System Schematic'),
    #ADDS THE ORC SCHEMATIC TO THE PROGRAM
    html.Img(src='https://github.com/ndaly06/orcprogram/blob/master/orcschematic3.png?raw=true',
        #SETS THE IMAGE STYLING
        style={
        'max-height': '250px',
        'max-width': '80%',
        'position':'relative'}
        ),

            ],
                className='five columns',
                style={'display': 'inline-block', 'position': 'absolute'}
            ),
        ],
            className='row',
            style={'margin-bottom': '10'}
        ),


        html.Div([
            html.Div([
                dcc.Graph(id='graph2', config={'displayModeBar': False}, style={'max-height': '350', 'height': '50vh'}),
            ],
                className='five columns'
            ),
            html.Div([
                dcc.Graph(id='graph1', config={'displayModeBar': False}, style={'max-height': '350', 'height': '50vh'}),
            ],
                className='seven columns'
            ),

            html.Div([
            html.H6('Parameteric Analysis'),
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

        ],
            className='row',
            style={'margin-bottom': '30'}
        ),


        html.Div([
            dcc.Graph(id='graph3', config={'displayModeBar': False}, style={'max-height': '380', 'height': '60vh'}),

        ],
            className='row',
            style={'margin-bottom': '15'}
        ),

        html.Div([
    html.H6('ORC Model Results'),
    dt.DataTable(

        rows=[{}],
        row_selectable=False,
        filterable=False,
        sortable=False,
        selected_row_indices=[],
        id='table'
    ),

    #html.Div([
    #html.A('EXPORT CSV',
        #id='download_button',

        #download="orc_model_data.csv",
        #href="",
        #download="123.csv",
        #download="https://github.com/ndaly06/orcprogram/blob/master/orc_model_data.csv?raw=true",
        #href="https://github.com/ndaly06/orcprogram/blob/master/orc_model_data.csv?raw=true",
        #target="_blank"
        #)
    #],
    #style={'display': 'inline-block', 'float':'right', 'padding-top': '5'}
    #)
]),



        html.P(
            hidden='',
            id='raw_container',
            style={'display': 'none'}
        ),
        html.P(
            hidden='',
            id='filtered_container',
            style={'display': 'none'}
        )
    ],
    style={
        'width': '85%',
        'max-width': '970',
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





#ENTHALPY COMPARISON GRAPH CALLBACK FUNCTION
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


    return {
    'data': [
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_1'], 'type': 'bar', 'name': 'State 1'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_2'], 'type': 'bar', 'name': 'State 2'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_3'], 'type': 'bar', 'name': 'State 3'},
                {'x': dff3['REFRIGERANT'], 'y': dff3['H_4'], 'type': 'bar', 'name': 'State 4'}

                ],
                'layout': {
                        'title': 'Refrigerant State Enthalpy Analysis',
                        "xaxis": { "title": "Refrigerant", "fixedrange": True, 'zeroline':True, 'showline':True},
                        "yaxis": { "title": "Enthalpy (kJ/kg)", "fixedrange": True, 'zeroline':True, 'showline':True}
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

    dz1 = dff3[dff3['REFRIGERANT'] == 'R11']
    dz2 = dff3[dff3['REFRIGERANT'] == 'R141b']
    dz3 = dff3[dff3['REFRIGERANT'] == 'R218']
    dz4 = dff3[dff3['REFRIGERANT'] == 'R134a']
    dz5 = dff3[dff3['REFRIGERANT'] == 'R113']
    dz6 = dff3[dff3['REFRIGERANT'] == 'R410a']
    dz7 = dff3[dff3['REFRIGERANT'] == 'R236ea']
    dz8 = dff3[dff3['REFRIGERANT'] == 'R227ea']
    dz9 = dff3[dff3['REFRIGERANT'] == 'R245ca']
    dz10 = dff3[dff3['REFRIGERANT'] == 'R600a']



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
                {'x': dz9['EFFICIENCY'], 'y': dz9['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R245ca'},
                {'x': dz10['EFFICIENCY'], 'y': dz10['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R600a'}


                ],
                'layout': {
                        'title': 'Refrigerant Thermal Efficiency Analysis',
                        "xaxis": { "title": "Thermal Efficiency (%)", "fixedrange": True, 'zeroline':True, 'showline':True},
                        "yaxis": { "title": "Refrigerant", "fixedrange": True, 'zeroline':True, 'showline':True}
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
    dz10 = dff3[dff3['REFRIGERANT'] == 'R600a']

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
            {'x': dz9['T_3'], 'y': dz9[y], 'type': 'line', 'name': 'R245ca'},
            {'x': dz10['T_3'], 'y': dz10[y], 'type': 'line', 'name': 'R600a'}


            ],
        'layout':
        {
        'title': 'Refrigerant Performance Analysis',
        "xaxis": { "title": "Turbine Inlet Temperature, T3 (°C)", "fixedrange": True, 'showline':False, 'zeroline':True},
        "yaxis": { "title": dropdown_4, "fixedrange": True, 'zeroline':True, 'showline':True}
        }
}


@app.callback(
    dash.dependencies.Output('download_button', 'href'),
    [dash.dependencies.Input('slider_1', 'value'),
        dash.dependencies.Input('slider_2', 'value'),
        dash.dependencies.Input('slider_3', 'value'),
        dash.dependencies.Input('slider_4', 'value'),
        dash.dependencies.Input('dropdown_3', 'value'),
        dash.dependencies.Input('dropdown_4', 'value'),
        dash.dependencies.Input('input_1', 'value')
        ])

def update_download_button(slider_1, slider_2, slider_3, slider_4, dropdown_3, dropdown_4, input_1):

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    dff2 = dff[dff['T_1'] == slider_1]
    dff3 = dff2[dff2['T_3'] == slider_2]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)

    dff3['PUMP_EFF'] = float(slider_3)
    dff3['TURBINE_EFF'] = float(slider_4)


    #CALCULATES ENTHALPY AT STATE 2
    #dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) / (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    dff3['H_2'] = dff3['H_2_ISENTROPIC'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])
    #dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - (TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC']))

    #dff3 = dff3.round(2)

    #CALCULATES ENTHALPY AT STATE 2
    dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - (TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC']))

    #TURBINE POWER CALCULATION (kW)
    dff3['TURBINE_POWER'] = MFR * (dff3['H_3'] - dff3['H_4'])

    #PUMP POWER CALCULATION (kW)
    dff3['PUMP_POWER'] = MFR * (dff3['H_2'] - dff3['H_1'])

    #NET POWER (kW)
    dff3['NET_POWER'] = dff3['TURBINE_POWER'] - dff3['PUMP_POWER']

    #SYSTEM HEAT INPUT CALCULATION
    dff3['HEAT_INPUT'] = MFR * (dff3['H_3'] - dff3['H_2'])

    #THERMAL EFFICIENCY (%) CALCULATION
    dff3['EFFICIENCY'] = (dff3['NET_POWER'] / dff3['HEAT_INPUT']) * 100

    #
    dff3 = dff3[['REFRIGERANT', 'T_1', 'T_3', 'PUMP_EFF', 'TURBINE_EFF', 'TURBINE_POWER', 'PUMP_POWER', 'NET_POWER','HEAT_INPUT', 'EFFICIENCY']]

    dff3 = dff3.round(3)





if __name__ == '__main__':
    app.run_server(debug=True)
