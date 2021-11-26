from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_daq as daq
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import pathlib
from dash.exceptions import PreventUpdate
from datetime import date
import time

from apps.equipments.StationMeteo.Api import api_station_meteo_db as api_meteo_helper

from app import app

DB_FILENAME = "../datasets/weewx.db"
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME).resolve()
conn_db = sqlite3.connect(DB_FILE, check_same_thread=False)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

card_gauge = dbc.Card([
    html.Div([
            dbc.Container(
                [
                    dbc.Col([
                            html.Div([
                                dbc.Row(daq.Gauge(id="daq_temp", size=100, min=0, max=110, label="Température"),className='ml-5 p-3 pb-2'),
                                dbc.Row(daq.LEDDisplay(id='temp_led',label="",value=0,color=theme['secondary'],className='dark-theme-control ml-5 pb-5')),
                            ],className="row justify-content-center",),
                    ]),
                    dbc.Col([
                        html.Div([
                            dbc.Row(daq.Gauge(id="daq_pression", size=100, min=0, max=10, value=6, label="Pression"),className='ml-5 p-3 pb-2'),
                            dbc.Row(daq.LEDDisplay(id='pression_led',label="",value=0,color=theme['secondary'],className='dark-theme-control ml-5 pb-5')),
                        ], className="row justify-content-center", ),
                    ]),
                    dbc.Col([
                        html.Div([
                            dbc.Row(daq.Gauge(id="daq_humi", size=100, min=0, max=10, value=6, label="Humidité"),className='ml-5 p-3 pb-2'),
                            dbc.Row(daq.LEDDisplay(id='humi_led', label="", value=0, color=theme['secondary'],className='dark-theme-control ml-5 pb-5')),
                        ], className="row justify-content-center", ),
                    ]),
                    dbc.Col([
                        html.Div([
                            dbc.Row(daq.Gauge(id="daq_vent", size=100, min=0, max=10, value=6, label="Vent (km/h)"),className='ml-5 p-3 pb-2'),
                            dbc.Row(daq.LEDDisplay(id='vent_led', label="", value=0, color=theme['secondary'],className='dark-theme-control ml-5 pb-5')),
                        ], className="row justify-content-center", ),
                    ]),
                    dbc.Col([
                        html.Div([
                            dbc.Row(daq.Gauge(id="daq_vent2", size=100, min=0, max=10, value=6, label="Vent (km/h)"),className='ml-5 p-3 pb-2 h-100'),
                            dbc.Row(daq.LEDDisplay(id='vent2_led', label="", value=0, color=theme['secondary'],className='dark-theme-control ml-5 pb-5 h-100')),
                        ], className="row justify-content-center", ),
                    ]),
                    dcc.Interval(id="data_update_temp", disabled=False, interval=3000, n_intervals=0),
                    dcc.Interval(id="data_update_pression", disabled=False, interval=1800000, n_intervals=0),
                    dcc.Interval(id="data_update_humi", disabled=False, interval=1800000, n_intervals=0),
                    dcc.Interval(id="data_update_vent", disabled=False, interval=1800000, n_intervals=0),
                ],
                fluid=True,
                className="row justify-content-center  h-100 pt-5 pb-5 mt-5 ml-2 border border-2 rounded rounded-3 border-dark",
            ),
        ]
    ),

card_export_meteo_layout = dbc.Card([
            dbc.Container(
                [
                    html.Div(
                        [
                            html.H4(
                                    children='SELECT DATA AND EXPORT:',
                                    className="display-5 text-center",
                            ),
                            dcc.Checklist(
                                id='check_list_data',
                                options=[
                                    {'label': 'Température', 'value': 'outTemp'},
                                    {'label': 'Pression', 'value': 'pressure'},
                                    {'label': 'Humidité', 'value': 'outHumidity'},
                                    {'label': 'Vent (km/h)', 'value': 'windSpeed'},
                                    {'label': 'Vent (km/h)', 'value': 'windSpeed'}
                                ],
                                value=[],
                                labelStyle={'display': 'inline-block',
                                            'background':'#2b95ff',   # style of the <label> that wraps the checkbox input and the option's label
                                            'padding':'0.5rem 0.5rem',
                                            'border-radius':'0.5rem',
                                            'marginLeft':'5rem',
                                            'marginRight':'5rem',
                                            'marginTop':'2rem',
                                            'color':'white'
                                },
                            ),
                            dcc.DatePickerRange(
                                id='my_date_picker_range',
                                min_date_allowed=api_meteo_helper.get_min_time_in_db(conn_db),
                                max_date_allowed=api_meteo_helper.get_max_time_in_db(conn_db),
                                initial_visible_month=api_meteo_helper.get_max_time_in_db(conn_db),
                                display_format='YYYY-MM-DD',
                                end_date=date.today(),
                                className="mt-4"
                            ),
                            dcc.Download(id="download_meteo_csv"),
                            dbc.Button('Export as csv', id='btn_export_csv', className='ml-5 mt-4 btn btn-outline-success',
                                       n_clicks=0)
                        ],
                        className="row justify-content-center "),
                        html.Div(
                            id='export_data_meteo_confirmation',
                            children=[],
                            className="row justify-content-center mt-3 display-5 text-center",
                    ),
                ],
                fluid=True,
                className="row justify-content-center pt-5",
            ),
    ], style={'height':'25vh', 'marginTop':'25px', 'marginLeft':'10px'}
)

card_map = dbc.Card([
    dl.Map([dl.TileLayer(), dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}, startDirectly=True)],
    id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
], style={'height':'50vh', 'marginRight':'10px', 'marginTop':'20px'})
            
card_prevision = dbc.Card([
], style={'height':'25vh', 'marginTop':'25px', 'marginLeft':'10px'})

card_infomap = dbc.Card([
    html.H4("Informations géographiques", className='mt-3'),
    html.Div(id="text")
], style={'height':'25vh', 'marginTop':'25px', 'marginRight':'10px', 'textAlign':'center'})
                    

meteo_layout = html.Div([
    dbc.Row(
        [
            dbc.Col(card_gauge, width=8),
            dbc.Col(card_map, width=4)
        ]
    ),
    dbc.Row(
        [
            dbc.Col(card_export_meteo_layout, width=8),
            dbc.Col(card_infomap, width=4),
        ]
    )
])

@app.callback(
    Output("download_meteo_csv", "data"),
    Output("export_data_meteo_confirmation", "children"),
    State("my_date_picker_range", "start_date"),
    State("my_date_picker_range", "end_date"),
    State("check_list_data", "value"),
    Input("btn_export_csv", "n_clicks"),
)
def export_data_to_csv(start_date, end_date, check_list_value, n_clicks):
    """
    export to csv the data of the pv from the start date to the end_date.

    :params start_date: start date of the date-picker-range
    :params end_date: end date of the date-picker-range
    """
    if n_clicks > 0:
        print(check_list_value)
        start_date_stamp = time.mktime(time.strptime(start_date, '%Y-%m-%d'))
        end_date_stamp = time.mktime(time.strptime(end_date, '%Y-%m-%d'))
        statement = f'SELECT outTemp,pressure,outHumidity,windSpeed FROM archive WHERE dateTime >= {start_date_stamp} AND dateTime <= {end_date_stamp};'
        #statement = f"SELECT outTemp,pressure,outHumidity,windSpeed FROM archive WHERE dateTime >= {timestamp}"
        df = pd.read_sql_query(statement, conn_db)
        dict = {}
        for key in check_list_value:
            dict[key]=df[key]
        export_data_file_name='export_meteo_from_'+str(start_date)+'_to_'+str(end_date)+'.csv'
        dff = pd.DataFrame.from_dict(dict)
        print(dff)
        return dcc.send_data_frame(dff.to_csv, filename=export_data_file_name, index=False), 'data successfully saved'
    raise PreventUpdate

                            
@app.callback(
    Output("text", "children"),
    Input("map", "location_lat_lon_acc"),
    prevent_initial_call=True
)
def update_location(location):
    return "Latitude : {} Longitude : {}".format(location[0], location[1])    

@app.callback(
    Output("temp_led", "value"),
    Output("daq_temp", "value"),
    Output("pression_led", "value"),
    Output("daq_pression", "value"),
    Output("humi_led", "value"),
    Output("daq_humi", "value"),
    Output("vent_led", "value"),
    Output("daq_vent", "value"),
    Input("data_update_temp", "n_intervals")
)
def gauge_temp(interval):
    if interval==0:
        raise PreventUpdate
    else:
        timestamp = 1630533600
        statement = f"SELECT outTemp,pressure,outHumidity,windSpeed FROM archive WHERE dateTime >= {timestamp}"
        #statement = f'SELECT outTemp FROM archive'
        df_temp = pd.read_sql_query(statement, conn_db)
        # print(df_temp)
        # print(df_temp['outTemp'][0])
        temp = round(float(df_temp['outTemp'][0]),1)
        pression = round(float(df_temp['pressure'][0]),1)
        humidity = round(float(df_temp['outHumidity'][0]),1)
        vent = round(float(df_temp['windSpeed'][0]),1)
        return temp,temp,pression,pression,humidity,humidity,vent,vent

