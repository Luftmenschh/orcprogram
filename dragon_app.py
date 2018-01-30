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


df = pd.read_csv('https://github.com/ndaly06/orcprogram/blob/master/athlete_data.csv?raw=true')


app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True

external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
              "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]



for css in external_css:
    app.css.append_css({"external_url": css})






# Make app layout
app.layout = html.Div(
    [
        html.Div([
            html.Img(
                src="https://github.com/ndaly06/orcprogram/blob/master/analyifit_logo.png?raw=true",
                className='four columns',
                style={
                    'height': '60',
                    'width': '240',
                    'float': 'left',
                    'position': 'relative',
                    'top': '0px',
                    'left': '0px'

                },

            ),

        ],
            className='row'
        ),
        html.Hr(style={'margin': '0', 'margin-bottom': '1'}),
        html.Div([
            html.Div([
                html.Label('Select Date:'),
                dcc.Dropdown(
                    id='dropdown_1',
                    options=[{'label': i, 'value': i} for i in df.Date.unique()],
                    placeholder='Select Date',
                    multi=True,
                ),

            html.Label('Select Athlete:'),
                dcc.Dropdown(
                    id='dropdown_2',
                    options=[{'label': i, 'value': i} for i in df.Athlete.unique()],
                    placeholder='Select Athlete',
                    multi=True,
                    value=['Cathal', 'Nial', 'Eoin']
                ),

            html.Label('Select Movement:'),
                dcc.Dropdown(
                    id='dropdown_3',
                    options=[{'label': i, 'value': i} for i in df.Athlete.unique()],
                    placeholder='Select Movement',
                    multi=True,
                ),
            ],
                className='six columns',
            ),
            html.Div([
                html.Label('Athlete Data'),

                dt.DataTable(
                    rows=[{}],
        row_selectable=False,
        filterable=False,
        sortable=False,
        selected_row_indices=[],
        id='table',

    ),
            ],
                className='six columns',
                style={'max-height': '250', 'height': '30vh'}
            ),
        ],
            className='row',
            style={'margin-bottom': '10'}
        ),
        html.Div([
            html.Div([
                html.Label('Implied volatility settings:'),


            ],
                className='six columns',
                style={'display': 'inline-block'}
            ),
        ],
            className='row'
        ),
        html.Div([
            dcc.Graph(id='graph2', style={'max-height': '600', 'height': '60vh'}),
        ],
            className='row',
            style={'margin-bottom': '20'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='graph3', style={'max-height': '350', 'height': '50vh'}),
            ],
                className='five columns'
            ),
            html.Div([
                dcc.Graph(id='iv_scatter', style={'max-height': '350', 'height': '35vh'}),
            ],
                className='seven columns'
            )
        ],
            className='row'
        ),
        # Temporary hack for live dataframe caching
        # 'hidden' set to 'loaded' triggers next callback
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

    style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "1100px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})








@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [dash.dependencies.Input('dropdown_2', 'value'),
    ])

def display_table(dropdown_2):
    if dropdown_2 is None:

        return dff3.to_dict('records')

    dff = df[df.Athlete.str.contains('|'.join(dropdown_2))]

    dff2 = dff

    dff3 = dff2

    dff3 = dff3.drop('Date', axis=1)

    dff3 = dff3.drop_duplicates()
    #

    return dff3.to_dict('records')


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [
    dash.dependencies.Input('dropdown_2', 'value'),
    ])

def produce_graph(dropdown_2):

    df = pd.read_csv('https://github.com/ndaly06/orcprogram/blob/master/athlete_strength_data.csv?raw=true')

    dff = df[df.Athlete.str.contains('|'.join(dropdown_2))]



    return {
    'data': [
                {'x': dff['Athlete'], 'y': dff['Deadlift'], 'type': 'bar', 'name': 'Deadlift 1RM (kg)'},
                {'x': dff['Athlete'], 'y': dff['Clean'], 'type': 'bar', 'name': 'S. Clean 1RM (kg)'},
                {'x': dff['Athlete'], 'y': dff['Back Squat'], 'type': 'bar', 'name': 'B. Squat 1RM (kg)'},
                {'x': dff['Athlete'], 'y': dff['Front Squat'], 'type': 'bar', 'name': 'F. Squat 1RM (kg)'},

                {'x': dff['Athlete'], 'y': dff['Front Squat'], 'type': 'bar', 'name': 'F. Squat 1RM (kg)'},



                ],
                'layout': {
                        'title': 'Athlete Strength Analysis',
                        "xaxis": { "title": "Athlete", "fixedrange": True, 'zeroline':True, 'showline':True},
                        "yaxis": { "title": "Weight (kg)", "fixedrange": True, 'zeroline':True, 'showline':True}
    }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
