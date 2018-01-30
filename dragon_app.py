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
                className='eight columns',
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
                    id='dropdown_3',
                    options=[{'label': i, 'value': i} for i in df.Date.unique()],
                    placeholder='Select Date',
                    multi=True,
                ),

            html.Label('Select Athlete:'),
                dcc.Dropdown(
                    id='dropdown_1',
                    options=[{'label': i, 'value': i} for i in df.Athlete.unique()],
                    placeholder='Select Athlete',
                    multi=True,
                ),

            html.Label('Select Movement:'),
                dcc.Dropdown(
                    id='dropdown_2',
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
        id='table'
    ),
            ],
                className='six columns',
            ),
            html.Div([
            ],
                className='five columns'
            ),
        ],
            className='row',
            style={'margin-bottom': '10'}
        ),
        html.Div([
            html.Div([
                html.Label('Implied volatility settings:'),
                html.Div([
                    dcc.RadioItems(
                        id='iv_selector',
                        options=[
                            {'label': 'Calculate IV ', 'value': True},
                            {'label': 'Use given IV ', 'value': False},
                        ],
                        value=True,
                        labelStyle={'display': 'inline-block'},
                    ),
                    dcc.RadioItems(
                        id='calendar_selector',
                        options=[
                            {'label': 'Trading calendar ', 'value': True},
                            {'label': 'Annual calendar ', 'value': False},
                        ],
                        value=True,
                        labelStyle={'display': 'inline-block'},
                    )
                ],
                    style={'display': 'inline-block', 'margin-right': '10', 'margin-bottom': '10'}
                ),
                html.Div([
                    html.Div([
                        html.Label('Risk-free rate (%)'),
                        dcc.Input(
                            id='rf_input',
                            placeholder='Risk-free rate',
                            type='number',
                            value='0.0',
                            style={'width': '125'}
                        )
                    ],
                        style={'display': 'inline-block'}
                    ),
                    html.Div([
                        html.Label('Dividend rate (%)'),
                        dcc.Input(
                            id='div_input',
                            placeholder='Dividend interest rate',
                            type='number',
                            value='0.0',
                            style={'width': '125'}
                        )
                    ],
                        style={'display': 'inline-block'}
                    ),
                ],
                    style={'display': 'inline-block', 'position': 'relative', 'bottom': '10'}
                )
            ],
                className='six columns',
                style={'display': 'inline-block'}
            ),
            html.Div([
                html.Label('Chart settings:'),
                dcc.RadioItems(
                    id='log_selector',
                    options=[
                        {'label': 'Log surface', 'value': 'log'},
                        {'label': 'Linear surface', 'value': 'linear'},
                    ],
                    value='log',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Checklist(
                    id='graph_toggles',
                    options=[
                        {'label': 'Flat shading', 'value': 'flat'},
                        {'label': 'Discrete contour', 'value': 'discrete'},
                        {'label': 'Error bars', 'value': 'box'},
                        {'label': 'Lock camera', 'value': 'lock'}
                    ],
                    values=['flat', 'box', 'lock'],
                    labelStyle={'display': 'inline-block'}
                )
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            dcc.Graph(id='iv_surface', style={'max-height': '600', 'height': '60vh'}),
        ],
            className='row',
            style={'margin-bottom': '20'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='iv_heatmap', style={'max-height': '350', 'height': '35vh'}),
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
    style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)


# Cache raw data
@app.callback(Output('raw_container', 'hidden'),
              [Input('ticker_dropdown', 'value')])
def cache_raw_data(ticker):

    global raw_data
    raw_data = get_raw_data(ticker)
    print('Loaded raw data')

    return 'loaded'





@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [dash.dependencies.Input('dropdown_1', 'value'),
    #dash.dependencies.Input('table', 'selected_row_indices')

    ])

def display_table(dropdown_1):
    if dropdown_1 is None:

        return dff3.to_dict('records')

    dff = df[df.Athlete.str.contains('|'.join(dropdown_1))]

    dff2 = dff

    dff3 = dff2

    dff3 = dff3.drop('Date', axis=1)

    dff3 = dff3.drop_duplicates()
    #

    return dff3.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
