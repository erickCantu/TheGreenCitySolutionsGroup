from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
today = date.today()
from train_model import linreg_model

#forecasts = linreg_model(building_nr=5)

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select building:"),
    dcc.Dropdown(
        id="dropdown1",
        options=['Building 1', 'Building 2', 'Building 3', 
                'Building 4', 'Building 5', 'Building 6',
                'Building 7', 'Building 8', 'Building 9',
                'All Buildings'],
        value='Building 1',
        style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'middle'},
        clearable=False,
    ),
    dcc.DatePickerSingle(
            id='my-date-picker-single',
            month_format='Y-M-D',
            #min_date_allowed=today - timedelta(years=12, days=3),
            #max_date_allowed=today + timedelta(days=730),
            initial_visible_month=datetime(2011, 5, 5),
            date=datetime(2011, 5, 5)),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown1", "value"),
    Input("my-date-picker-single", "date"),
    )
def display_color(building_nr, date):
    if building_nr == "All Buildings":
        forecasts = pd.read_pickle('../data/models/linreg_poly_building_all.pkl')
    else:
        forecasts = pd.read_pickle('../data/models/linreg_poly_building_'+building_nr.split(' ')[1]+'.pkl')
    start_date = pd.Timestamp(date)
    end_date = pd.Timestamp(date) + pd.Timedelta(hours=24)
    masked_forecasts = forecasts.loc[start_date:end_date]
    #fig = px.line(masked_forecasts, x="datetime", y="linreg_poly")
    fig = px.line(masked_forecasts, x="datetime", y=["net_load_kW", "linreg_poly"])
    return fig


app.run_server(debug=True, port=8113)