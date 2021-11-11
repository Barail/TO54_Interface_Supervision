import dash
import dash_core_components as dcc

import dash_html_components as html
import plotly.express as px

import pandas as pd
from datetime import datetime, time
from datetime import date
import time

import sqlite3
import datetime

import csv

div_style1 = {
    "width": '20%',
    "height": '5%',
    'margin-left':'20px',
    'margin-right':'20px',
    'margin-top':'10px',
    'margin-bottom':'10px',
    "display": "inline-block",

    "textAlign": "left",
}

div_style2 = {
    "width": '20%',
    "height": '5%',
    'margin-left':'20px',
    'margin-right':'20px',
    'margin-top':'10px',
    'margin-bottom':'10px',
    "display": "inline-block",

    "textAlign": "right",
}



# server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

db_file = 'weewx.sdb'
conn = sqlite3.connect(db_file, check_same_thread=False)
statement = f'SELECT * FROM archive ORDER BY dateTime DESC LIMIT 10080;'
df = pd.read_sql_query(statement, conn)
# print(df)

df['dateTime'] = df['dateTime'].apply(time.localtime)


def shijian(timeArray):
    a = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return a


df['dateTime'] = df['dateTime'].apply(shijian)
df['dateTime'] = pd.to_datetime(df.dateTime)
df = df.sort_values(['dateTime'])
print(df)
data = df


# data=df[(df['dateTime']>pd.to_datetime('2021-04-01'))  & (df['dateTime']<pd.to_datetime('2021-04-30'))].dropna(axis=1)  # å…¨å±€å˜é‡
# print(df)


@app.callback(
    # dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Output("plot1", "figure"),
     dash.dependencies.Output("plot2", "figure"),
     dash.dependencies.Output("plot3", "figure"),
     dash.dependencies.Output("plot4", "figure"),
     dash.dependencies.Output("plot5", "figure"),
     dash.dependencies.Output("plot6", "figure")],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    # string_prefix = 'You have selected: '
    print(start_date)
    print(end_date)
    if start_date is not None and end_date is not None:
        # data=df[(df['dateTime']>pd.to_datetime(start_date))  & (df['dateTime']<pd.to_datetime(end_date))].dropna(axis=1)  # å…¨å±€å˜é‡
        start_date_ts = time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple())
        end_date_ts = time.mktime(datetime.datetime.strptime(end_date, "%Y-%m-%d").timetuple())
        statement = f'SELECT * FROM archive WHERE dateTime between ' + str(start_date_ts) + ' and ' + str(
            end_date_ts) + ';'
        print(statement)
        df = pd.read_sql_query(statement, conn)
        data = df
        print(df)

        trace1 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['inTemp'],
        )
        trace2 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['pressure'],
        )
        trace3 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['barometer'],
        )
        trace4 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['inHumidity'],
        )
        trace5 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['windSpeed'],
        )
        trace6 = dict(
            type="scatter",
            x=data['dateTime'],
            y=data['radiation'],
        )

        layout = dict()

    return [dict(data=[trace1], layout=layout), dict(data=[trace2], layout=layout), dict(data=[trace3], layout=layout),
            dict(data=[trace4], layout=layout), dict(data=[trace5], layout=layout), dict(data=[trace6], layout=layout)]
    # return string_prefix


# FIGURE
fig1 = {'data':
   [px.line(
    x=data['dateTime'],
    y=data['inTemp'],
    title="inTemp",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'temperature'})

        }
fig_1 = html.Div(
    [
        dcc.Graph(
            id="plot1",
            figure=fig1
        )
    ],
    style=div_style1,
)

fig2 = {'data':
   [px.line(
    x=data['dateTime'],
    y=data['pressure'],
    title="pressure",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'pressure'})

        }

fig_2 = html.Div(
    [
        dcc.Graph(
            id="plot2",
            figure=fig2
        )
    ],
    style=div_style2,
)

fig3  = {'data':
   [px.line(
    x=data['dateTime'],
    y=data['barometer'],
    title="barometer",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'barometer'})

        }

fig_3 = html.Div(
    [
        dcc.Graph(
            id="plot3",
            figure=fig3
        )
    ],
    style=div_style1,
)

fig4 = {'data':
   [px.line(
    x=data['dateTime'],
    y=data['inHumidity'],
    title="inHumidity",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'inHumidity'})

        }

fig_4 = html.Div(
    [
        dcc.Graph(
            id="plot4",
            figure=fig4
        )
    ],
    style=div_style2,
)

fig5 ={'data':
   [px.line(
    x=data['dateTime'],
    y=data['windSpeed'],
    title="windSpeed",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'windSpeed'})

        }

fig_5 = html.Div(
    [
        dcc.Graph(
            id="plot5",
            figure=fig5
        )
    ],
    style=div_style1,
)

fig6 = {'data':
   [px.line(
    x=data['dateTime'],
    y=data['radiation'],
    title="radiation",
     )],
#        'layout':px.layout(
#                xaxis={'title': 'time'},
#                yaxis={'title': 'radiation'})

        }

fig_6 = html.Div(
    [
        dcc.Graph(
            id="plot6",
            figure=fig6
        )
    ],
    style=div_style2,
)

# html
app.layout = html.Div(
    children=[
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2019, 6, 16),
            max_date_allowed=date(2021, 5, 4),
            initial_visible_month=date(2021, 4, 30),
            start_date=date(2021, 4, 1),
            end_date=date(2021, 4, 30)
        ),
        html.Div(id='output-container-date-picker-range'),
        html.Div([fig_1]),
        html.Div([fig_2]),
        html.Div([fig_3]),
        html.Div([fig_4]),
        html.Div([fig_5]),
        html.Div([fig_6])
    ]
)

n = [data['dateTime'], data['inTemp'], data['pressure'], data['barometer'], data['inHumidity'], data['windSpeed'],
     data['radiation']]
b = ["time", "intemp", "barometer", 'inHumidity', 'windSpeed', 'radiation']
i=int(input('if you want to get csv'))
if i == 1:
 with open("weather.csv", 'w', newline='') as t:
    writer = csv.writer(t)
    writer.writerow(b)
    writer.writerows(n)
else:
    print('no csv')

if __name__ == "__main__":
    app.run_server(debug=True)
