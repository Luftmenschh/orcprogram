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



app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True

#image_filename = src='https://github.com/ndaly06/orcprogram/blob/master/orcschematic2.png?raw=true'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

df = pd.read_csv('https://github.com/ndaly06/orcprogram/blob/master/refrig_data_3.csv?raw=true')
df2 = df[['REFRIGERANT', 'T_1_K', 'T_3_K', 'H_1', 'H_2_ISENTROPIC', 'H_3', 'H_4_ISENTROPIC']]
df2 = df2.round(2)


#GENERATES TABLE
def generate_table(dataframe, max_rows=9):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        )

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
                    'height': '70px',
                    'width': '180px',
                    'float': 'left',
                    'position': 'relative',
                },
            ),
            html.H1(
                'ORCa System Analysis',
                className='eight columns',
                style={'text-align': 'center'}
            )
        ],
            className='row'
        ),
        html.Hr(style={'margin': '0', 'margin-bottom': '5'}),
        html.Div([
            html.Div([

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
                    value=['R134a', 'R141b', 'R123'],
                ),
            ],
                className='six columns',
            ),
            html.Div([
                html.Label('Mass Flow Rate (kg/s)',style={'width': '200'}),
                        dcc.Input(
                            id='input_1',
                            type='number',
                            value='12',
                            min='1',
                            style={'max-width': '150px'}
                        )
            ],
                className='two columns',
            ),
            html.Div([
                html.Div([
                    html.Label(
                        id='pump_temp_value'),
                    dcc.Slider(
                        id='slider_1',
                        min=1,
                        max=70,
                        step=1,
                        value=10
                        )
                ]),
                html.Div([
                    html.Label(
                        id='turbine_temp_value'),
                    dcc.Slider(
                        id='slider_2',
                        min=1,
                        max=70,
                        value=60,
                    )
                ]),
                html.Div([
                    html.Label(
                        id='pump_eff_value'),
                    dcc.Slider(
                        id='slider_3',
                        min=1,
                        max=100,
                        value=60,
                    )
                ]),

                html.Div([
                    html.Label(
                        id='turbine_eff_value'),
                    dcc.Slider(
                        id='slider_4',
                        min=1,
                        max=100,
                        value=80,
                    )
                ]),

            ],
                className='four columns'
            ),
        ],
            className='row',
            style={'margin-bottom': '10'}
        ),
        html.Div([
            html.Div([
                html.Label('Model Results'),
                html.Div(id='table-container',
                    style={
                    'max-height': '250',
                    'max-width': '450',
                    'float': 'left',
                    'position': 'left',
                    'display' : 'left'}
                    ),
                #html.Label('Parametric Analysis'),
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
                    value='NET_POWER'
                ),






            ],
                className='six columns',
                style={'display': 'inline-block'}
            ),
            html.Div([
                html.Img(src='https://github.com/ndaly06/orcprogram/blob/master/orcschematic2.png?raw=true',
                #html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                    style={
                    'max-height': '250',
                    'max-width': '500',
                    'float': 'right',
                    'position': 'right',
                    'display' : 'right'}
                    )

            ],
                className='six columns'

            ),
        ],
            className='row'
        ),

        html.Hr(style={'margin': '5', 'margin-bottom': '5'}),

        html.Div([
            dcc.Graph(id='graph3', config={'displayModeBar': False}, style={'max-height': '400', 'height': '60vh'}),

        ],
            className='row',
            style={'margin-bottom': '30'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='graph2', config={'displayModeBar': False}, style={'max-height': '450', 'height': '50vh'}),
            ],
                className='five columns'
            ),
            html.Div([
                dcc.Graph(id='graph1', config={'displayModeBar': False}, style={'max-height': '450', 'height': '50vh'}),
            ],
                className='seven columns'
            )
        ],
            className='row'
        ),

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
        'max-width': '1400',
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


@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('slider_1', 'value'),
    dash.dependencies.Input('slider_2', 'value'),
    dash.dependencies.Input('slider_3', 'value'),
    dash.dependencies.Input('slider_4', 'value'),
    dash.dependencies.Input('dropdown_3', 'value'),
    dash.dependencies.Input('input_1', 'value')
    ])

def display_table(slider_1, slider_2, slider_3, slider_4, dropdown_3, input_1):
    if dropdown_3 is None:
        return generate_table(dff3)

    dff = df[df.REFRIGERANT.str.contains('|'.join(dropdown_3))]
    dff2 = dff[dff['T_1'] == slider_1]
    dff3 = dff2[dff2['T_3'] == slider_2]
    MFR = float(input_1)
    PUMP_EFF = float(slider_3)
    TURBINE_EFF = float(slider_4)


    #CALCULATES ENTHALPY AT STATE 2
    dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

    #CALCULATES ENTHALPY AT STATE 4
    dff3['H_4'] = (dff3['H_3'] - (TURBINE_EFF / 100) * (dff3['H_3'] - dff3['H_4_ISENTROPIC']))

    dff3 = dff3.round(2)

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
    dff3 = dff3[['REFRIGERANT', 'PUMP_POWER', 'TURBINE_POWER', 'HEAT_INPUT']]

    dff3 = dff3.round(3)

    #DATASET
    return generate_table(dff3)




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
    dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

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
    dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

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
    dz3 = dff3[dff3['REFRIGERANT'] == 'R123']
    dz4 = dff3[dff3['REFRIGERANT'] == 'R134a']



    return {
    'data': [
                {'x': dz1['EFFICIENCY'], 'y': dz1['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R11'},
                {'x': dz2['EFFICIENCY'], 'y': dz2['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R141b'},
                {'x': dz3['EFFICIENCY'], 'y': dz3['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R123'},
                {'x': dz4['EFFICIENCY'], 'y': dz4['REFRIGERANT'], 'type': 'bar', 'orientation': 'h', 'width': '0.5', 'name': 'R134a'}

                ],
                'layout': {
                        'title': 'Refrigerant Thermal Efficiency Comparison',
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
    dff3['H_2'] = dff3['H_1'] + (PUMP_EFF / 100) * (dff3['H_2_ISENTROPIC'] - dff3['H_1'])

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
    dz3 = dff3[dff3['REFRIGERANT'] == 'R123']
    dz4 = dff3[dff3['REFRIGERANT'] == 'R134a']

    return {
        'data': [
            #x=dff4['T_3'],
            {'x': dz1['T_3'], 'y': dz1[y], 'type': 'line', 'name': 'R11'},
            {'x': dz2['T_3'], 'y': dz2[y], 'type': 'line', 'name': 'R141b'},
            {'x': dz3['T_3'], 'y': dz3[y], 'type': 'line', 'name': 'R123'},
            {'x': dz4['T_3'], 'y': dz4[y], 'type': 'line', 'name': 'R134a'}
            ],
        'layout':
        {
        'title': 'Refrigerant Performance Comparison',
        "xaxis": { "title": "Turbine Inlet Temperature, T1 (°C)", "fixedrange": True, 'showline':False, 'zeroline':True},
        "yaxis": { "title": dropdown_4, "fixedrange": True, 'zeroline':True, 'showline':True},
        #"height": '450'
        }
}


if __name__ == '__main__':
    app.run_server(debug=True)
