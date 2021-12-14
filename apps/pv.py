import os
import pathlib
from dash import dcc
from dash import dash_table
from dash import html
from datetime import date
import time
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import sqlite3
import pandas as pd
import dash_daq as daq

from app import app

from apps.equipments.PV.Api import api_db_pv

# Parameters
DB_FILENAME = "../datasets/data_pv.db"
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)

# Connect to database
DB_FILE = pathlib.Path(__file__).parent.joinpath(DB_FILENAME).resolve()
conn_db = sqlite3.connect(DB_FILE, check_same_thread=False)

# Initialize table PV
#statement = f'SELECT * FROM measurements'
statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
df = pd.read_sql_query(statement, conn_db)
df_init = df.T
df_init = df_init.reset_index()
df_init.columns = ['Parameter', 'Value']

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

pv_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1(
                                    children='Panneau photovoltaïque',
                                    className="display-4 text-center text-white",
                                ),
                                html.Div(
                                    children='Donnees de la puissance géneré par les panneaux',
                                    className="display-5 text-center text-white",
                                ),
                            ],
                            className="bg-info h-100 mr-3 ml-3 mt-3 p-5 border border-5 rounded rounded-3 border-dark ",
                        ),
                    ],
                    md = 12,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                    html.H2("Puissance: [W]", className="display-3 mt-5 mb-5", style={'textAlign': 'center'}),
                                    html.Hr(className="my-2"),
                                    daq.LEDDisplay(
                                        id='power_display',
                                        label="",
                                        value=10000,
                                        color=theme['secondary'],
                                        className='mt-5 dark-theme-control row justify-content-center'
                                    ),
                                    html.Div(
                                    id='power_display_info',
                                    children='(recu a 10h39)',
                                    className="display-5 text-center mt-5",
                                ),
                            ],
                            className="bg-secondary h-100 p-5 ml-3 mt-5 border border-2 rounded rounded-3 border-dark",
                        ),
                    ],
                    md = 6,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="plot_power_pv",
                                    config=dict(
                                        showTips=False,
                                        displayModeBar=False,
                                    ),
                                ),
                                dcc.Interval(
                                    id="data_update_pv",
                                    interval=int(GRAPH_INTERVAL),
                                    n_intervals=20,
                                ),
                                html.Hr(className="my-2"),
                                html.Div(
                                    children='SELECT DATA AND EXPORT:',
                                    className="display-5 text-center",
                                ),
                                html.Div([
                                        dcc.DatePickerRange(
                                            id='my_date_picker_range',
                                            min_date_allowed=api_db_pv.get_min_time_in_db(conn_db),
                                            max_date_allowed=api_db_pv.get_max_time_in_db(conn_db),
                                            initial_visible_month=api_db_pv.get_min_time_in_db(conn_db),
                                            display_format='YYYY-MM-DD',
                                            end_date=date.today()
                                        ),
                                        dcc.Download(id="download_csv"),
                                        dbc.Button('Export as csv', id='btn_export_csv', className='ml-5 btn btn-outline-success', n_clicks=0)
                                    ], className="row justify-content-center mt-3",
                                ),
                                html.Div(
                                    id='export_data_confirmation',
                                    children=[],
                                    className="row justify-content-center mt-3 display-5 text-center",
                                ),
                            ],
                            className="bg-secondary h-100 p-5 mr-3 mt-5 border border-5 rounded rounded-3 border-dark",
                        ),
                    ],
                    md = 6,
                ),
            ],
            style={'margin-bottom': 20},
        )
    ],
    className="app__container",
)  # end table PV

@app.callback(
    Output("download_csv", "data"),
    Output("export_data_confirmation", "children"),
    State("my_date_picker_range", "start_date"),
    State("my_date_picker_range", "end_date"),
    Input("btn_export_csv", "n_clicks")
)
def export_data_to_csv(start_date, end_date, n_clicks):
    """
    export to csv the data of the pv from the start date to the end_date.

    :params start_date: start date of the date-picker-range
    :params end_date: end date of the date-picker-range
    """
    if n_clicks > 0:
        statement = f'SELECT * FROM measurements WHERE strftime(\'%Y-%m-%d\', time) >= \'{start_date}\' AND strftime(\'%Y-%m-%d\', time) <= \'{end_date}\' ORDER BY time ASC'
        df = pd.read_sql_query(statement, conn_db)
        dict = {'time':df['time'], 'PV_power':df['PV_power']}
        export_data_file_name='export_pv_from_'+str(start_date)+'_to_'+str(end_date)+'.csv'
        export_data=[]
        for index, value in enumerate(dict['time']):
            if value[:10] >= start_date and value[:10] <= end_date:
                data = [str(value),str(dict['PV_power'][index])]
                export_data.append(data)
        dff = pd.DataFrame(export_data, columns=['time','PV_power'])
        return dcc.send_data_frame(dff.to_csv, filename=export_data_file_name, index=False), 'data successfully saved'
    raise PreventUpdate



# call back pv
@app.callback(
    Output("plot_power_pv", "figure"),
    Output("power_display", "value"),
    Output("power_display_info", "children"),
    [Input("data_update_pv", "DatePickerRange")]
)
def gen_power_pv(intervals):
    """
    Generate the power graph.

    :params interval: update the graph based on an interval
    """
    #statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
    #statement = f"SELECT * FROM measurements WHERE time == datetime('now','-1 hours') ORDER BY time DESC LIMIT 200;"
    last_date_in_db = api_db_pv.get_max_time_in_db(conn_db)
    statement = f"SELECT * FROM measurements WHERE strftime(\'%Y-%m-%d\', time) >= \'{last_date_in_db}\' ORDER BY time ASC"
    df = pd.read_sql_query(statement, conn_db)

    latest_pv_power_index = len(df['PV_power']) - 1
    latest_pv_value = df['PV_power'][latest_pv_power_index]
    latest_time = df['time'][latest_pv_power_index]

    trace1 = dict(
        type="scatter",
        x=df["time"],
        y=df["PV_power"],
        line={"color": "#FF3048"},
        mode="lines",
        name="system power [W]",
    )

    layout = dict(
        plot_bgcolor="#FFF",
        paper_bgcolor="#FFF",
        font={"color": "#666"},
        margin=dict(l=30, r=0, b=45, t=43),
        title=dict(text="Puissance genere sur la journee du", x=0.5),
        xaxis={
            #"range": [0, 200],
            "showline": True,
            "invert": True,
            "zeroline": False,
            # "fixedrange": True,
            # "title": "Temps",
            # "autorange": "reversed"
        },
        yaxis={
            "range": [0, 10000],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": "#FFF",
            "title": dict(text="Power [W]", x=-0.5),
        },
    )

    return dict(data=[trace1], layout=layout), latest_pv_value, f'reçu le {latest_time}'
# end callback pv