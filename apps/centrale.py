import os
import pathlib
import numpy as np
import dash
from dash import dcc
from dash import dash_table
import dash_daq as daq
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import sqlite3
import pandas as pd
# import api_pdu
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Parameters
# DB_FILENAME = "../datasets/data.db"
# DB_FILENAME_2 = "../datasets/data_centrale_tri.db"
# GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)
#
# # Connect to database
# DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME).resolve()
# DB_FILE_2 = pathlib.Path(__file__).resolve().parent.joinpath(DB_FILENAME_2).resolve()
# conn_db = sqlite3.connect(DB_FILE, check_same_thread=False)
# conn_db_2 = sqlite3.connect(DB_FILE_2, check_same_thread=False)

# #Initialize table contents
# statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
# df = pd.read_sql_query(statement, conn_db)
# df_init = df.T
# df_init = df_init.reset_index()
# df_init.columns=['Parameter','Value']
#
# #Initialize table contents 2
# statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
# df = pd.read_sql_query(statement, conn_db_2)
# df_init = df.T
# df_init = df_init.reset_index()
# df_init.columns=['Parameter','Value']

# layout = html.Div(
#     [
#         # header
#         dbc.Row(
#             [
#
#                 # Project description
#                 dbc.Col(
#                     [
#                         html.P(
#                             "Supervision centrale",
#                             className="app__header__title--grey",
#                         ),
#                     ], width=2,
#                 ),
#             ],
#             style={'margin-bottom': 20},
#         ),
#         # Tabs
#         dcc.Tabs(
#             [
#                 # Simple mode
#                 dcc.Tab(
#                     label='Mode normal',
#                     children=[
#                         dbc.Row(
#                             [
#                                 dbc.Col(daq.Indicator(
#                                     id='Status_HyProvide',
#                                     label="Status HyProvide",
#                                     value=False,
#                                     color="#0F0",
#                                     size=20,
#                                 ), width=1),
#                                 dbc.Col(daq.Indicator(
#                                     id='Stop_code-HyProvide',
#                                     label="Stop code HyProvide",
#                                     value=False,
#                                     color="#0F0",
#                                     size=20,
#                                 ), width=1),
#                                 dbc.Col(daq.Indicator(
#                                     id='status_hydry-indicator',
#                                     label="Status HyDry",
#                                     value=False,
#                                     color="#0F0",
#                                     size=20,
#                                 ), width=1),
#                                 dbc.Col(daq.Indicator(
#                                     id='Stop_code_hydry-indicator',
#                                     label="Stop code HyDry",
#                                     value=False,
#                                     color="#0F0",
#                                     size=20,
#                                 ), width=1)
#                             ]),  # end row
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     [
#                                         dcc.Graph(
#                                             id="plot-power_centrale",
#                                             config=dict(
#                                                 displayModeBar=False,
#                                             ),
#                                         ),
#                                         dcc.Graph(
#                                             id="plot-power",
#                                             config=dict(
#                                                 displayModeBar=False,
#                                             ),
#                                         ),
#                                         dcc.Interval(
#                                             id="data-update",
#                                             interval=int(GRAPH_INTERVAL),
#                                             n_intervals=0,
#                                         ),
#                                         dcc.Interval(
#                                             id="data-update_centrale",
#                                             interval=int(GRAPH_INTERVAL),
#                                             n_intervals=0,
#                                         ),
#                                     ],
#                                 ),
#                             ],
#                             style={'margin-bottom': 20},
#                         ),
#                         dbc.Row(
#                             # Badges
#                             [
#                                 dbc.Col(dbc.Badge(
#                                     "Stack current : 0 A",
#                                     id='bdg_stack_current'
#                                 ), width=1),
#
#                                 dbc.Col(dbc.Badge(
#                                     "Voltage : 0 V",
#                                     id='bdg_voltage'
#                                 ), width=1),
#
#                                 dbc.Col(dbc.Badge(
#                                     "Stack power : 0 kW",
#                                     id='bdg_Stack_power'
#                                 ), width=1),
#                             ], ),  # end row
#                         dbc.Row(
#                             [
#                                 dbc.Col(dbc.Badge(
#                                     "H2 production : 0 Nm^3/h",
#                                     id='bdg_h2_production'
#                                 ), width=2),
#                                 dbc.Col(dbc.Badge(
#                                     "Output pressure : 0 barg",
#                                     id='bdg_output_pressure'
#                                 ), width=2),
#                             ], ),  # end row
#                         dbc.Row(
#                             [
#                                 dbc.Col(dbc.Badge(
#                                     "Stack outlet water temperature : 0 °C",
#                                     id='bdg_water_temp_out_stack'
#                                 ), width=2),
#                                 dbc.Col(dbc.Badge(
#                                     "Water flow : 0 L/min",
#                                     id='bdg_water_flow'
#                                 ), width=2),
#                             ],
#                             style={'margin-bottom': 20},
#                         ),  # end row
#                         # end row
#                     ],  # end tab children
#                 ),  # end tab
#                 # Expert mode
#                 dcc.Tab(
#                     label='Mode expert',
#                     children=[
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dash_table.DataTable(
#                                         id='table_gen',
#                                         columns=[{'name': i, 'id': i} for i in df_init.columns],
#                                         data=df_init.to_dict('records'),
#                                         style_data_conditional=[
#                                             {
#                                                 'if': {
#                                                     'column_id': 'Value',
#                                                 },
#                                                 'backgroundColor': '#ebf9ff',
#                                                 'color': '#666'
#                                             },
#                                             {
#                                                 'if': {
#                                                     'filter_query': '{Value} < 0',
#                                                     'column_id': 'Value'
#                                                 },
#                                                 'backgroundColor': 'tomato',
#                                                 'color': 'white'
#                                             },
#                                         ],
#                                         style_cell={'fontSize': '1.0em', 'font-family': 'sans-serif', 'color': '#666',
#                                                     'textAlign': 'left'},
#                                     ),  # end table
#                                 ),  # end col
#                             ],
#                             style={'margin-bottom': 20, 'margin-top': 20},
#                         ),  # end row
#                     ],  # end tab children
#                 ),  # end tab
#             ],
#             style={'padding': 6},
#         ),  # end tabs
#         html.Div(id='hidden-div', style={'display': 'none'}),  # fake div for no output callbacks
#         html.Div(id='hidden-div2', style={'display': 'none'}),  # fake div for no output callbacks
#     ],
#     className="app__container",
# )  # end table PV
#
#
# @app.callback(
#     Output("plot-power", "figure"), [Input("data-update", "n_intervals")]
# )
# def gen_power(interval):
#     """
#     Generate the power graph.
#
#     :params interval: update the graph based on an interval
#     """
#
#     statement = f"SELECT * FROM measurements WHERE time >= datetime('now','-1 hours') ORDER BY time DESC LIMIT 200;"
#     df = pd.read_sql_query(statement, conn_db)
#
#     trace1 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["Stack_current"],
#         line={"color": "#42C4F7"},
#         mode="lines",
#         name="I_stack [A]",
#     )
#     trace2 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["Water_conductivity"],
#         line={"color": "#066489"},
#         mode="lines",
#         name="Water cond [μS/cm]",
#     )
#     trace3 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["water_temp_out_stack"],
#         line={"color": "#F00"},
#         mode="lines",
#         name="T_out [°C]",
#     )
#
#     trace4 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["water_temp_in_stack"],
#         line={"color": "#0F0"},
#         mode="lines",
#         name="T_in [°C]",
#     )
#
#     trace5 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["Stack_power"] / 10000,
#         line={"color": "#000"},
#         mode="lines",
#         name="Power [kW]",
#         yaxis="y2"  # gyjgyguj
#     )
#
#     trace6 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["voltage"],
#         line={"color": "#ff7f00"},
#         mode="lines",
#         name="Voltage [V]",
#     )
#
#     trace7 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["h2_production"],
#         line={"color": "black"},
#         mode="lines",
#         name="H2 production [Nm^3/h]"
#     )
#
#     layout = dict(
#         plot_bgcolor="#FFF",
#         paper_bgcolor="#FFF",
#         font={"color": "#666"},
#         margin=dict(l=30, r=0, b=45, t=43),
#         title=dict(text="Valeurs", x=0.02),
#         xaxis={
#             # "range": [0, 200],
#             "showline": True,
#             "invert": True,
#             "zeroline": False,
#             # "fixedrange": True,
#             # "title": "Temps",
#             # "autorange": "reversed"
#         },
#         yaxis={
#             "range": [0, 50],
#             "showgrid": True,
#             "showline": True,
#             "fixedrange": True,
#             "zeroline": False,
#             "gridcolor": "#CCC",
#             "title": None,
#         },
#         yaxis2=dict(  # ffkhghgkhg
#             title="Power",
#             anchor="free",
#             overlaying="y",
#             side="right",
#             position=1
#         ),
#     )
#
#     return dict(data=[trace1, trace2, trace3, trace4, trace5, trace6, trace7], layout=layout)
#
#
# # call back centrale
# @app.callback(
#     Output("plot-power_centrale", "figure"), [Input("data-update_centrale", "n_intervals")]
# )
# def gen_power_centrale(interval):
#     """
#     Generate the power graph.
#
#     :params interval: update the graph based on an interval
#     """
#
#     statement = f"SELECT * FROM measurements WHERE time >= datetime('now','-1 hours') ORDER BY time DESC LIMIT 200;"
#     df = pd.read_sql_query(statement, conn_db_2)
#
#     trace1 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["puissance_centrale_tri"],
#         line={"color": "#FF0000"},
#         mode="lines",
#         name="system power [W]",
#     )
#     trace2 = dict(
#         type="scatter",
#         x=df["time"],
#         y=df["courant_centrale_tri"],
#         line={"color": "#CC33FF"},
#         mode="lines",
#         name="system current [A]",
#     )
#
#     layout = dict(
#         plot_bgcolor="#FFF",
#         paper_bgcolor="#FFF",
#         font={"color": "#666"},
#         margin=dict(l=30, r=0, b=45, t=43),
#         title=dict(text="Valeurs", x=0.02),
#         xaxis={
#             # "range": [0, 200],
#             "showline": True,
#             "invert": True,
#             "zeroline": False,
#             # "fixedrange": True,
#             # "title": "Temps",
#             # "autorange": "reversed"
#         },
#         yaxis={
#             "range": [0, 50],
#             "showgrid": True,
#             "showline": True,
#             "fixedrange": True,
#             "zeroline": False,
#             "gridcolor": "#CCC",
#             "title": "Power unit",
#         },
#     )
#
#     return dict(data=[trace1, trace2], layout=layout)
#
#
# # end callback centrale
#
# @app.callback(
#     Output("table_gen", "data"), Output('table_gen', 'columns'), [Input("data-update", "n_intervals")]
# )
# def update_table_gen(interval):
#     """
#     Generate the generator table.
#
#     :params interval: update the graph based on an interval
#     """
#
#     statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     df = pd.read_sql_query(statement, conn_db)
#     # statement0 = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     # df0 = pd.read_sql_query(statement0, conn_db0)
#     # df_combine = pd.concat([df, df0])
#     df_combine = pd.concat([df])
#     df_init = df_combine.T
#     df_init = df_init.reset_index()
#     df_init.columns = ['Parameter', 'Value']
#     data = df_init.to_dict('records')
#     columns = [{"name": i, "id": i} for i in df_init.columns]
#     return (data, columns)
#
#
# # Badges
# @app.callback(
#     Output('bdg_stack_current', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_stack_current(interval):
#     statement = f'SELECT Stack_current FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children = "Stack current : " + str(df['Stack_current'].iloc[0]) + " A"
#
#     return children
#
#
# @app.callback(
#     Output('bdg_voltage', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_voltage(interval):
#     statement = f'SELECT voltage FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children = "Voltage : " + str(df['voltage'].iloc[0]) + " V"
#     return children
#
#
# @app.callback(
#     Output('bdg_Stack_power', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_Stack_power(interval):
#     statement = f'SELECT Stack_power FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children = "Power : " + str(df['Stack_power'].iloc[0] / 10000) + " kW"
#     return children
#
#
# @app.callback(
#     Output('bdg_h2_production', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_h2_production(interval):
#     statement = f'SELECT h2_production FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children = "Hydrogen production : " + str(df['h2_production'].iloc[0]) + " Nm^3/h "
#     return children
#
#
# @app.callback(
#     Output('bdg_water_temp_out_stack', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_water_temp_out_stack(interval):
#     statement = f'SELECT water_temp_out_stack FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     water_temp = "Outlet water temperature : " + str(df['water_temp_out_stack'].iloc[0]) + " °C"
#     return water_temp
#
#
# @app.callback(
#     Output('bdg_output_pressure', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_output_pressure(interval):
#     statement = f'SELECT output_pressure FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children = "Output pressure : " + str(df['output_pressure'].iloc[0]) + " barg"
#     return children
#
#
# @app.callback(
#     Output('bdg_water_flow', 'children'),
#     [Input("data-update", "n_intervals")])
# def update_bdg_water_flow(interval):
#     statement = f'SELECT water_flow FROM measurements ORDER BY time DESC LIMIT 1;'
#     df = pd.read_sql_query(statement, conn_db)
#
#     children_wf = "Water flow : " + str(df['water_flow'].iloc[0]) + " L/min "
#     return children_wf
#
#
# @app.callback(
#     Output('Stop_code-HyProvide', 'color'), Output('Stop_code-HyProvide', 'label'),
#     [Input("data-update", "n_intervals")])
# def update_indicators(interval):
#     green_style = 'green'
#     red_style = 'red'
#     orange_style = 'orange'
#
#     statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     df = pd.read_sql_query(statement, conn_db)
#
#     if df['stop_code'].iloc[0] == 0:
#         stop_code_indic_style = orange_style
#         label = 'no error'
#     if df['stop_code'].iloc[0] == 1:
#         stop_code_indic_style = red_style
#         label = 'HyProvide off'
#     if df['stop_code'].iloc[0] == 2:
#         stop_code_indic_style = red_style
#         label = 'current low'
#     if df['stop_code'].iloc[0] == 100:
#         stop_code_indic_style = red_style
#         label = 'error stops'
#     if df['stop_code'].iloc[0] == 104:
#         stop_code_indic_style = red_style
#         label = 'positive current'
#     if df['stop_code'].iloc[0] == 105:
#         stop_code_indic_style = red_style
#         label = 'negative current'
#     if df['stop_code'].iloc[0] == 106:
#         stop_code_indic_style = red_style
#         label = 'fatal bit'
#     if df['stop_code'].iloc[0] == 107:
#         stop_code_indic_style = red_style
#         label = 'max temperature'
#     if df['stop_code'].iloc[0] == 108:
#         stop_code_indic_style = red_style
#         label = 'i stack alarm'
#     if df['stop_code'].iloc[0] == 110:
#         stop_code_indic_style = red_style
#         label = 'temperature out'
#     if df['stop_code'].iloc[0] == 111:
#         stop_code_indic_style = red_style
#         label = 'h2 pressure'
#     if df['stop_code'].iloc[0] == 116:
#         stop_code_indic_style = red_style
#         label = 'wd'
#     if df['stop_code'].iloc[0] == 120:
#         stop_code_indic_style = red_style
#         label = 'h2o supply'
#     if df['stop_code'].iloc[0] == 122:
#         stop_code_indic_style = red_style
#         label = 'h2o pressure'
#     if df['stop_code'].iloc[0] == 123:
#         stop_code_indic_style = red_style
#         label = 'conductivity'
#     if df['stop_code'].iloc[0] == 124:
#         stop_code_indic_style = red_style
#         label = 'h2 alarm'
#     if df['stop_code'].iloc[0] == 125:
#         stop_code_indic_style = red_style
#         label = 'hydrogen pressure'
#     if df['stop_code'].iloc[0] == 150:
#         stop_code_indic_style = red_style
#         label = 'i out low'
#     if df['stop_code'].iloc[0] == 200:
#         stop_code_indic_style = red_style
#         label = 'pressure flow'
#
#     return (stop_code_indic_style, label)
#
#
# @app.callback(
#     Output('Status_HyProvide', 'label'), Output('Status_HyProvide', 'color'),
#     [Input("data-update", "n_intervals")])
# def update_status(interval):
#     green_style = 'green'
#     red_style = 'red'
#     orange_style = 'orange'
#     grey_style = 'grey'
#     yellow_style = 'yellow'
#
#     statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     df = pd.read_sql_query(statement, conn_db)
#
#     if df['status'].iloc[0] == 0:
#         label = 'HyProvide off'
#         status_indic_style = grey_style
#         # grey
#     if df['status'].iloc[0] == 1:
#         label = 'Status: idle'
#         status_indic_style = orange_style
#         # orange
#     if df['status'].iloc[0] == 2:
#         label = 'pump on'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 3:
#         label = 'flush h2'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 4:
#         label = 'build h2 press'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 5:
#         label = 'build o2 press'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 6:
#         label = 'run'
#         status_indic_style = green_style
#         # green
#     if df['status'].iloc[0] == 7:
#         label = 'power down'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 8:
#         label = 'current off'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 9:
#         label = 'depress o2'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 10:
#         label = 'depress h2'
#         status_indic_style = yellow_style
#         # yelow
#     if df['status'].iloc[0] == 11:
#         label = 'shutdown'
#         status_indic_style = yellow_style
#         # yelow
#
#     return (label, status_indic_style)
#
#
# @app.callback(
#     Output('Stop_code_hydry-indicator', 'color'), Output('Stop_code_hydry-indicator', 'label'),
#     [Input("data-update", "n_intervals")])
# def update_HD_indicators(interval):
#     green_style = 'green'
#     red_style = 'red'
#     orange_style = 'orange'
#     grey_style = 'grey'
#     yellow_style = 'yellow'
#
#     statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     df = pd.read_sql_query(statement, conn_db)
#
#     if df['stop_code_HyDry'].iloc[0] == 0:
#         stop_code_hydry_indic_style = green_style
#         label = 'no error'
#     if df['stop_code_HyDry'].iloc[0] == 1:
#         stop_code_hydry_indic_style = grey_style
#         label = 'HyDry off'
#     if df['stop_code_HyDry'].iloc[0] == 2:
#         stop_code_hydry_indic_style = red_style
#         label = 'deoxo cold'
#     if df['stop_code_HyDry'].iloc[0] == 3:
#         stop_code_hydry_indic_style = red_style
#         label = 'deoxo time'
#     if df['stop_code_HyDry'].iloc[0] == 4:
#         stop_code_hydry_indic_style = red_style
#         label = 'con temp'
#     if df['stop_code_HyDry'].iloc[0] == 5:
#         stop_code_hydry_indic_style = red_style
#         label = 'con time'
#     if df['stop_code_HyDry'].iloc[0] == 6:
#         stop_code_hydry_indic_style = red_style
#         label = 'predrain'
#     if df['stop_code_HyDry'].iloc[0] == 7:
#         stop_code_hydry_indic_style = red_style
#         label = 'condrain'
#     if df['stop_code_HyDry'].iloc[0] == 8:
#         stop_code_hydry_indic_style = red_style
#         label = 'pressure low'
#     if df['stop_code_HyDry'].iloc[0] == 9:
#         stop_code_hydry_indic_style = red_style
#         label = 'shutdown drain fail'
#     if df['stop_code_HyDry'].iloc[0] == 10:
#         stop_code_hydry_indic_style = red_style
#         label = 'dryer 1 fail'
#     if df['stop_code_HyDry'].iloc[0] == 11:
#         stop_code_hydry_indic_style = red_style
#         label = 'dryer 2 fail'
#     if df['stop_code_HyDry'].iloc[0] == 12:
#         stop_code_hydry_indic_style = red_style
#         label = 'no dryers'
#     if df['stop_code_HyDry'].iloc[0] == 13:
#         stop_code_hydry_indic_style = red_style
#         label = 'wd fail'
#     if df['stop_code_HyDry'].iloc[0] == 14:
#         stop_code_hydry_indic_style = red_style
#         label = 'slave wd fail'
#
#     return (stop_code_hydry_indic_style, label)
#
#
# @app.callback(
#     Output('status_hydry-indicator', 'color'), Output('status_hydry-indicator', 'label'),
#     [Input("data-update", "n_intervals")])
# def update_HD_status_indicators(interval):
#     green_style = 'green'
#     grey_style = 'grey'
#
#     statement = f'SELECT * FROM measurements WHERE ROWID IN ( SELECT max( ROWID ) FROM measurements );'
#     df = pd.read_sql_query(statement, conn_db)
#
#     if df['status_HyDry'].iloc[0] == 0:
#         status_hydry_indic_style = grey_style
#         label = 'HyDry off'
#     if df['status_HyDry'].iloc[0] == 1:
#         status_hydry_indic_style = green_style
#         label = 'Bootup'
#     if df['status_HyDry'].iloc[0] == 2:
#         status_hydry_indic_style = green_style
#         label = 'startup deox'
#     if df['status_HyDry'].iloc[0] == 3:
#         status_hydry_indic_style = green_style
#         label = 'startup condenser'
#     if df['status_HyDry'].iloc[0] == 4:
#         status_hydry_indic_style = green_style
#         label = 'startup pressure'
#     if df['status_HyDry'].iloc[0] == 5:
#         status_hydry_indic_style = green_style
#         label = 'opperation'
#     if df['status_HyDry'].iloc[0] == 6:
#         status_hydry_indic_style = green_style
#         label = 'shutdown drainers'
#     if df['status_HyDry'].iloc[0] == 7:
#         status_hydry_indic_style = green_style
#         label = 'shutdown drainers fin'
#     if df['status_HyDry'].iloc[0] == 8:
#         status_hydry_indic_style = green_style
#         label = 'post drying'
#
#     return (status_hydry_indic_style, label)

