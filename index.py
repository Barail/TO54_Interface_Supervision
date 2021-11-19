from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_flexbox_grid as dfx

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import pv, centrale, station_meteo

# main app layout that will contain all our equipments pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Accueil", href='../')),
                dbc.NavItem(dbc.NavLink("PV", href='/apps/pv')),
                dbc.NavItem(dbc.NavLink("Batteries", href='/apps/lol')),
                dbc.NavItem(dbc.NavLink("Station Meteo", href='/apps/station_meteo')),
            ],
            brand="Interface de Supervision - Batiment F",
            brand_href="",
            color="primary",
            dark=True,
        ),
    ], className="column"),
    # page content of our main page that will be fill with the layout of the equipment we want to see the data
    html.Div(id='page-content', children=[])
])

welcome_layout = html.Div([
    # header
    dbc.Row([
        dbc.Col([html.Div(id='pv_content', children=[pv.pv_layout])],md=6),
        dbc.Col([html.Div(id='station_meteo_content', children=[station_meteo.welcome_meteo_layout])],md=6),
    ]),
    dbc.Row([
        dbc.Col([html.Div(id='batteries_content', children=[])],md=12)
    ]),
])

welcome_layout2 = dfx.Grid(id='grid', fluid=True, children=[
        dfx.Row(children=[
            dfx.Col(xs=20, lg=5, children=[
                html.Div(id='station_meteo_content', children=[station_meteo.welcome_meteo_layout])
            ]),
            dfx.Col(xs=20, lg=5, children=[
                html.Div(id='batteries_content', children=[pv.pv_layout])
            ])
        ]),
        dfx.Row(id='row', children=[
            dfx.Col(id='col', xs=20, lg=5, children=html.Div(id='station_meteo_content', children=[station_meteo.welcome_meteo_layout])),
            dfx.Col(xs=20, lg=5, children=html.Div(id='electrolyseur_content', children=[pv.pv_layout]))
        ])
    ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/pv':
        return pv.pv_layout
    elif pathname == '/':
        return welcome_layout
    elif pathname == '/apps/station_meteo':
        return station_meteo.meteo_layout
    else:
        return "404 Page Error! Please choose a link okay ?"

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True, use_reloader=True)
