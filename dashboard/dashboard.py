from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
today = date.today()
from train_model import linreg_model

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown1",
        options=list(range(1, 10)),
        value=5,
        clearable=False,
    ),
    dcc.Dropdown(
        id="dropdown2",
        options=['small', 'medium', 'large'],
        value='small',
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
    Input("dropdown2", "value"),
    Input("my-date-picker-single", "date"),
    )
def display_color(building_nr, size, date):
    start_date = pd.Timestamp(date)
    end_date = pd.Timestamp(date) + pd.Timedelta(hours=24)
    forecasts = linreg_model(building_nr=5)
    masked_forecasts = forecasts.loc[start_date:end_date]
    fig = px.line(masked_forecasts, x="datetime", y="linreg_poly")
    return fig


app.run_server(debug=True, port=8113)